# Author: J. H. Montoya
import sys
from filen import Filen
from node import Node

class Distributor:
    def __init__(self,files_filename,nodes_filename):
        self.files = self.parse_filenfile(files_filename)
        self.nodes = self.parse_nodefile(nodes_filename)
        self.sort_all_by_size()
        self.files_unassigned = self.files[:]
        self.assignments = {}

    def parse_filenfile(self,filename):
        '''Returns a list of filen objects from a text file
        with filename'''
        f = open(filename)
        lines = f.read().split('\n')
        f.close()
        filen_list = []
        for n,line in enumerate(lines):
            # Handle cases in parsing
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
                filen_list += [Filen(name = line.split()[0],
                                     size = int(line.split()[1]))]
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
        luf = self.files_unassigned[-1] # largest unassigned file
        self.sort_nodes_by_used_capacity()
        j = 0 
        llfn_thatfits = False
        while not llfn_thatfits:
            if j==len(self.nodes)-1:
                if luf.size < self.nodes[j].remaining_capacity:
                    #luf.location = self.nodes[j].name
                    self.nodes[j].add_file(luf)
                    self.files_unassigned.pop()
                else:
                    luf.location='NULL'
                    self.files_unassigned.pop()
                llfn_thatfits = True
            elif (self.nodes[j].size >= self.nodes[j-1].size or j==0) and \
                 self.nodes[j].used_capacity <= self.nodes[j+1].used_capacity and \
                 luf.size < self.nodes[j].remaining_capacity:
                #luf.location = self.nodes[j].name
                self.nodes[j].add_file(luf)
                self.files_unassigned.pop()
                llfn_thatfits = True
            else:
                j+=1

    def distribute_iteratively(self):
        while len(self.files_unassigned) != 0:
            self.pack_last_file()
    
    def plot(self,filename='out.png'):
        from matplotlib import pyplot as plt
        for m,node in enumerate(self.nodes):
            plt.bar(m,node.size,color='w')
            bottom = 0.0
            for filen in node.contained_files:
                plt.bar(m,filen.size,bottom=bottom)
                bottom += filen.size
        plt.show()
            

