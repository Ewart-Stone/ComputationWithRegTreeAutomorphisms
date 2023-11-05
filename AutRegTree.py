#This class implements the approximation automorphism for a regular tree
#as a decorated tree structure using the AutEdge and AutNode sublasses
#Methods of operations performbable with the AutRegTree are also implemented
#Developed by Ewart Stone

import random
import json
from AutNode import AutNode
from AutEdge import AutEdge

class AutRegTree:

    def __init__(self):

        #List to store nodes
        self.nodes = []
        self.edges = []

        #aut reference
        self.reference = (-1, -1)

    def genInitTree(self, radius, degree, center):

        start = 0
        end = 0

        #add origin nodes
        self.nodes.append(AutNode(degree))

        for r in range(radius):
            for d in range(start, end + 1):

                targ = degree - self.nodes[d].edgeNum

                for count in range(0, targ):

                    temp = AutNode(degree)
                    
                    #parse used edges for parent node
                    #and find next unset edge
                    usedEdges = self.nodes[d].getEdges()
                    edgeIndex = 0

                    for edgeIndex in range(len(usedEdges)):
                        if usedEdges[edgeIndex] == None:
                            break

                    #create edge, connect nodes, and add temp to nodes
                    tempEdge = AutEdge([self.nodes[d], temp])

                    self.nodes[d].addEdge(tempEdge, edgeIndex)
                    temp.addEdge(tempEdge, edgeIndex)

                    self.nodes.append(temp)
            
            start = end + 1
            end = len(self.nodes) - 1

        self.assignPaths(center)

    def assignPaths(self, center):
        self.nodes[0].assignPath(center)

    def genRandomAut(self, degree, centerRef = True):

        #gen random node between the bound of tree nodes
        nodeRange = len(self.nodes) - 1

        #get ref node start
        if centerRef:
            startNodeInt = 0
        else:
            startNodeInt = random.randint(0, nodeRange)
        
        startingNode = self.nodes[startNodeInt]
        #startingNode = self.nodes[0]

        #get destination
        destinationNodeInt = random.randint(0, nodeRange)
        destinationNode = self.nodes[destinationNodeInt]
        #destinationNode = self.nodes[0]

        #set tree reference point tuple
        self.reference = (startingNode.path, destinationNode.path)

        startingNode.imagePath = destinationNode.path

        self.randomNodeAssign(startingNode, degree, -1)
        
    def randomNodeAssign(self, nodeInput, degree, lastSetLocal):            

        #get available local actions for the node to set

        destColours = []
        for i in range(degree):
            destColours.append(i)

        if lastSetLocal != -1:
            destColours.pop(nodeInput.localAction[lastSetLocal][1])

        
        #for each neighbour node
            #select next available colour
            #map the neightbour node to that colour

        for i in range(len(nodeInput.localAction)):

            if i != lastSetLocal and nodeInput.localAction[i][0] != -1:
                #select random edge to map to
                destInt = random.randint(0, len(destColours) - 1)

                nextNode = None

                #fetch next node
                for x in nodeInput.edges[i].nodes:
                    if nodeInput != x:
                        nextNode = x

                #assign col in nodeinput and next node

                nodeLocal = (i, destColours[destInt])

                nodeInput.localAction[i] = nodeLocal
                nextNode.localAction[i] = nodeLocal

                #record image path in next node
                imagePath = nodeInput.imagePath.copy()
                backward = False
                if len(imagePath) > 0:

                    #print(imagePath[len(imagePath) - 1])

                    if imagePath[len(imagePath) - 1] == destColours[destInt]:
                        backward = True

                if backward:
                    #step back
                    imagePath.pop(len(imagePath) - 1)
                else:
                    #step forward
                    imagePath.append(destColours[destInt])
            
                nextNode.imagePath = imagePath

                destColours.pop(destInt)

                #call next recursive call
                self.randomNodeAssign(nextNode, degree, i)

    ################################################################################
    #Automorphism Analysis Functions

    def typeCheck(self):

        #establish path
        refPoint = self.reference[0].copy()
        refPointAut = self.reference[1].copy()

        path = self.createPath(refPoint, refPointAut)

        left = 0
        right = len(path) - 1

        startNode = self.getNode(self.reference[0])
        leftNode = startNode

        if(len(path) == 0 or len(path) == 1):
            print("Fixed Automorphism")
            results = self.getFixedPoints(leftNode)

            print("Fixed Nodes: ")
            for each in results:
                print("Node %s" % (each))
            return
        
        #print(path)
        #print("%s  %s" % (left, right))

        while left < right:
            #step left node along path and check local actions support this
            
            #print("node %s" % leftNode.path)
            #print("image %s" % leftNode.imagePath)
            #print("testing %s != %s" % (leftNode.localAction[path[left]][1], path[right]))

            #determine next colour step to take in path
            #leftStep
            if(len(path[left]) < len(path[left + 1])):
                leftStep = path[left + 1][len(path[left + 1]) - 1]
            else:
                leftStep = path[left][len(path[left]) - 1]

            #rightStep
            if(len(path[right]) < len(path[right - 1])):
                rightStep = path[right - 1][len(path[right - 1]) - 1]
            else:
                rightStep = path[right][len(path[right]) - 1]

            #print("left %s right %s" % (leftStep, rightStep))

            #check if local action of left matches right
            if(len(leftNode.localAction) - 1 < leftStep or  leftNode.localAction[leftStep][1] != rightStep):
                print("Translation Automorphism")

                print("Distance: %s" % (right - left))

                if(left != 0):
                    #generate minimal path
                    minPath = []

                    for count in range(left, right + 1):
                        minPath.append(path[count])
                else:
                    minPath = path
                
                #print all along axis of translation using minPath and leftNode
                vertices = self.getTranslationAxisVertices(leftNode, minPath)
                print(vertices)
                return
            
            #if nodes match then continue to next nodes
            leftNode = leftNode.getNode(leftStep)

            left += 1
            right -= 1

        if left > right:
            #reflected along axis
            print("Reflected Automorphism")
            
            print("Axis of reflection: ")
            print("%s, %s" % (path[right], path[left]))


        elif left == right:
            #fixed node
            print("Fixed Automorphism")
            results = self.getFixedPoints(leftNode)

            print("Fixed Nodes: ")
            for each in results:
                print("Node %s" % (each))

    #Fixed Point Aut Analysis
    #preconditions: fixedNode is a reference to a fixedNode in the Aut
    #postconditions: returns an array of the paths of all fixed nodes in the aut
    def getFixedPoints(self, fixedNode):
        
        #for local action at "central" fixed node
            #if assigned and (x, y) where x == y
            #record node as fixed
            #call algorithm on that node
        results = []

        results.append(fixedNode.path)
        
        self.checkFixedPoint(fixedNode, results, -1)

        return results

    #preconditions: fixedNode is fixed, results not null, origin is an int
    #postconditions: recursively populates results with the paths of fixedNodes
    # connected to fixedNode
    def checkFixedPoint(self, fixedNode, results, origin):

        #origin: index of local action traversed to reach fixedNode

        #for local action at fixed node
            #if assigned and (x, y) where x == y
            #record node as fixed
            #call algorithm on that node

        for tuple in fixedNode.localAction:
            if tuple[0] != origin and tuple[0] != -1 and tuple[1] != -1 and tuple[0] == tuple[1]:

                next = fixedNode.getNode(tuple[0])
                results.append(next.path)
                self.checkFixedPoint(next, results, tuple[0])


    #translation aut analysis
    #preconditions: aut is a translation type and path is a subpath of the path of translation
    #postconditions: returns a list of nodes identified by path on the axis of translation
    def getTranslationAxisVertices(self, leftNode, path):

        #left going right
        rightPath = path.copy()
        endOfAxis = False
        currentNode = leftNode
        pathIndex = 0

        while not endOfAxis:
            
            #get next step
            nextStep = self.getNextInSequence(rightPath[pathIndex], rightPath[pathIndex + 1])

            if len(currentNode.localAction) - 1 < nextStep:
                #end of axis as not enough info
                endOfAxis = True
            #check if currentNode has mapping for nextStep
            elif currentNode.localAction[nextStep][1] != -1:
                
                #form next on path and append
                rightPath.append(self.pathFromStep(rightPath[len(rightPath) - 1],
                    currentNode.localAction[nextStep][1]))

                #iterate to next node in path sequence
                currentNode = currentNode.getNode(nextStep)
                pathIndex += 1

            #else end of axis as not enough info
            else: 
                endOfAxis = True


        #right going left
        leftOut = []
        leftPath = path.copy()
        pathIndex = len(leftPath) - 1
        currentNode = leftNode
        endOfAxis = False

        while not endOfAxis:

            nextStep = self.getNextInSequence(leftPath[pathIndex - 1], leftPath[pathIndex])
            laFound = False

            #for each local action find the la corresponding
            #to nextstep under the mapping
            for la in currentNode.localAction:
                if la[1] == nextStep:
                    #target local action found
                    laFound = True

                    currentNode = currentNode.getNode(la[0])

                    leftPath.insert(0, currentNode.path)
                    leftOut.insert(0, currentNode.path)
                    break
        
            if not laFound:
                endOfAxis = True

        leftOut.extend(rightPath)
        return leftOut
    
    #preconditions: origin is a valid int array, step is an integer step
    #postconditions: returns an array that is the result of taking the input step from origin
    def pathFromStep(self, origin, step):

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

    #preconditions: p1 and p2 are arrays of positive integers
    #postconditions: creates a path from p1 to p2 and returns an array result
    def createPath(self, p1, p2):

        if(self.compareList(p1, p2)):
            return [p1.copy()]

        pathPrefix = []
        pathSuffix = []

        pathPrefix.append(p1.copy())
        pathSuffix.append(p2.copy())

        matchingPos = 0

        for count in range(0, len(p1)):

            if count >= len(p2):
                break 

            if p1[count] == p2[count]:
                matchingPos += 1
            else:
                break

        #while path halves have not met
        while p1 != p2:
            #add p1 onto prefix and p2 onto suffix
            #pathPrefix.append(p1)
            #pathSuffix.insert(0, p2)

            #determine if p1 increases or decreases
            if len(p1) > matchingPos:
                #decrease
                #pathPrefix.append(p1[len(p1) - 1])

                pathPrefix.append(pathPrefix[len(pathPrefix) - 1].copy())
                pathPrefix[len(pathPrefix) - 1].pop()
                
                p1.pop(len(p1) - 1)
            else:
                #increases
                #pathPrefix.append(p2[matchingPos])
                pathPrefix.append(pathPrefix[len(pathPrefix) - 1].copy())
                pathPrefix[len(pathPrefix) - 1].append(p2[matchingPos])

                p1.append(p2[matchingPos])

                matchingPos += 1

            if(self.compareList(pathPrefix[len(pathPrefix) - 1], pathSuffix[0])):
                    pathPrefix.pop()

            #check if path is now complete
            if self.compareList(p1, p2):
                #is complete
                #break loop
                break


            #determine if p2 increases or decreases
            if len(p2) > matchingPos:
                #decrease
                #pathSuffix.insert(0, p2[len(p2) - 1])
                pathSuffix.insert(0, pathSuffix[0].copy())
                pathSuffix[0].pop()
                p2.pop(len(p2) - 1)
            else:
                #increases
                #pathSuffix.insert(0, p1[matchingPos])
                pathSuffix.insert(0, pathSuffix[0].copy())
                pathSuffix[0].append(p1[matchingPos])
                p2.append(p1[matchingPos])

                matchingPos += 1

            if(self.compareList(pathPrefix[len(pathPrefix) - 1], pathSuffix[0])):
                pathSuffix.pop(0)

            #check if path is now complete
            if self.compareList(p1, p2):
                #is complete
                break

        pathPrefix.extend(pathSuffix)

        #print(pathPrefix)
        return pathPrefix
    
    #preconditions: l1 and l2 are arrays
    #postconditions: a True False result is returned
    # representing a comparison on the contents of the arrays
    # i.e., contents are equal, in same order, etc.
    def compareList(self, l1, l2):
        if len(l1) != len(l2):
            return False
        
        for i in range(len(l1)):
            if l1[i] != l2[i]:
                return False
            
        return True
    
    #precodntions: nodePath is either None or an array of integers
    # representing a valid path in the tree
    #postconditions: returns the reference to the node at the address nodePath
    def getNode(self, nodePath = None):

        #print(nodePath)

        if nodePath == None:
            return self.nodes[0]
        
        #parse tree and retrieve node
        pos = 0
        current = self.nodes[0]
    
        found = False

        while not found:
            if self.compareList(current.path, nodePath):
                found = True
                break

            #get next step
            nextStep = self.getNextInSequence(current.path, nodePath)

            #print(nodePath)
            #print(current.path)
            #print(nextStep)

            #take step
            current = current.getNode(nextStep)

            if current == None:
                break

        #while pos < len(nodePath):
        #
        #    if current.edges[nodePath[pos]] == None:
        #        return None
        #
        #    current = current.edges[nodePath[pos]].nodes[1]
        #
        #    pos += 1

        return current
    
    def getNextInSequence(self, current, destination):
        #find where matching

        matchingIndex = -1

        shortest = current if len(current) <= len(destination) else destination

        #iterate and find highest matching 
        for count in range(len(shortest)):
            if current[count] == destination[count]:
                matchingIndex += 1

        #if matching == -1 then shortest is the empty string
        if current != shortest or matchingIndex != len(current) - 1:
            return current[len(current) - 1]
        else:
            return destination[matchingIndex + 1]
    
    ################################################################################
    #Mutator Functions
    #
    #Return a third aut resultant of this aut, and the input aut

    #############################
    #Inverse

    def getInverse(self):

        #get reference node
        current = self.getNode(self.reference[0])

        #count degree and radius
        degree = self.findMaxColour(current)

        #init inverse and reverse reference direction
        inverseTree = AutRegTree()

        #create center node
        inverseTree.nodes.append(AutNode(degree))

        inverseTree.reference = (self.reference[1], self.reference[0])
        
        inverse = inverseTree.nodes[0]

        inverse.path = current.imagePath.copy()

        self.inverseNode(current, inverse, -1, inverseTree)

        return inverseTree
    
    def inverseNode(self, thisNode, inverseNode, step, inverseTree):
        
        #for each local action of thisNode
            #set inverse on inverseNode
            #call this method on next node

        inverseNode.imagePath = thisNode.path.copy()

        for tuple in thisNode.localAction:

            if tuple[0] != -1:

                inverseNode.localAction[tuple[1]] = (tuple[1], tuple[0])

                #if step is not already recorded
                if tuple[0] != step:
                    
                    #get next node info
                    next = thisNode.getNode(tuple[0])
                    degree = self.findMaxColour(next)


                    #create connected node in inverse tree
                    temp = AutNode(degree)
                    tempEdge = AutEdge([inverseNode, temp])
                    inverseNode.setEdge(tempEdge, tuple[1])
                    temp.setEdge(tempEdge, tuple[1])

                    inverseTree.nodes.append(temp)

                    #set path
                    temp.path = self.pathFromStep(inverseNode.path, tuple[1])

                    

                    self.inverseNode(next,
                        temp, tuple[0], inverseTree)
                    
    def findMaxColour(self, node):
        max = -1

        for la in node.localAction:
            if la[0] > max:
                max = la[0]
            if la[1] > max:
                max = la[1]

        return max + 1

    #############################
    #Merge

    def merge(self, targetAut):
        
        #return tree of merged if compatible
        #else return null
        out = AutRegTree()

        out.nodes.append(AutNode(0))


        #search for shared node
            #check node is agreed on
            #span out on adjacent shared nodes

        startingTargNode = None
        startingNode = None

        compatible = False
        
        for node in targetAut.nodes:

            if node != None:
                startingNode = self.getNode(node.path)            

                if startingNode != None:
                    #match
                    startingTargNode = node

                    if(self.compatibleNodeCheck(startingNode, startingTargNode)):

                        out.nodes[0].path = startingNode.path.copy()
                        out.nodes[0].imagePath = startingNode.imagePath.copy()

                        out.reference = (out.nodes[0].path.copy(), out.nodes[0].imagePath.copy())

                        compatible = True

                        #iterate through longest local action array
                        #if mapped to -1 then use other list if in range
                        #copy action, add coressponding edge and node to toSearch
                        toSearch = []
                        toAdd = []

                        if len(startingNode.localAction) >= len(startingTargNode.localAction):
                            longer = startingNode
                            shorter = startingTargNode
                        else:
                            longer = startingTargNode
                            shorter = startingNode

                        for count in range(len(longer.localAction)):

                            #0th local action tuple -1 if not assigned

                            if longer.localAction[count][0] == -1 and len(shorter.localAction) > count and shorter.localAction[count][0] != -1:
                                toAdd.append(shorter.getNode(shorter.localAction[count][0]))
                                out.nodes[0].localAction.append((shorter.localAction[count][0], shorter.localAction[count][1]))

                            elif longer.localAction[count][0] != -1:

                                ######
                                if len(shorter.localAction) <= count:
                                    toAdd.append(longer.getNode(count))
                                elif shorter.localAction[count][0] == -1:
                                    toAdd.append(longer.getNode(count))
                                else:
                                    toSearch.append((longer.getNode(count), shorter.getNode(count)))

                                out.nodes[0].localAction.append((count, longer.localAction[count][1]))

                            else:
                                out.nodes[0].localAction.append((-1, -1))

                            out.nodes[0].edges.append(None)

                        #for each in to search
                            #call recursive mergeNode
                        for tuple in toSearch:
                            result = self.mergeSharedNode(out.nodes[0], tuple[0], tuple[1], out)

                            if not result:
                                compatible = False
                                break

                        if compatible:
                            #for each in to add
                                #call recursive mergeAddNode
                            for node in toAdd:
                                self.mergeSingleNode(out.nodes[0], node, out)

                    else:
                        #not compatible
                        pass

                    break

        if not compatible:
            print("Trees are not compatible for merging")
            return None

        return out
    
    def mergeSharedNode(self, prevOutNode, nodeA, nodeB, newTree):

        #record last step
        if len(prevOutNode.path) > len(nodeA.path):
            lastStep = prevOutNode.path[len(prevOutNode.path) - 1]
        else:
            lastStep = nodeA.path[len(nodeA.path) - 1]

        if len(nodeA.localAction) >= len(nodeB.localAction):
            longer = nodeA
            shorter = nodeB
        else:
            longer = nodeB
            shorter = nodeA

        #check nodeA and nodeB are compatible
        if(self.compatibleNodeCheck(nodeA, nodeB)):

            #create new node and edge
            #populate with info
            newNode = AutNode(len(longer.localAction))
            newTree.nodes.append(newNode)

            newNode.path = nodeA.path.copy()
            newNode.imagePath = nodeA.imagePath.copy()

            newEdge = AutEdge([prevOutNode, newNode])

            #connect edge to nodes
            newNode.addEdge(newEdge, lastStep)
            
            #prevOutNode.addEdge(newEdge, lastStep)
            prevOutNode.edges[lastStep] = newEdge
            prevOutNode.edgeNum += 1

            #set local actions
                #iterate through longest local action array
                #if mapped to -1 then use other list if in range
                #copy action, add coressponding edge and node to toSearch
            toSearch = []
            toAdd = []

            for count in range(len(longer.localAction)):

                #if tuple is only in longer action then it can be merged
                if count >= len(shorter.localAction):

                    #if la is defined
                    if longer.localAction[count][0] != -1:
                        if lastStep != count:
                            toAdd.append(longer.getNode(longer.localAction[count][0]))

                        #set local action in new node
                        newNode.localAction[count] = (longer.localAction[count][0], longer.localAction[count][1])

                #0th local action tuple -1 if not assigned
                elif longer.localAction[count][0] == -1 and shorter.localAction[count][0] != -1:
                    
                    if lastStep != count:
                        toAdd.append(shorter.getNode(shorter.localAction[count][0]))

                    newNode.localAction[count] = (shorter.localAction[count][0], shorter.localAction[count][1])

                elif longer.localAction[count][0] != -1:

                    if lastStep != count:
                        if len(shorter.localAction) <= count:
                            toAdd.append(longer.getNode(count))
                        elif shorter.localAction[count][0] == -1:
                            toAdd.append(longer.getNode(count))
                        else:
                            toSearch.append((longer.getNode(count), shorter.getNode(count)))

                    newNode.localAction[count] = (count, longer.localAction[count][1])

                else:
                    #newNode.localAction.append((-1, -1))
                    pass


            #continue recursive call
            #for each in to search
                #call recursive mergeNode
            for tuple in toSearch:
                result = self.mergeSharedNode(newNode, tuple[0], tuple[1], newTree)
                
                #if not compatible
                if not result:
                    return False

            #for each in to add
                #call recursive mergeAddNode
            for node in toAdd:
                self.mergeSingleNode(newNode, node, newTree)

        else:
            #trees are not compatible so merge cannot be completed
            return False
        
        return True

    def mergeSingleNode(self, prevOutNode, node, newTree):

        #record last step
        if len(prevOutNode.path) > len(node.path):
            lastStep = prevOutNode.path[len(prevOutNode.path) - 1]
        else:
            lastStep = node.path[len(node.path) - 1]

        #create new node and edge
        newNode = AutNode(len(node.localAction))
        newTree.nodes.append(newNode)

        newNode.path = node.path.copy()
        newNode.imagePath = node.imagePath.copy()

        newEdge = AutEdge([prevOutNode, newNode])

        #connect edge to nodes
        newNode.addEdge(newEdge, lastStep)
        prevOutNode.edges[lastStep] = newEdge
        prevOutNode.edgeNum += 1

        #set local actions
            #iterate through longest local action array
            #if mapped to -1 then use other list if in range
            #copy action, add coressponding edge and node to toSearch
        toAdd = []

        for count in range(len(node.localAction)):
            if node.localAction[count][0] != -1:
                if count != lastStep:
                    toAdd.append(node.getNode(count))

                #assign tuple
                newNode.localAction[count] = (count, node.localAction[count][1])
            else:
                #newNode.localAction.append((-1, -1))
                pass

        #continue recursive call
        #for each in to add call recursive mergeAddNode
        for node in toAdd:
            self.mergeSingleNode(newNode, node, newTree)

    #preconditions: nodeA and nodeB are two AutNodes
    #postconditions: return true if nodeA and nodeB are compatible
    # in the context of merging and false if incompatible
    # matching path and image, non-conflicting localAction
    def compatibleNodeCheck(self, nodeA, nodeB):
        if not self.compareList(nodeA.path, nodeB.path):
            return False
        
        if not self.compareList(nodeA.imagePath, nodeB.imagePath):
            return False

        for count in range(len(nodeA.localAction)):
            if count > len(nodeB.localAction) - 1:
                break

            if ((nodeA.localAction[count][0] != nodeB.localAction[count][0] or 
                nodeA.localAction[count][1] != nodeB.localAction[count][1]) and 
                nodeB.localAction[count][0] != -1 and nodeA.localAction[count][1] != -1):
                return False

        return True
    
    ###################################
    #composition

    #preconditions: targetAut is a valid AutRegTree
    #postconditions: returns a composed tree of the operation: this composes targetAut
    def compose(self, targetAut):

        composedTree = targetAut.copyTree()
        
        #targetAut.getRadius(), len(targetAut.nodes[0].edges)

        #composedTree.printAut()

        #search for at least one node with it's image in this tree
        startingTargNode = None
        startingNode = None

        for node in targetAut.nodes:

            if node.imagePath != None:
                #print(node.imagePath)

                startingNode = self.getNode(node.imagePath)    

                #startingNode.print()        

                if startingNode != None:
                    #print(startingNode.path)
                    startingTargNode = node
                    break
        
        #if no nodes matching to compose then return null
        if startingTargNode == None:
            return None

        composedTreeNode = composedTree.getNode(startingTargNode.path)

        if startingTargNode != None:
            self.composedNode(startingTargNode, startingNode, composedTreeNode, -1, composedTree)

            refNode = composedTree.getNode(composedTree.reference[0])
            composedTree.reference = (refNode.path.copy(), refNode.imagePath.copy())

        #if no nodes are shared then returned in an empty tree                    
        return composedTree

    #preconditions:
    #postconditions: composes the composedTreeNode from this composes target
    # and recursively does so for the rest of the operation
    def composedNode(self, targetAutNode, currentNode, composedTreeNode, sourceIndex, composedTree):
        
        #print(targetAutNode.path)
        #print(composedTreeNode.path)
        #print(composedTreeNode.imagePath)
        #print(currentNode.imagePath)

        #write image and local action details to composedTreeNode
        composedTreeNode.imagePath = currentNode.imagePath.copy()

        for tuple in targetAutNode.localAction:

            #if tuple has defined local action and is in currentNode range of defined actions
            if tuple[1] != -1 and tuple[1] < len(currentNode.localAction):
                result = currentNode.localAction[tuple[1]][1]

                if result != -1:
                    composedTreeNode.localAction[tuple[0]] = (tuple[0], result)

                    #if tuple was not the source edge to this node
                    if sourceIndex != tuple[0]:

                        #perform composition on nodes corresponding to local action
                        nextTargNode = targetAutNode.getNode(tuple[0])
                        nextComposedNode = composedTreeNode.getNode(tuple[0])
                        nextCurrentNode = currentNode.getNode(tuple[1])

                        #recursive composition
                        self.composedNode(nextTargNode, nextCurrentNode, nextComposedNode, tuple[0], composedTree)

                else:
                    #redefined to -1 value
                    
                    #recursivly record connected nodes from tree
                    output = []
                    composedTree.addNodeToList(tuple[0], composedTreeNode.getNode(tuple[0]), output)

                    #remove recorded nodes
                    for node in output:
                        composedTree.nodes.remove(node)

                    #remove connection to nodes
                    composedTreeNode.localAction[tuple[0]] = (-1, -1)
                    composedTreeNode.edges[tuple[0]] = None
                    composedTreeNode.edgeNum -= 1



            elif tuple[1] != -1:
                #not defined in composer therefore remove
                    
                #recursivly record connected nodes from tree
                output = []
                self.addNodeToList(tuple[0], composedTreeNode.getNode(tuple[0]), output)

                #remove recorded nodes
                for node in output:
                    self.nodes.remove(node)

                #remove connection to nodes
                composedTreeNode.localAction[tuple[0]] = (-1, -1)
                composedTreeNode.edges[tuple[0]] = None
                composedTreeNode.edgeNum -= 1
                
    def addNodeToList(self, source, currentNode, output):
        output.append(currentNode)

        for la in currentNode.localAction:
            if la[0] != -1 and la[0] != source:
                self.addNodeToList(la[0], currentNode.getNode(la[0]), output)

    def copyTree(self):
        out = AutRegTree()

        firstNode = self.nodes[0]

        out.reference = (self.reference[0].copy(), self.reference[1].copy())

        copy = AutNode()

        out.nodes.append(copy)

        copy.path = firstNode.path.copy()
        copy.imagePath = firstNode.imagePath.copy()

        for la in firstNode.localAction:
            copy.localAction.append((la[0], la[1]))
            copy.edges.append(None)

            self.copyNode(out, copy, firstNode.getNode(la[0]), la[0])

        return out

    def copyNode(self, copyTree, prevCopyNode, targetNode, step):

        copyNode = AutNode()
        copyTree.nodes.append(copyNode)

        copyNode.path = targetNode.path.copy()
        copyNode.imagePath = targetNode.imagePath.copy()

        for la in targetNode.localAction:
            copyNode.localAction.append((la[0], la[1]))
            copyNode.edges.append(None)

            if la[0] == step:
                #add edge
                newEdge = AutEdge([prevCopyNode, copyNode])
                prevCopyNode.setEdge(newEdge, step)

                copyNode.setEdge(newEdge, step)
            elif la[0] != -1:
                self.copyNode(copyTree, copyNode, targetNode.getNode(la[0]), la[0])    
            
        



    ################################################################################
    #Output functiones

    #output to console
    def printAut(self):
        print("\nRef ", self.reference)

        for count in range(len(self.nodes)):
            print("Node ", count)
            print("Path ", self.nodes[count].path)
            print("Image Path ", self.nodes[count].imagePath)
            print("Local Action ", self.nodes[count].localAction)

    #preconditions: self is a "complete" finite subsection of a tree aut
    #i.e., consistent number of neighbours for each node except leaves
    #save to json file as specified folder path with filename
    def saveToJsonFile(self, filepath = "", fileName = "defaultAutFileName"):

        print("Warning: This function is only guaranteed to work with automorphisms \n generated with the random construction procedure.")

        degree = len(self.nodes[0].edges)

        jsonDict = {
            "degree": degree,
            "reference": self.reference
        }

        #count radius
        numberOfNodes = len(self.nodes)

        #start at 1 radius measurement
        total = degree + 1
        c = degree
        radius = 1
        while(total != numberOfNodes):
            c = c * (degree - 1)
            total += c
            radius += 1

        #store local action set in list for dict
        imageSet = []
        localActionSet = []

        for count in range(len(self.nodes)):
            imageSet.append(self.nodes[count].imagePath)
            localActionSet.append(self.nodes[count].localAction)

        #add calculated values to dict
        jsonDict["center"] = self.nodes[0].path.copy()
        jsonDict["radius"] = radius
        jsonDict["localActions"] = localActionSet
        jsonDict["images"] = imageSet

        #write to file
        targetFP = ""
        if(filepath != ""):
            targetFP += filepath
            targetFP += "/"

        targetFP += fileName + ".json"

        with open(targetFP, "w") as outfile:
            json.dump(jsonDict, outfile)

    def initFromFile(self, filePath):
        with open(filePath, "r") as openFile:
            jsonObj = json.load(openFile)

        self.reference = (jsonObj["reference"][0], jsonObj["reference"][1])

        self.genInitTree(jsonObj["radius"], jsonObj["degree"], jsonObj["center"])

        images = jsonObj["images"]
        localActions = jsonObj["localActions"]

        for count in range(len(self.nodes)):
            self.nodes[count].localAction = localActions[count]
            self.nodes[count].imagePath = images[count]

    def loadFromFile(self, filePath):
        self.nodes = []
        self.edges = []

        self.initFromFile(filePath)