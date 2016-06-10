# layout.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from grid import Grid
import os
import random

class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height= len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.start = None
        self.goal = None
        self.position = None 
        self.processLayoutText(layoutText)
        self.layoutText = layoutText

    def isWall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def isGoal(self, pos):
        return self.goal == pos

    def getLegalPositions(self):
        x, y = self.position
        legal = [] 
        # Check up, down, left, right squares - No diagonal moves
        if not self.isWall((x, y+1)): legal.append((x, y+1))
        if not self.isWall((x, y-1)): legal.append((x, y-1))
        if not self.isWall((x+1, y)): legal.append((x+1, y))
        if not self.isWall((x-1, y)): legal.append((x-1, y))

        return legal

    def getRandomLegalPosition(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        while self.isWall( (x, y) ):
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))
        return (x,y)

    def __str__(self):
        return "\n".join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:])

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         % - Wall
         S - Start
         G - Goal
         P - Current Position 
        Other characters are ignored.
        """
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == 'S':
            self.start = (x, y)
            self.position = (x, y)
        elif layoutChar == 'E':
            self.end = (x,y)

def getLayout(name, back = 2):
    if name.endswith('.lay'):
        layout = tryToLoad('search/layouts/' + name)
        if layout == None: layout = tryToLoad(name)
    else:
        layout = tryToLoad('search/layouts/' + name + '.lay')
        if layout == None: layout = tryToLoad(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back -1)
        os.chdir(curdir)
    return layout

def tryToLoad(fullname):
    if(not os.path.exists(fullname)): return None
    f = open(fullname)
    try: return Layout([line.strip() for line in f])
    finally: f.close()
