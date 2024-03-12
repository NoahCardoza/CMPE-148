#!/bin/bash

# List of domains to ping
domains=(
    "berkeley.edu"
    "www.fbi.gov"
    "www.sis.gov.uk"
    "www.sjpd.org"
    "www.sjff.org"
)

START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BASE_PATH="scans/$START_TIME"
mkdir -p "$BASE_PATH"

# Loop through each domain and ping
for domain in "${domains[@]}"; do
    echo "- Starting ping and traceroute for $domain"
    mkdir -p "$BASE_PATH/$domain"
    ping -c 100 "$domain" > "$BASE_PATH/$domain/ping.log" 2>&1 &
    traceroute -m 100 "$domain" > "$BASE_PATH/$domain/trace.log" 2>&1 &
done

# Wait for all pings and traceroutes to complete
for job in `jobs -p`; do
    wait $job
done

echo "+ All pings and traceroutes complete."

echo "- Generating ping plots..."
poetry run python ping_plot.py $BASE_PATH/*/ping.log &
echo "- Generating traceroute diagrams..."
poetry run python traceroute_graph.py $BASE_PATH/*/trace.log &

# Wait for all plots and graphs to complete
for job in `jobs -p`; do
    wait $job
done

echo "+ All plots and graphs have been created."

echo "- Generating custom messages..."

poetry run python network_utilization_message.py $BASE_PATH/*/trace.log
poetry run python traceroute_message.py $BASE_PATH/*/trace.log

echo "+ Custom messages have been generated."