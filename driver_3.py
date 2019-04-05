
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import copy
import queue as Q
import heapq as heapq
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle



class Node(object):
    def __init__(self, state, md):
        self.config = state.config
        self.state = state
        self.md = md
    def __str__(self):
        return str(self.state.display())

    def __lt__(self, other):
        return self.md < other.md



class Frontier(object):
    def __init__(self):
        self._prioqueue = []


    def __getitem__(self, key):
        return 

    def insert(self, item, md):
        toPush = Node(item, md)
        heapq.heappush(self._prioqueue, toPush)

    def popMin(self):
        return heapq.heappop(self._prioqueue)

    def decreaseKey(self, item, newmd, curdepth):
        value = newmd + curdepth
        for node in self._prioqueue:
            if (node.config == item.config) and (node.md > value) :
                node.md = newmd + node.state.cost
                node.state.parent = item.parent


    def isEmpty(self):
        if len(self._prioqueue) <= 0:
            return True
        return False






class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        #this = PuzzleState(self.config, self.n, self.parent, self.action, self.cost)    
        newconfig = copy.deepcopy(self.config)
        action = "Up"
        cost = self.cost
        i = 0
        while newconfig[i] != 0:
            i += 1
        if((i-3) < 0):
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost)
            return newPuzzle
        else:
            newconfig[i] = newconfig[i-3]
            newconfig[i-3] = 0
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost + 1)
            return newPuzzle

      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        #this = PuzzleState(self.config, self.n, self.parent, self.action, self.cost)    
        newconfig = copy.deepcopy(self.config)
        action = "Down"
        cost = self.cost
        i = 0
        while newconfig[i] != 0:
            i += 1
        if((i+3) >= (self.n)**2):
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost)
            return newPuzzle
        else:
            newconfig[i] = newconfig[i+3]
            newconfig[i+3] = 0
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost + 1)
            return newPuzzle

      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        #this = PuzzleState(self.config, self.n, self.parent, self.action, self.cost)    
        newconfig = copy.deepcopy(self.config)
        action = "Left"
        cost = self.cost
        i = 0
        while newconfig[i] != 0:
            i += 1
        if((i-1) < 0 or i%self.n == 0):
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost)
            return newPuzzle
        else:
            newconfig[i] = newconfig[i-1]
            newconfig[i-1] = 0
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost + 1)
            return newPuzzle

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        #this = PuzzleState(self.config, self.n, self.parent, self.action, self.cost)    
        newconfig = copy.copy(self.config)
        action = "Right"
        cost = self.cost
        i = 0
        while newconfig[i] != 0:
            i += 1
        if((i+1) >= (self.n)**2 or i%self.n == 2):
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost)
            return newPuzzle
        else:
            newconfig[i] = newconfig[i+1]
            newconfig[i+1] = 0
            newPuzzle = PuzzleState(newconfig, self.n, parent=self, action=action, cost=cost + 1)
            return newPuzzle

    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return 0

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, expanded, maxdepth, start_time):
    ### Student Code Goes here
    end_time = time.time()
    arr = calculate_total_path(state)
    print("path_to_goal: ", arr)
    print("cost_of_path ", state.cost)
    print("nodes_expanded: ", expanded)
    print("search_depth: ", len(arr))
    print("max_search_depth: ", maxdepth)
    print("running_time: ", end_time - start_time)
    print("max_ram_usage: ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/100000000)

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    goal_state = [0,1,2,3,4,5,6,7,8] # GENERALIZE
    frontier = Q.Queue()
    frontierset = {}
    frontiersetkeys = set()
    maxdepth = 0
    curdepth = 0
    
    frontier.put(initial_state)
    frontierset[tuple(initial_state.config)] = 1
    frontiersetkeys.add(tuple(initial_state.config))


    visited = set()
    

    expanded = 0
    start_time = time.time()
    while not frontier.empty():

        state = frontier.get()
        frontierset[tuple(state.config)] -= 1

        visited.add(tuple(state.config))

        curdepth = state.cost + 1
        



        if state.config == goal_state:
       
            writeOutput(state, expanded, maxdepth, start_time)
            return state

        else:
            expanded += 1
            state.expand()
            for item in state.children:


                if tuple(item.config) not in frontiersetkeys:
                    frontiersetkeys.add(tuple(item.config))
                    frontierset[tuple(item.config)] = 0

                if tuple(item.config) not in visited and frontierset[tuple(item.config)] == 0:
                  
 
                    frontierset[tuple(item.config)] += 1
                    frontier.put(item)
        maxdepth = max(maxdepth, curdepth)
                    
    return 0


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    goal_state = [0,1,2,3,4,5,6,7,8] # GENERALIZE
    frontier = list()
    frontierset = {}
    frontiersetkeys = set()
    maxdepth = 0
    curdepth = 0
    
    frontier.append(initial_state)
    frontierset[tuple(initial_state.config)] = 1
    frontiersetkeys.add(tuple(initial_state.config))


    visited = set()
    

    expanded = 0
    start_time  = time.time()
    while len(frontier) > 0:

        state = frontier.pop()
        frontierset[tuple(state.config)] -= 1
        visited.add(tuple(state.config))
        curdepth = state.cost 
        maxdepth = max(maxdepth, curdepth)
 


        if state.config == goal_state:
        
            writeOutput(state, expanded, maxdepth ,start_time)
            return state

        else:
            expanded += 1
            state.expand()
            for item in reversed(state.children):
            

                if tuple(item.config) not in frontiersetkeys:
                    frontiersetkeys.add(tuple(item.config))
                    frontierset[tuple(item.config)] = 0

                if tuple(item.config) not in visited and frontierset[tuple(item.config)] == 0:
           
                    frontierset[tuple(item.config)] += 1
                    frontier.append(item)
                    
        

    
    return 0


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    goal_state = [0,1,2,3,4,5,6,7,8] # GENERALIZE
    frontier = Frontier()
    frontierset = {}
    frontiersetkeys = set()
    maxdepth = 0
    curdepth = 0
    md = calculate_manhattan_dist(initial_state.config, 3)
    frontier.insert(initial_state, md)
    frontierset[tuple(initial_state.config)] = 1
    frontiersetkeys.add(tuple(initial_state.config))
  

    visited = set()
    

    expanded = 0
    start_time  = time.time()
    while not frontier.isEmpty():

        Node = frontier.popMin()
        frontierset[tuple(Node.state.config)] -= 1
        visited.add(tuple(Node.state.config))
        curdepth = Node.state.cost
        maxdepth = max(maxdepth, curdepth)


        if Node.state.config == goal_state:
           
            writeOutput(Node.state, expanded, maxdepth ,start_time)
            return Node.state

        else:
            expanded += 1
            Node.state.expand()
            for item in Node.state.children:
 


                if tuple(item.config) not in frontiersetkeys:
                    frontiersetkeys.add(tuple(item.config))
                    frontierset[tuple(item.config)] = 0

                if tuple(item.config) not in visited and frontierset[tuple(item.config)] == 0:
               
               
                    md = calculate_manhattan_dist(item.config, 3)
                    frontierset[tuple(item.config)] += 1
            
                    md += curdepth
                    frontier.insert(item, md)

                    

    
    return 0

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    cost = 0
    cur = state
    while cur.parent != None:
        cost += 1
        cur = cur.parent
    return cost

def calculate_total_path(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    path = []
    cur = state
    while cur.parent != None:
        path.append(cur.action)
        cur = cur.parent
    list.reverse(path)
    return path



def calculate_manhattan_dist(config, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###

    correctdict = {}
    distdict = {}
    sum = 0
    for i in range(n**2):
        correctdict[i] = (i//n, i%n)
    for j in range(n**2):
        distdict[config[j]] = (j//n, j%n)
    

    for k in range(n**2):
        sum += abs(distdict[k][0] - correctdict[k][0]) + abs(distdict[k][1] - correctdict[k][1]) 
    
    return sum


    

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    pass

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()