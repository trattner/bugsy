#Problem Set 
#Name: Andrew Trattner
#Collaborators: none
#Time Spent: 0:


#for leslie kaelbling bling bling
#Michael and Andy

#Weight of time and solution cost
import time
import heapq
from math import log
import sys
import random

class Puzzle:
    """
    A 15-puzzle instance which takes input startin_state as a well-formed typle of 16 entries
    method next_states returns successors, goal_state is proper termination state
    """
    def __init__(self, starting_state):
        self.goal_state=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
        #State '0' represents the empty slot in the puzzle
        self.initial_state=starting_state

    def next_states(self, current_state):
        i = current_state.index(0)
        #Returns the position of the empty(0) slot
        validswaps = []
        v1 = i-4
        #Moving up
        v2 = i+4
        #Moving down
        v3 = i - 1
        #Moving left
        v4 = i + 1
        #Moving right

        if v1 >= 0:
            #Prevents you from going past top left corner
            validswaps.append(v1)
        if v2 <= 15:
            #Prevents you from going past bottom left corner
            validswaps.append(v2)
        if v3 % 4 < i % 4:
            #Prevents you from going past left side
            '''
            WORKING CASE:
            15(i) mod 4 returns 3
            14(v3) mod 4 returns 2
            So if the empty space is in position 15
            This would be a valid swap

            FAILURE CASE:
            12(i) mod 4 returns 0
            11(v2) mod 4 returns 1
            So if the empty space is in position 12
            This would not be a valid swap
            (Same case for 8,4,0)
            '''
            validswaps.append(v3)

        if v4 % 4 > i % 4:
            '''
            WORKING CASE:
            10(i) mod 4 returns 2
            11(v4) mod 4 returns 3
            So if the empty space is in position 10
            This would be a valid swap

            FAILURE CASE:
            1. 11(i) mod 4 returns 3
               12(v4) mod 4 returns 0
               So if the empty space is in position 11
               This would not be a valid swap
               (Same case for 3,7)
            '''
            validswaps.append(v4)
        next_states = []
        for v in validswaps:
            '''
            Swaps the empty space from the old position
            to the new position

            Will add each state from valid swaps to a list
            And return that list
            '''
            old = list(current_state)
            new = list(current_state)
            new[i] = old[v]
            new[v] = old[i]
            next_states.append(tuple(new))
        return next_states

#make a*

def a_star(puzzle, steps):
    
    index_state = 1
    index_parent_path = 2
    index_cost = 0
    index_birth_time = 3
    
    percent = 0

    closed = []
    initial_distance = -sys.maxint
    frontier = [(-sys.maxint, puzzle.initial_state,[])]
    #States are composed of (cost, state, parent path)
    
    #goal state dictionary allows for quick lookup for Manhattan Dist Calc
    goal_state_dictionary = convert_to_tuples(puzzle.goal_state)
    
    stopnow = 0
    
    goal_dictionary = convert_to_tuples(puzzle.goal_state)
    
    while len(frontier) > 0 and stopnow < steps:
        
        #pop off element and check if goal. mark state as visited
        current = heapq.heappop(frontier)
        if puzzle.goal_state == current[index_state]:
            current[index_parent_path].append(current[index_state])
            return current[index_parent_path]
        closed.append(current)
    
        #expand state using Manhattan Distance heuristic
        for state in puzzle.next_states(current[index_state]):
            parent_path = current[index_parent_path][:]
            parent_path.append(current[index_state])
            cost = len(parent_path) + man_dist(state, goal_dictionary) 
            child = (cost, state, parent_path)
            if child in closed or child in frontier:
                print 'child explored'
            else:
                heapq.heappush(frontier, child)

        if stopnow / float(steps) * 100 > percent:
            print str(percent) + ' percent complete'
            percent += 1
        stopnow+=1
        
    return_msg = 'search terminated due to timeout, length of frontier is: ' + str(len(frontier))
    return return_msg
    
