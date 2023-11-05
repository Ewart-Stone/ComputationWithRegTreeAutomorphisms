# Computing with Automorphisms of regular trees

## About this library
This project contains the source code for a python library
to handle basic construction and computation using the automorphisms
of infinite regular trees.

## Example Code
> Example code is provided on the Github repository at:
> 
> https://github.com/Ewart-Stone/ComputationWithRegTreeAutomorphisms

> Demo.py shows example usages of functions intended to be used 
by external code
>
> Additional functions for retrieving individual nodes and 
printing node information are also present within AutRegTree objects

## Useful Functions

### AutConstructor
> AutConstructor.constructRandom(int degree, int radius, int[] centre, bool centreRef)

> AutConstructor.constructGuided()

> AutConstructor.loadFromFile(string filePath)

### AutRegTree Class

> typeCheck()

> getInverse() 

> merge(AutRegTree target)

> compose(AutRegTree target) -- this composes target order

> saveToJsonFile(string filePath, string fileName)
-- only works with automorphisms constructed via constructRandom()

> getNode(int[] path) -- returns node of given path or type None if not exists

> copyTree() -- returns a new AutRegTree with the same data as this tree

> printAut()

### AutNode Class

> getNode(int index) -- returns the neighbour node corresponded to by the index 
representing the local action or None type if not defined

> print() -- prints the node and all of it's information
