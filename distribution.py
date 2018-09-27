# Author: J. H. Montoya - montoyjh@gmail.com
import logging

import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
from plotly.offline import plot
import plotly.graph_objs as go
from pandas import DataFrame


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
    def __init__(self, nodes, files):
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
    def from_filenames(cls, node_filename, file_filename):
        """
        Factory method to initialize class from parsed input files

        Args:
            file_filename (str): filename corresponding to files input
            node_filename (str): filename corresponding to nodes input
        """
        with open(node_filename) as f:
            nstring = f.read()
        with open(file_filename) as g:
            fstring = g.read()
        return cls.from_strings(nstring, fstring)

    @classmethod
    def from_strings(cls, nodes_string, files_string):
        nodes = parse_string(nodes_string)
        files = parse_string(files_string)
        return cls(nodes, files)

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
        plt.yticks(np.arange(0, 10001, 1000))
        if show:
            plt.show()
        return plt

    def get_plotly(self, output_file='distribution.html'):
        df = DataFrame(self.placed_files, index=self.nodes)
        node_names = self.node_names
        data = []
        for col_id, contents in df.items():
            vals = [v if v is not None else (None, None)
                    for v in contents.values]
            file_names, file_sizes = list(zip(*vals))
            trace = go.Bar(x=node_names, y=file_sizes, text=file_names, name='')
            data.append(trace)
        data.append(go.Bar(x=node_names, y=self.leftovers,
                           marker={"color": "white",
                                   "line": {"color": "black",
                                            "width": 0.5}},
                           hovertext=[
                               "Leftover on {}: {}".format(node_name, leftover)
                               for node_name, leftover in
                               zip(node_names, self.leftovers)]))
        layout = go.Layout(barmode='stack', showlegend=False,
                           yaxis={"title": "Space"})
        fig = go.Figure(data=data, layout=layout)
        if output_file:
            plot(fig, filename=output_file)
        return fig

    @property
    def node_names(self):
        return list(zip(*self.nodes))[0]

    def summary(self, output_file=None):
        lines = []
        for node, pf in zip(self.nodes, self.placed_files):
            for file in pf:
                lines.append('{} {}'.format(file[0], node[0]))
        lines.extend(['{} NULL'.format(file[0]) for file in self.null_files])
        text = '\n'.join(lines)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(text)
        else:
            print(text)
        return text


# Helper methods for parsing files
def parse_string(string):
    """Parses file into titles and values"""
    lines = [line for line in string.split('\n') if not line.startswith("#")]
    pairs = [parse_line(line) for line in lines]
    return pairs

def parse_line(line):
    """Parses individual lines and throws an error if bad line is encountered"""
    try:
        name, value = line.split(' ')
        return name, float(value)
    except:
        raise ValueError("Badly formatted line: {}. "
                         "Please format lines as 'NAME' 'VALUE'".format(line))