def bugsy(puzzle, steps):

    """
    BUGSY(initial, U())

    Utility = U_default - min(over children) { wf*cost + wt*time }
    -U_default is utility of returning empty solution
    -cost is length of parent path + manhattan distance
    -time is distance to end from current (manhattan) * delay * t_exp
        where delay is number of extra expansions estimated in between useful progress
        and t_exp is typical time to expand each node
        -->these parameters can be updated in realtime or they may be calculated beforehand (training)
    
    U* = -(wf*cost + wt*nodes_on_s*t_exp)
    u* = U* or U*-wt*t_exp
    -->t_exp is time to perform expansion of node
    
    estimating Max Util:
    1. estimate cost of solution find beneath each node as f
    2. estimates number expansions required to find a solution beneath each node n, exp(n) -- can be dist heuristic d
    3. exp(n) = delay * d(n) since delay expansions expected on each of d's steps
    
    Bugsy can stop and return empty or expand a node. Each node in frontier is possible outcome, so max util based on open nodes:
    U_hat = max{ max(n in frontier){ -wf*f(n)+wt*d(n)*delay*t_exp }, U(empty,0)}
    
    once uhat is found, substitute for U* to estimate u*
    -->note that only expanding one node, so no need to estimate u* for all frontier nodes
    -->note that computing maximization each time is unnecessary since simply ordering on u(n) is sufficient
    
    UTILITY DETAILS:

    """

    index_state = 1
    index_parent_path = 2
    index_cost = 0
    index_birth_time = 3
    
    DELAY = 1
    T_EXP = 1    
    w_f = 1
    w_t = 1
    
    percent = 0

    closed = []
    initial_util = sys.maxint
    frontier = [(initial_util, puzzle.initial_state,[])]
    #States are composed of (utility, state, parent path)
    
    #goal state dictionary allows for quick lookup for Manhattan Dist Calc
    goal_state_dictionary = convert_to_tuples(puzzle.goal_state)
    
    stopnow = 0
    
    while len(frontier) > 0 and stopnow < steps:
        
        #pop off MIN element and check if goal. mark state as visited
        current = heapq.heappop(frontier)
        if puzzle.goal_state == current[index_state]:
            current[index_parent_path].append(current[index_state])
            return current[index_parent_path]
        closed.append(current[index_state])
    
        #expand state using Manhattan Distance heuristic
        for state in puzzle.next_states(current[index_state]):
            parent_path = current[index_parent_path][:]
            parent_path.append(current[index_state])
            util = calculate_utility(len(parent_path), state, goal_state_dictionary, w_f, w_t, DELAY, T_EXP)
            child = (util, state, parent_path)
            if child in closed:
                pass
            elif child in frontier:
                update_best(child, frontier, index_state, index_cost)
            else:
                heapq.heappush(frontier, child)
        if stopnow / (steps/100.) > percent:
            print str(percent) + ' percent complete'
            percent += 1
        stopnow+=1
        
    return_msg = 'search terminated due to timeout, length of frontier is: ' + len(frontier)
    return return_msg

def convert_to_tuples(state):
    output = {}
    for i in range(1, len(state)+1):
        x = (i-1) % 4
        w = int((i-1) / 4)
        output[state[i-1]] = (x, w)
    return output

def calculate_utility(parent_path_length, state, goal_state_dictionary, w_f, w_t, delay, t_exp):
    util = w_f * parent_path_length + w_t * man_dist(state, goal_state_dictionary) * delay * t_exp
    return util

def u(delay, t_exp, w_t, w_f, g, node, goal_state_dictionary):
    '''
    utility = something here ****
    Involving w_t and w_f

    ^
    U = max { max( n in frontier) - (w_f *  f(n) + w_t * d(n) * delay * t_exp)}
                                            ^
    You expand the node that produces the   U value above

    d(n) = Manhattan distance
    f(n) = g*(n) + d(n)

    Calculate d:
        -Loop and use the difference between the index of each number
        -in current state and the index of those same numbers in goal state
    '''
    utility =  (w_f * g(node) + w_t * man_dist(node ,goal_state_dictionary) * delay * t_exp)
    return utility

def man_dist(puzzle_state, goal_state_dict):
    dict_puzzle = convert_to_tuples(puzzle_state)
    d = 0
    for i in xrange(1, len(goal_state_dict)):
        dx = abs(dict_puzzle[i][0] - goal_state_dict[i][0])
        dw = abs(dict_puzzle[i][1] - goal_state_dict[i][1])
        d += (dx + dw)
    return d

def find_uhat(frontier, count, u, delay, t_exp, w_t, w_f, g, Uhat):
    if type(log(count, 2)) is int:
        new_frontier = []
        u_new = Uhat
        for node in frontier:
            util = u(delay, t_exp, w_t, w_f, g, node)
            new_frontier.append((util, node[1], node[2], node[3]))
            u_new = max(u_new, util)
        return (heapq.heapify(new_frontier), u_new)
    else:
        return (frontier, Uhat)

def shuffle(n):
    puzzle_initial = Puzzle((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0))
    out_state = puzzle_initial.goal_state
    rand_ind = 0
    for i in xrange(n):
        next_states = puzzle_initial.next_states(out_state)
        rand_ind = int(random.random()*len(next_states))
        out_state = next_states[rand_ind]
    return out_state

def update_best(state,frontier, index_state,  index_cost):
    for front_state in frontier:
        if front_state[index_state] == state[index_state]:
            new_util = min(front_state[index_cost], state[index_cost])
            if new_util == front_state[index_cost]:
                state = front_state
#test cases
times = []
w_t = 9
w_f = 9

#test case 1
start_state = (3, 7, 0, 4, 1, 6, 2, 8, 5, 10, 13, 12, 9, 14, 11, 15) #shuffle(60)
# with time diff 0.546999931335
new_puz = Puzzle(start_state)
goal_state_dict = convert_to_tuples(new_puz.goal_state)
start_time = time.time()
print a_star(new_puz, 10000)
end_time = time.time()
print end_time - start_time
start_time = time.time()
print bugsy(new_puz, 10000)
end_time = time.time()
print end_time - start_time

#should test if child in closed and has better util now?
