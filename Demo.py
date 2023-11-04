import AutConstructor
from AutRegTree import AutRegTree

import time

def main():
    #Example random generation
    degree = 3
    radius = 2
    center = []
    centerRef = True

    a = AutConstructor.constructRandom(degree, radius, center, centerRef)

    #example print
    a.printAut()

    print("\n")

    #example type check call
    a.typeCheck()

    #saving and loading procedure
    #filePath="C://someFolder" is optional
    a.saveToJsonFile(fileName="test")

    b = AutConstructor.loadFromFile("test.json")

    #example composition call
    a.compose(b)

    #example inverse call
    c = a.getInverse()

    #example merge
    d = a.merge(b)

    #example guided construction
    #e = AutConstructor.constructGuided()

if __name__ == '__main__':
    main()