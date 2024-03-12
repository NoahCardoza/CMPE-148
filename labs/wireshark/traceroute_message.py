import sys
import re
import requests
from functools import cache

def parse_traceroute_output(trace_output):
    hops = []
    for line in trace_output.split('\n'):
        match = re.match(r'\s*\d+\s+(.*?)\s+\((\d+\.\d+\.\d+\.\d+)\)\s+(\d+\.\d+)\s+ms\s+(\d+\.\d+)\s+ms\s+(\d+\.\d+)\s+ms', line)
        if match:
            hop = {
                'hostname': match.group(1),
                'ip': match.group(2),
                'times': [float(match.group(i)) for i in range(3, 6)]
            }
            hops.append(hop)
    return hops

def find_slowest_router(hops):
    slowest_router = max(hops, key=lambda x: max(x['times']))
    return slowest_router

@cache
def get_location(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    if response.status_code == 200:
        data = response.json()
        return data.get('org'), data.get('city'), data.get('region'), data.get('country')
    else:
        return None
    

def create_message(trace_output):
    hops = parse_traceroute_output(trace_output)
    slowest_router = find_slowest_router(hops)
    slowest_ip = slowest_router['ip']
    location = get_location(slowest_ip)
    
    message = f"The slowest link in the traceroute was {slowest_ip}"
    
    if location:
        org, city, region, country = location
        if org:
            message += f", belonging to \"{org}\""

    message += f". The the worse RTT measurement was {max(slowest_router['times'])} ms."    

    if location:
        org, city, region, country = location
        message += f" The server is located in {city}, {region}, {country}."
    else:
        message += " The location of the server could not be determined."
    
    return message

def main():
    for arg in sys.argv[1:]:
        with open(arg, 'r') as file:
            trace_output = file.read()

        message = create_message(trace_output)
        
        with open(f"{arg}.message.txt", 'w') as file:
            file.write(message)
    

if __name__ == "__main__":
    main()
