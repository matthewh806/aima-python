import layout
import sys
from utils import manhattan_distance
from search import Problem
from search import *

class MazeProblem(Problem):
    def __init__(self, initial, goal, maze):
        Problem.__init__(self, initial, goal)
        self.maze = maze

        print "Maze..."
        print self.maze
        print "start: ", self.initial
        print "goal: ", self.goal
        print "\n"
    
    def actions(self, state):
        "The actions at a maze pos are just neighbours"
        return maze.getLegalMoves(state).keys() 
    
    def result(self, state, action):
        "Result of going to neighbor is new neighbor position"
        return maze.getNeighbourPosition(state, action)

    def value(self, state):
        raise NotImplementedError
    
    def h(self, node):
        "h function is manhattan distance from a node's state to goal."
        return manhattan_distance(node.state, maze.goal)

class OnlineDFSMazeAgent(OnlineDFSAgent):
    def __init__(self, problem):
        OnlineDFSAgent.__init__(self, problem)
    
    def update_state(self, percept):
        "percept is just the new state"
        return percept

def readCommand(argv):
    """
    Process the command used to run maze from the command line.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Supply a maze and see it \
                                     solved by a search AI!")
    parser.add_argument('-m', '--maze', default='smallMaze', type=str,
                      help='The maze for the agent to solve')
    parser.add_argument('-s', '--search', default='dfs',
                        type=str, help='The search algorithm for the agent to \
                        use', choices=['dfs', 'bfs', 'astar'])
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = readCommand(sys.argv[1:])
    maze = layout.getLayout(args.maze)
    if maze is None:
        raise NameError("Could not find maze!")

    mazeProblem = MazeProblem(maze.start, maze.goal, maze)
    if args.search == "dfs":
        print "depth-first-search" 
        print depth_first_graph_search(mazeProblem).solution() 
        
    elif args.search == "bfs":
        print "breadth-first-search" 
        print breadth_first_tree_search(mazeProblem).solution()
    elif args.search == "astar":
        print "a-star search with manhattan distance heuristic"
        print astar_search(mazeProblem).solution()
    
