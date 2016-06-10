import layout
from search import Problem
from search import breadth_first_search

class MazeProblem(Problem):
    def __init__(self, initial, goal, maze):
        Problem.__init__(self, initial, goal)
        self.maze = maze
    
    def actions(self, state):
        "The actions at a maze pos are just neighbours"
        return maze.getLegalPositions() 
    
    def result(self, state, action):
        "Result of going to neighbor is neighbor"
        raise NotImplementedError

    def value(self, state):
        raise NotImplementedError

if __name__ == "__main__":
    maze = layout.getLayout("smallMaze")
    breadth_first_search(MazeProblem(maze.start, maze.goal, maze))
    print maze 
