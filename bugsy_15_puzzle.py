#for leslie kaelbling bling bling
#Michael and Andy
w_t = 9
w_f = 9
#Weight of time and solution cost
import time
import heapq
from math import log
class Puzzle:
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

#make bugsy happen

def bugsy(puzzle, u, goal_state_d):
    '''
    for later: be complicated...A search function which takes input Utility, Problem Instance (with initial state, goal state, and successor function)
    for now: be simple: 15 puzzle instance (goal, initial, next_states), Utility func, g* calculated by graph distance bt states
    '''
    start_time = time.time()
    closed = []
    frontier = [(-5, puzzle.initial_state, [], start_time)]
    #States are composed of (current state - tuple, parent state - tuple, cost - int)
    #State: tuple - (cost, current, parent)
    expansion_count = 0
    delay = 0
    total_delay_time = 0
    total_exp_time = 0
    t_exp = 0

    while len(frontier) > 0:
        #finds utility of each node on every iteration
        current = heapq.heappop(frontier)
        if puzzle.goal_state == current[1]:
            return current[2]
        closed.append(current)
        if not expansion_count == 0:
            delay  += total_delay_time / expansion_count
        #calc exp time
        t_exp_1 = time.time()
        for next in puzzle.next_states(current[1]):
            parent_path = current[2][:]
            parent_path.append(current[1])
            #use placeholder child node in util to avoid self-reference
            child = (u(start_time, w_t, w_f, g, (0,(),parent_path)), next, parent_path)
            if child[1] is puzzle.goal_state:
                heapq.heappush(frontier,child)
            elif u(start_time, w_t, w_f, g, child) > 0 or (child in closed or child in frontier):
                pass
            else:
                expansion_count += 1
                heapq.heappush(frontier,child)
        total_exp_time+=time.time()-t_exp_1
        t_exp = total_exp_time/expansion_count
        frontier = find_uhat(frontier, expansion_count)
    return 'while ended'

def convert_to_tuples(state):
    output = {}
    for i in range(len(state)):
        x = i % 4
        w = int(i / 4)
        output[start[i]] = (x, w)
    return output

def u(delay, t_exp, w_t, w_f, g, node):
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
    '''



    '''
    utility = -1 * (w_f * g(node) + w_t * delay * t_exp)
    return utility

def g(node):
    if type(node) is not None:
        return len(node[2])

goal_state_dict = convert_to_tuples(puzzle.goal_state)

def man_dist(puzzle_state, goal_state_dict):
    dict_puzzle = convert_to_tuples(puzzle_state)
    d = 0
    for i in xrange(1, len(goal_state_dict) + 1):
        dx = abs(dict_puzzle[i][0] - goal_state_dict[i][0])
        dw = abs(dict_puzzle[i][1] - goal_state_dict[i][1])
        d += (dx + dw)
    return d

def find_uhat(frontier, count, u):
    if type(log(expansion_count, 2)) is int:
        new_frontier = []
        for node in frontier:
            delay =
            util = u(delay, t_exp, w_t, w_f, g, node)
            new_frontier.append([])
        return heapq.heapify(new_frontier)
    else:
        return frontier


#test cases
start_state = (0, 1, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12)
new_puz = Puzzle(start_state)
print bugsy(new_puz, u)






