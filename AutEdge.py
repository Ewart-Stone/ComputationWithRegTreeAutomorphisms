#This class provides a skeleton container class for nodes
#in an automorphism of a regular tree
#the node closer to the origin is placed within index 0
#and conversely in index 1 for the opposite case.
#Developed by Ewart Stone

class AutEdge:

    def __init__(self, nodes):
        #array of nodes connected by the edge
            #index 0 closer to origin (node of empty string)
            #index 1 further from origin
        if len(nodes[0].path) < len(nodes[1].path):
            self.nodes = nodes
        else:
            self.nodes = [nodes[1], nodes[0]]
    
    #returns each node
    def getNodes(self):
        return self.nodes
    
    #returns the node at the given index
    #0 for closer to origin
    #1 for further from origin
    def getNode(self, index):
        return self.nodes[index]