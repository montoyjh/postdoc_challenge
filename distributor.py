# Author: J. H. Montoya - montoyjh@gmail.com
import sys

class Distributor:
    '''Distributor class, initializes with filenames corresponding
    to node and file lists.  Includes methods for parsing files,
    sorting nodes by both used capacity and total size, distributing
    files among nodes, summarizing the results, and plotting 
    the resulting distribution.'''
    def __init__(self,files_filename,nodes_filename):
        self.files = self.parse_filenfile(files_filename)
        self.nodes = self.parse_nodefile(nodes_filename)
        self.sort_all_by_size()
        self.files_unassigned = self.files[:]

    def parse_filenfile(self,filename):
        '''Returns a list of filens from a text file
        with filename'''
        f = open(filename)
        lines = f.read().split('\n')
        f.close()
        filen_list = []
        for n,line in enumerate(lines):
            # Handle cases in parsing
            if line=='': # empty line, ignore line
                continue
            elif line[0]=='#': # Comment line starting with hash, ignore line
                continue
            elif ' ' not in line: # No space in line
                print 'Format error in line '+str(n)+\
                      ' of '+filename+': no space in line'
                print 'Line '+str(n)+' reads: '+'\''.join(['',line,''])
                print 'Line must be formatted as \'FILENAME SIZE\''
                sys.exit(0)
            elif not line.split()[1].isdigit(): # size is not an integer
                print 'Format error in line '+str(n)+\
                      ' of '+filename+': file size not integer'
                print 'Line '+str(n)+' reads: '+'\''.join(['',line,''])
                print 'Line must be formatted as \'FILENAME SIZE\''
                sys.exit(0)
            else:
                # Try/catch for other errors
                try:
                    filen_list += [Filen(name = line.split()[0],
                                     size = int(line.split()[1]))]
                except:
                    print 'Error parsing line '+str(n)+' of '+filename
                    print 'Line must be formatted as \'FILENAME SIZE\''
                    sys.exit(0)

        return filen_list
    
    def parse_nodefile(self,filename):
        '''Returns a list of node objects from a text file
        with filename'''
        f = open(filename)
        lines = f.read().split('\n')
        f.close()
        node_list = []
        for n,line in enumerate(lines):
            # Handle cases in parsing
            if line=='':
                continue
            if line[0]=='#': # Comment line starting with hash, ignore line
                continue
            elif ' ' not in line: # No space in line
                print 'Format error in line '+str(n)+\
                      ' of '+filename+': no space in line'
                print 'Line '+str(n)+' reads:'+line
                sys.exit(0)
            elif not line.split()[1].isdigit(): # size is not an integer
                print 'Format error in line '+str(n)+\
                      ' of '+filename+': file size not integer'
                print 'Line '+str(n)+' reads:'+line
                sys.exit(0)
            else:
                node_list += [Node(name = line.split()[0],
                                     size = int(line.split()[1]))]
        return node_list


    def sort_all_by_size(self):
        '''sorts the files_data and nodes_data lists in place'''
        self.files.sort(key=lambda x: x.size)
        self.nodes.sort(key=lambda x: x.size)

    def sort_nodes_by_used_capacity(self):
        '''sorts nodes first by fullness, then by size'''
        self.nodes.sort(key=lambda x: (x.used_capacity,x.size))
    
    def pack_last_file(self):
        '''This packing algorithm takes the largest unassigned 
        file, and places it into the largest least full node 
        that it can fit into.  If it is unable to pack, assigns
        file to NULL location'''
        luf = self.files_unassigned[-1] # largest unassigned file
        self.sort_nodes_by_used_capacity()
        j = 0 
        llfn_thatfits = False
        # Iteratively check whether the three criteria are met
        while not llfn_thatfits:
            if j==len(self.nodes)-1:
                if luf.size < self.nodes[j].remaining_capacity:
                    self.nodes[j].add_file(luf)
                    self.files_unassigned.pop()
                else:
                    luf.location='NULL'
                    self.files_unassigned.pop()
                llfn_thatfits = True
            elif (self.nodes[j].size >= self.nodes[j-1].size or j==0) and \
                 self.nodes[j].used_capacity <= self.nodes[j+1].used_capacity and \
                 luf.size < self.nodes[j].remaining_capacity:
                self.nodes[j].add_file(luf)
                self.files_unassigned.pop()
                llfn_thatfits = True
            else:
                j+=1

    def distribute(self):
        '''method iteratively packs unassigned files
        until 0 remaining, then stops'''
        while len(self.files_unassigned) != 0:
            self.pack_last_file()

    def summary(self):
        '''prints summary of file locations, as per
        problem statement'''
        self.files.sort(key = lambda x: (x.location,x.size))
        col1 = 1+max([len(filen.name) for filen in self.files]+[8])
        col2 = 1+max([len(filen.location) for filen in self.files]+[8])
        col3 = 1+max([len(str(filen.size)) for filen in self.files]+[4])
        # heading
        border = ''.join(['-' for n in range(col1+col2+col3+7)])
        print border  
        print '| '.join(['','FILENAME'.ljust(col1),
                         'LOCATION'.ljust(col2),
                         'SIZE'.ljust(col3),''])
        print border
        # filenames/locations
        for filen in self.files:
            print '| '.join(['',filen.name.ljust(col1),
                            filen.location.ljust(col2),
                            str(filen.size).ljust(col3),''])
        print border
        
    def plot(self,filename='out.png'):
        from matplotlib import pyplot as plt
        for m,node in enumerate(self.nodes):
            plt.bar(m,node.size,color='w')
            bottom = 0.0
            for filen in node.contained_files:
                plt.bar(m,filen.size,bottom=bottom)
                bottom += filen.size
        plt.xticks([0.4+m for m in range(len(self.nodes))],
                   [node.name for node in self.nodes])
        plt.show()

class Node:
    '''node class for distributor module, an object that has a size,
    a list of contained files, a remaining capacity'''
    def __init__(self,name,size):
        self.name=name # Node name
        self.size=size # Node total capacity
        self.used_capacity = 0 # Used capacity of the node, initialized to 0
        self.remaining_capacity = self.size # Remaining capacity
        self.contained_files = [] # list of filen objects on node
        self.update_capacity()

    def update_capacity(self):
        '''method that updates the capacity according to the filelist'''
        for filen in self.contained_files:
            filen.location = self.name
        self.used_capacity = sum([f.size for f in self.contained_files])
        self.remaining_capacity = self.size - self.used_capacity
        if self.remaining_capacity < 0:
            raise ValueError('node ' + self.name + ' exceeds capacity')

    def add_file(self,new_file):
        '''method that adds a new file to the node and updates capacity'''
        self.contained_files += [new_file] # append new file
        #sys.exit(0)
        #print 'adding '+new_file.name+' to '+self.name
        self.update_capacity()
        #self.report()

    def report(self):
        print 'Node:'+self.name+','+str(self.size)
        print 'Node contents:'
        for f in self.contained_files:
            print f.name+', '+str(f.size)
        print 'Capacity:'+str(self.used_capacity)

class Filen:
    '''filen class for distributor, has a size, a name, 
    and a location (i. e. a node on which it is located)'''
    def __init__(self,name,size,location='unassigned'):
        self.name = name
        self.size = size
        self.location = location # Location of file
