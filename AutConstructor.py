#
#
#
#

from AutRegTree import AutRegTree

from AutNode import AutNode
from AutEdge import AutEdge


def constructGuided():
    #get reference input
    #mark as center
    v1Str = input("Enter v1 in format x0,x1,x2,x3,x4 \n")
    v2Str = input("Enter v2 in format x0,x1,x2,x3,x4 \n")

    if v1Str == "":
        v1 = []
    else:
        v1 = list(map(int, v1Str.split(",")))

    if v2Str == "":
        v2 = []
    else:
        v2 = list(map(int, v2Str.split(",")))

    aut = AutRegTree()

    aut.reference = (v1.copy(), v2.copy())

    aut.nodes.append(AutNode(0))
    aut.nodes[0].path = v1.copy()
    aut.nodes[0].imagePath = v2.copy()

    finished = False
    selectedNode = None

    nextStepInput = input("Select Node (s), Finish (f)")

    if nextStepInput == "f" or nextStepInput == "F":
        finished = True

    #while not finished
        #take input node

        #take input on 0 to many localAction on Node
    while not finished:

        while selectedNode == None:

            #current nodes print
            print("-- Nodes in Aut --")
            for node in aut.nodes:
                print(node.path)

            #add validation
            selectInputStr = input("Enter a node in format x0,x1,x2,x3,x4 \n")

            if selectInputStr == "":
                selectInput = []
            else:
                selectInput = list(map(int, selectInputStr.split(",")))

            selectedNode = aut.getNode(selectInput)

            if selectedNode == None:
                print("Error: The selected node does not exist\n")

        finishedLaInput = False
        la = (0,0)

        while not finishedLaInput:
            #print node
            print("\n-- Current Node --")
            selectedNode.print()

            #take local action inpit
            #assumes you aren't modifying an existing tuple
            laInput = int(input("Enter the local action colour to add (integer): "))

            laImageInput = int(input("Enter the image for the colour (integer): "))

            la = (laInput, laImageInput)

            #check validity of input
            if validateLocalAction(selectedNode.localAction, la):
                finishedLaInput = True
            else:
                print("Error: The local action tuple clashes with an existing assignment")

        while len(selectedNode.localAction) - 1 < la[0]:
            selectedNode.localAction.append((-1, -1))
            selectedNode.edges.append(None)

        #set local action in this node and create next node connected
        selectedNode.localAction[la[0]] = (la[0], la[1])

        newNode = AutNode(la[0] + 1)
        aut.nodes.append(newNode)
        newEdge = AutEdge([selectedNode, newNode])

        newNodePath = pathFromStep(selectedNode.path, la[0])
        newNodeImagePath = pathFromStep(selectedNode.imagePath, la[1])

        newNode.path = newNodePath
        newNode.imagePath = newNodeImagePath

        #set la of new ndoe
        newNode.localAction[la[0]] = (la[0], la[1])

        #connect via edge
        selectedNode.setEdge(newEdge, la[0])
        newNode.setEdge(newEdge, la[0])

        nextStep = input("Add tuple (a), Select a new Node (s), Finish tree (f) ")

        print("\n")

        if nextStep == "f" or nextStep == "F":
            break
        elif nextStep == "s" or nextStep == "S":
            selectedNode = None
        
    return aut

def validateLocalAction(localAction, localActionTuple):
    for la in localAction:
        if ((la[0] == localActionTuple[0] or la[1] == localActionTuple[1])
            and la[0] != -1 and la[1] != -1):
            return False
        
    return True


def constructRandom(degree, radius, centre = [], centreRef = True):\

    if degree < 0 or radius < 0:
        return None

    aut = AutRegTree()

    aut.genInitTree(radius, degree, centre)
    aut.genRandomAut(degree, centreRef)

    return aut

#preconditions: the localAction array corresponds to a "complete" automorphism subsection
#i.e., consistent number of neighbours for each node except leaves 
#ref[0] describes the path for the center node
#in form shell 0 nodes ..., shell 1 nodes ...., .... , shell n nodes
#def constructFromParams(ref = ([], []), localActions = []):
#    aut = AutRegTree()

#    aut.reference = (ref[0], ref[1])

#    degree = len(localActions[0])
#    radius = (int)(len(localActions) / degree)

#    aut.genInitTree(degree, radius, ref[0])

    #for each local action
    #create corresponding node
    #connect to prev w/ edge
    #set local actions

#    for count in range(len(aut.nodes)):
#            aut.nodes[count].localAction = localActions[count]
            
            #aut.nodes[count].imagePath = images[count]
            #figure out image path for node
    


def loadFromFile(filepath):

    aut = AutRegTree()
    aut.loadFromFile(filepath)
    
    return aut


#preconditions: origin is a valid int array, step is an integer step
#postconditions: returns an array that is the result of taking the input step from origin
def pathFromStep(origin, step):

    if len(origin) - 1 < 0:
        out = origin.copy()
        out.append(step)
        return out

    if origin[len(origin) - 1] == step:
        out = origin.copy()
        out.pop()
        return out
    else:
        out = origin.copy()
        out.append(step)
        return out