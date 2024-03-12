import re
import sys
import matplotlib.pyplot as plt

# Parse ping output and extract wait times
def parse_ping_output(output):
    wait_times = []
    pattern = r"time=(\d+\.\d+)"
    matches = re.findall(pattern, output)
    for match in matches:
        wait_times.append(float(match))
    return wait_times

# Read ping output from a file
def read_ping_output_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Plot scatterplot of wait times
def plot_scatterplot(wait_times, output_file='pingplot.png'):
    plt.scatter(range(len(wait_times)), wait_times, color='blue', alpha=0.5)
    plt.title('Ping Wait Times')
    plt.xlabel('Packet Number')
    plt.ylabel('Wait Time (ms)')
    plt.grid(True)
    plt.savefig(output_file)
    plt.clf()

def plot_histogram(wait_times, output_file='pinghist.png'):
    plt.hist(wait_times, bins=20, color='blue', alpha=0.7)
    plt.title('Ping Wait Times Histogram')
    plt.xlabel('Wait Time (ms)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(output_file)
    plt.clf()


if __name__ == "__main__":
    for input_file in sys.argv[1:]:
        host = input_file.split('/')[-2]
        timestamp = input_file.split('/')[-3]
        ping_output = read_ping_output_from_file(input_file)
        wait_times = parse_ping_output(ping_output)
        # plot_scatterplot(wait_times, input_file + 'scatter.png')
        # plot_histogram(wait_times, input_file + 'hist.png')

        # Create a subplot with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Plot histogram on the first subplot
        ax1.hist(wait_times, bins=20, color='blue', alpha=0.7)
        ax1.set_title('Ping Wait Times Histogram')
        ax1.set_xlabel('Wait Time (ms)')
        ax1.set_ylabel('Frequency')
        ax1.grid(True)

        # Plot scatterplot on the second subplot
        ax2.scatter(range(len(wait_times)), wait_times, color='blue', alpha=0.5)
        ax2.set_title('Ping Wait Times Scatterplot')
        ax2.set_xlabel('Packet Number')
        ax2.set_ylabel('Wait Time (ms)')
        ax2.grid(True)

        fig.suptitle(f"{host} ({timestamp})", fontsize=16)

        plt.tight_layout()
        # plt.show()
        plt.savefig(input_file + '.png', dpi=800, bbox_inches='tight', pad_inches=0)
        plt.clf()