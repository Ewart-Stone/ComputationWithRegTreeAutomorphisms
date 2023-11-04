#
#
#
#

class AutEdge:

    def __init__(self, nodes):
        #array of nodes connected by the edge
            #index 0 closer to origin
            #index 1 further from origin
        self.nodes = nodes
    
    def getNodes(self):
        return self.nodes
    
    def getNode(self, index):
        return self.nodes[index]