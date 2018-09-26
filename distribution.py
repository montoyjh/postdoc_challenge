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
        files ([tuple]): list of (filename, size) tuples corresponding
            to files to put on nodes
        nodes ([tuple]): list of (nodename, size) tuples corresponding
            to nodes on which to place files
    """
    def __init__(self, files, nodes):
        self.files = files
        self.nodes = nodes
        self.placed_files, self.null_files,\
            self.leftovers = self.distribute_files(nodes, files)

    @staticmethod
    def distribute_files(nodes, files):
        """
        Static method to distribute nodes and files.  The algorithm
        places each file sequentially in order of decreasing file size
        onto the node with the least used space on which it can fit.

        If a given file cannot fit on any node, it is placed into a
        null_files list, which is eventually returned with the list
        of placed files.

        Args:
            files ([tuple]): list of (filename, size) tuples corresponding
                to files to put on nodes
            nodes ([tuple]): list of (nodename, size) tuples corresponding
                to nodes on which to place files

        Returns:
            placed_files ([[tuple]]): a list of list of tuples of files
                placed on each node.  The list of lists is ordered in the
                same order as the node list.
            null_files ([tuple]): the list of files which cannot be placed
                on any node.
            used_space (np.array): total space used
        """
        null_files = []
        # Sort files by reverse size
        logger.debug("Sorting files")
        files = sorted(files, key=lambda x: -x[1])
        # Initialize node space and file placement array
        total_space = np.array(list(zip(*nodes))[1])
        used_space = np.zeros(total_space.shape)
        placed_files = [[] for _ in range(len(nodes))]
        for file in tqdm(files):
            candidates = used_space.copy()
            # Find biggest node and put the file in that spot
            logger.debug("Finding largest remaining space node")
            # Find where least space has been added where the file can fit
            mask = total_space - used_space >= file[1]
            if not mask.any():
                null_files.append(file)
            else:
                candidates[np.logical_not(mask)] = np.inf
                loc = np.argmin(candidates)
                logger.debug("Placing file on node: %s", nodes[loc][0])
                # Add file to files on node and reduce available space
                placed_files[loc].append(file)
                used_space[loc] += file[1]
        leftover = total_space - used_space
        return placed_files, null_files, leftover

    @classmethod
    def from_filenames(cls, file_filename, node_filename):
        """
        Factory method to initialize class from parsed input files

        Args:
            file_filename (str): filename corresponding to files input
            node_filename (str): filename corresponding to nodes input
        """
        nodes = parse_file(node_filename)
        files = parse_file(file_filename)
        return cls(files, nodes)

    def plot(self, show=False):
        """
        Simple plotting method, mostly for testing
        """
        for x, (node, files) in enumerate(zip(self.nodes, self.placed_files)):
            # Draw outline
            plt.bar(x, node[1], color='w', edgecolor='k')
            bottom = 0.0
            for file in files:
                # Draw bars upward and move bottom
                plt.bar(x, file[1], bottom=bottom)
                bottom += file[1]
        plt.xticks([x for x in range(len(self.nodes))],
                   [node[0] for node in self.nodes])
        plt.show()

    def get_plotly(self):
        # hella wonky, but I'm not sure how to do it otherwise in plotly
        traces = []
        for pf, node in zip(self.placed_files, self.nodes):
            pf_names, pf_sizes = list(zip(pf))
            trace = go.Bar(x=[node[0]]*len(pf), y=pf_sizes,
                           base=np.cumsum(pf_sizes) - pf_sizes[0])
            traces.append(trace)

        fig = go.Figure(data=traces)
        py.iplot(fig, filename='stacked-bar')

    def summary(self, output_file=None):
        lines = []
        for node, pf in zip(self.nodes, self.placed_files):
            for file in pf:
                lines.append('{} {}'.format(node[0], file[0]))
        lines.extend(['NULL {}'.format(file[0]) for file in self.null_files])
        text = '\n'.join(lines)
        if output_file:
            with open(output_file) as f:
                f.write(text)
        else:
            print(text)

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
