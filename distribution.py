# Author: J. H. Montoya - montoyjh@gmail.com
import logging

import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go


logger = logging.getLogger(__name__)


class Distribution(object):
    """
    Distributor class, initializes with filenames corresponding
    to node and file lists.  Includes methods for parsing files,
    sorting nodes by both used capacity and total size, distributing
    files among nodes, summarizing the results, and plotting
    the resulting distribution.

    Args:
        files_list (dict
    """
    def __init__(self, files, nodes):
        self.files = files
        self.nodes = nodes
        self.placed_files = self.get_placed_files(nodes, files)

    @staticmethod
    def get_placed_files(nodes, files):
        node_space = list(zip(nodes))[1]
        placed_files = [[] for _ in len(nodes)]
        for file in tqdm(files):
            # Find biggest node and put the file in that spot
            logger.debug("Finding largest remaining space node")
            loc = np.argmax(node_space)

            # Add file to files on node
            logger.debug("Placing file on node: %s", nodes[loc][0])
            placed_files[loc].append(file)

            # Reduce available space on the node according to file size
            node_space[loc] -= file[1]
            if node_space[loc] < 0:
                raise ValueError("Files are too large to be placed on nodes")
        return placed_files

    @classmethod
    def from_filenames(cls, file_filename, node_filename):
        nodes = parse_file(node_filename)
        files = parse_file(file_filename)
        return cls(files, nodes)

    def plot(self):
        for x, (node, files) in enumerate(zip(self.nodes, self.placed_files)):
            # Draw outline
            plt.bar(x, node[0], color='w')
            bottom = 0.0
            for file in files:
                # Draw bars upward and move bottom
                plt.bar(x, file[1], bottom=bottom)
                bottom += file[1]
        plt.xticks([0.4 + x for x in range(len(self.nodes))],
                   [node.name for node in self.nodes])
        plt.show()

    def get_plotly(self):
        # hella wonky, but I'm not sure how to do it otherwise in plotly
        traces = []
        for pf, node in zip(self.placed_files, self.nodes):
            pf_names, pf_sizes = list(zip(pf))

            trace = go.Bar(
                x = [node[0]]*len(pf),
                y = pf_sizes,
                base = np.cumsum(pf_sizes) - pf_sizes[0]
            )
            traces.append(trace)

        fig = go.Figure(data=traces)
        py.iplot(fig, filename='stacked-bar')


# Helper methods for parsing files
def parse_file(filename):
    """Parses file into titles and values"""
    with open(filename) as f:
        lines = f.readlines()
    lines = [line for line in lines if not line.startswith("#")]
    pairs = [parse_line(line) for line in lines]
    return pairs

def parse_line(line):
    try:
        name, value = line.split(' ')
        return name, float(value)
    except:
        raise ValueError("Badly formatted line: {}. "
                         "Please format lines as 'NAME' 'VALUE'".format(line))
