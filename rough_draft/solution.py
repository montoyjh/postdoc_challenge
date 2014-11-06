from distributor import Distributor

dist = Distributor('files.txt','nodes.txt')
dist.distribute()
print dist.assignments
