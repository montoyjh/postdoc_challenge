# Node filen file

class Filen:
    '''filen class for distributor, an object that has a size,
    a name, and a location'''
    def __init__(self,name,size,location='unassigned'):
        self.name = name
        self.size = size
        self.location = location # Location of file
