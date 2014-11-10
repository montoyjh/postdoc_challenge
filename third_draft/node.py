# Node class file

class Node:
    '''node class for distributor, an object that has a size,
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
