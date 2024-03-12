import sys
import json
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from schemdraw import flow
import re


# def read_traceroute(filename):
#     hops = []
#     hop_regex = re.compile(r'\s*\d+\s+(?P<ip>\d+\.\d+\.\d+\.\d+)\s+\((?P<hostname>[\w\.-]+)\)\s+(?P<times>(\d+\.\d+ ms\s*)+)')
    
#     next_hop_index = 2
#     hop = []

#     with open(filename, 'r') as file:
#         lines = file.readlines()
    
#     for line in lines:
#         match = hop_regex.match(line)
#         if match:
#             ip = match.group('ip')
#             hostname = match.group('hostname')
#             times = re.findall(r'(\d+\.\d+)', match.group('times'))
#             if str(next_hop_index) in line[0:4]:
#                 next_hop_index += 1
#                 hops.append(hop)
#                 hop = []
#             hop.append({'ip': ip, 'hostname': hostname, 'times': times})

    
#     return hops

import networkx as nx
from itertools import product

nodes = [1, 2, 3]
terminal = [0]

G = nx.from_edgelist(product(nodes, terminal), create_using=nx.DiGraph)


def read_traceroute(filename):
    hops = []
    hop = []
    next_hop_index = 2
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if 'ms' in line or '* * *' in line:
            if '* * *' in line:
                hostname = '* * *'
            else:
                hostname = line.split('(', 1)[1].split(')', 1)[0]
            if str(next_hop_index) in line[0:4]:
                next_hop_index += 1
                hops.append(hop)
                hop = []
            hop.append(hostname)
    if hop:
        hops.append(hop)
    
    return hops

def create_graph(filename: str, output_file: str = 'graph.png'):
    route = read_traceroute(filename)
    route = ['\n'.join(a) for a in route]

    with schemdraw.Drawing() as d:
        d.config(fontsize=13, unit=.5, fill='white', font='Times New Roman')
        for i in range(len(route)):
            flow.Circle().label(route[i])
            if i < len(route) - 1:
                flow.Arrow().right()

    fig = plt.gcf()
    fig.set_frameon(False)
    fig.set_size_inches(16, 3)

    ax = fig.gca()
    ax.axis('off')
    
    # plt.show()
    fig.savefig(output_file, dpi = 400, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.clf()


if __name__ == "__main__":
    for input_file in sys.argv[1:]:
        create_graph(input_file, input_file + '.png')