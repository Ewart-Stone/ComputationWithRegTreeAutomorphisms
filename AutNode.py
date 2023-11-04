#
#
#
#

from AutEdge import AutEdge

class AutNode:

    def __init__(self, degree = 0):

        #array of tuples of len d
        self.localAction = []
        self.edges = []
        self.edgeNum = 0

        self.path = None
        self.imagePath = None

        for x in range(degree):
            self.edges.append(None)
            self.localAction.append((-1, -1))

    def addEdge(self, edge, col):
        #add edge
        self.edges[col] = edge
        self.edgeNum += 1

        #record possible local action for that edge
        self.localAction[col] = (col, -1)

    def setEdge(self, edge, col):
        self.edges[col] = edge
        self.edgeNum += 1

    def getNode(self, index):
        if(self.edges[index].nodes[0].path != self.path):
            return self.edges[index].nodes[0]
        else:
            return self.edges[index].nodes[1]


    def getEdges(self):
        return self.edges

    #edges are organised such that index of edge 0
    #holds the edge responsible for local action (0, x)
    def getEdge(self, index):
        return self.edges[index]
    
    def print(self):
        print("---Node---")
        print("Path: ")
        print(self.path)
        print("Image: ")
        print(self.imagePath)

        print("-Local Action-")
        for la in self.localAction:
            print(la)
    
    def assignPath(self, path):

        self.path = path.copy()

        for x in self.localAction:
            if(x[0] != -1):
                
                pathCpy = path.copy()

                if len(pathCpy) > 0:

                    if pathCpy[len(pathCpy) - 1] == x[0]:
                        pathCpy.pop()
                    else:
                        pathCpy.append(x[0])
                else:
                    pathCpy.append(x[0])

                if len(path) == 0:
                    self.edges[x[0]].getNode(1).assignPath(pathCpy)
                elif(x[0] != path[len(path) - 1]):
                    self.edges[x[0]].getNode(1).assignPath(pathCpy)
    
