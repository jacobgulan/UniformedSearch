# Jacob Gulan
import time

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:20:27 2020

@author: jpgul
"""
# https://docs.python.org/3/library/queue.html


# The grid values must be separated by spaces, e.g.
# 1 1 1 1 1
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
# Returns a 2D list of 1s and 0s
def readGrid(filename):
    #print('In readGrid')
    grid = []
    with open(filename) as f:
        for l in f.readlines():
            grid.append([int(x) for x in l.split()])
   
    f.close()
    #print 'Exiting readGrid'
    return grid
 
 
# Writes a 2D list of 1s and 0s with spaces in between each character
# 1 1 1 1 1
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
def outputGrid(grid, start, goal, path):
    #print('In outputGrid')
    filenameStr = 'pathInt.txt'
 
    # Open filename
    f = open(filenameStr, 'w')
 
    # Mark the start and goal points
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'
 
    # Mark intermediate points with *
    for i, p in enumerate(path):
        if i > 0 and i < len(path)-1:
            grid[p[0]][p[1]] = '*'
 
    # Write the grid to a file
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
           
            # Don't add a ' ' at the end of a line
            if c < len(row)-1:
                f.write(str(col)+' ')
            else:
                f.write(str(col))
 
        # Don't add a '\n' after the last line
        if r < len(grid)-1:
            f.write("\n")
 
    # Close file
    f.close()
    #print('Exiting outputGrid')
    

#######################################################
#                  MY CODE HERE                       #
#######################################################

def main():
    search = input("Input BFS or DFS: ")
    startx = int(input("Input initial x: "))
    starty = int(input("Input initial y: "))
    goalx = int(input("Input goal x: "))
    goaly = int(input("Input goal y: "))
    grid = readGrid('GridInt.txt') # Filename goes here
    start = Node((starty,startx), None)
    goal = Node((goaly,goalx), None)
    print(uninformedSearch(grid, start, goal, search))


class Node:
  def __init__(self, v, p):
    self.value = v
    self.parent = p

  def getValue(self):
    return self.value
  
  def getParent(self):
    return self.parent


def uninformedSearch(grid, start, goal, search):
    current = start
    openList = []
    closedList = []
    
    sx = start.getValue()[0]
    sy = start.getValue()[1]
    gx = goal.getValue()[0]
    gy = goal.getValue()[1]
    
    if (grid[sx][sy] == 1):
        return "Error! Initial state in blocked location."
    if (grid[gx][gy] == 1):
        return "Error! Goal state in blocked location."
        
    openList = expandNode(current, grid, closedList, openList)
    
    # Breadth First Traversal
    if (search == 'BFS'):
        while(True):
            if not openList:
                return "Failed to find path using BFS."
            current = openList.pop(0)
            if (current.getValue() == goal.getValue()):
                path = []
                path = setPath(current, path)
                outputGrid(grid, list(start.getValue()), list(goal.getValue()), path)
                return "Success"
            closedList.append(current)
            openList = expandNode(current, grid, closedList, openList)

        
    # Depth First Traversal
    if (search == 'DFS'):
        while(True):
            if not openList:
                return "Failed to find path using DFS."
            current = openList.pop()
            if (current.getValue() == goal.getValue()):
                path = []
                path = setPath(current, path)
                outputGrid(grid, list(start.getValue()), list(goal.getValue()), path)
                return "Success"
            closedList.append(current)
            openList = expandNode(current, grid, closedList, openList)

        

# getNeighbors takes in a location and a grid and returns a list of Nodes
# that will be processed by the expandNode function
def getNeighbors(location, grid):
  x = location.getValue()[0]
  y = location.getValue()[1]
  newNode = Node
  movementList = []
  
  
  # Checks space above position
  if(grid[x][y-1] == 0):
    newNode = Node((x,y-1), location)
    movementList.append(newNode)
  
  
  
  
  # Checks space left of position
  if(grid[x-1][y] == 0):
    newNode = Node((x-1,y), location)
    movementList.append(newNode)
  
  # Checks space right of position
  if(grid[x+1][y] == 0):
    newNode = Node((x+1,y), location)
    movementList.append(newNode)
    
    # Checks space below position
  if(grid[x][y+1] == 0):
    newNode = Node((x,y+1), location)
    movementList.append(newNode)


  return movementList


# Adds only the nodes that contain 0s from the getNeighbors function to
# the openList
def expandNode(node, grid, closedList, openList):
    neighbors = []
    neighbors = getNeighbors(node, grid)
    
    for neighbor in neighbors:
        inClosed = False
        inOpen = False

        for closedNode in closedList:
            if neighbor.getValue() == closedNode.getValue():
                inClosed = True

        for openNode in openList:
            if neighbor.getValue() == openNode.getValue():
                inOpen = True
            
        if not inClosed and not inOpen:
            openList.append(neighbor)
    
    return openList


def setPath(current, path):
    while(current.getParent() != None):
        path.append(list(current.getValue()))
        current = current.getParent()
    path.append(list(current.getValue()))
    return path

main()