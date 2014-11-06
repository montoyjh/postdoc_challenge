# Author: J. H. Montoya
import sys

class Distributor:
    def __init__(self,files_filename,nodes_filename):
        self.files_data=self.parse_file(files_filename)
        self.nodes_data=self.parse_file(nodes_filename)
        # Since nodes are empty at init, also sorted by fullness
        self.sort_all_by_size()
        self.files_unassigned = self.files_data[:]
        self.assignments = {}

    def parse_file(self,filename):
        '''Returns a list of [filename,size] lists, 
        ignores lines starting with #,
        prints error'''
        f = open(filename)
        lines = f.read().split('\n')
        f.close()
        parsed_list = []
        for n,line in enumerate(lines):
            # More elegant error handling to be added
            if ' ' not in line:
                # Format error
                sys.exit(0)
            elif line[0]=='#':
                continue
            elif not line.split()[1].isdigit():
                print 'warning: Non-integer size error'
                continue
            else:
                parsed_list.append([line.split()[0], # name
                                    int(line.split()[1]), # size
                                    0 # fullness initialized to zero
                                    ])
        # go ahead and sort by size
        # parsed_list.sort(key = lambda x: x[1])
        return parsed_list

    def sort_all_by_size(self):
        '''sorts the files_data and nodes_data lists in place'''
        self.files_data.sort(key=lambda x: x[1])
        self.nodes_data.sort(key=lambda x: x[1])

    def sort_nodes_by_fullness(self):
        '''sorts nodes first by fullness, then by size'''
        self.nodes_data.sort(key=lambda x: (x[2],x[1]))
    
    def place_file_in_llfn_that_fits(self,n=0):
        '''Place the largest file into the largest 
        least full node that can fit object
        If I fits, I sits.  -Anonymous cat'''
        if n==len(self.nodes_data)-1:
            self.assignments[self.files_unassigned[-1][0]]='NULL'
            self.files_unassigned.pop()
        else:
            # Walk forward along node list
            while self.nodes_data[n][2]==self.nodes_data[n+1][2]:
                n += 1
                if n==len(self.nodes_data)-1:
                    break
            if self.files_unassigned[-1][1] < \
                        self.nodes_data[n][1] - self.nodes_data[n][2]:
                self.assignments[self.files_unassigned[-1][0]] = self.nodes_data[n][0]
                self.nodes_data[n][2] = \
                        self.nodes_data[n][2]+self.files_unassigned[-1][1]
                self.files_unassigned.pop()
            else:
                self.place_file_in_llfn_that_fits(n=n)
            self.sort_nodes_by_fullness()

    def distribute(self):
        '''Packs files into nodes recursively'''
        if len(self.files_unassigned)==0:
            return
        else:
            self.place_file_in_llfn_that_fits()
            self.distribute()
    
    def plot(self,filename='out.png'):
        from matplotlib import pyplot as plt
        node_dict = {}
        for m,node in enumerate(self.nodes_data):
            plt.bar(m,node[1])
            node_dict[node[0]] = [m,0.0]
        #print node_dict
        for m,filename in enumerate(self.files_data):
            if not self.assignments[filename[0]]=='NULL':
                plt.bar(node_dict[self.assignments[filename[0]]][0],
                        filename[1],
                        bottom=node_dict[self.assignments[filename[0]]][1])
                node_dict[self.assignments[filename[0]]][1] += filename[1]
        plt.show()
            

