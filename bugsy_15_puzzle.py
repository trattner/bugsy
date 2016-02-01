#for leslie kaelbling bling bling
w_t = 2
w_f = 3
#Weight of time and solution cost
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

        if v4 <= 15 and v4 % 4 > i % 4:
            '''
            WORKING CASE:
            10(i) mod 4 returns 2
            11(v4) mod 4 returns 3
            So if the empty space is in position 10
            This would be a valid swap

            FAILURE CASE:
            1. 16(v4) is not less than current_state length

            2. 11(i) mod 4 returns 3
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
'''
BUGSY Pseudo code:

Bugsy(initial, u(·))
1. open ← {initial}, closed ← {}
2. do
3.      n ← remove node from open with highest u(n) value
4.      if n is a goal, return it
5.      add n to closed
6.      for each of n('parent')’s children c('child'),
7.          if c is not a goal and u(c) < 0 or an old version of c is in open or closed
8.              skip c
9.          else add c to open
10.     if the expansion count is a power of two
11.         re-compute u(n) for all nodes on the open list using the most recent estimates
12.         re-heapify the open list
13.loop to step 3

'''
def bugsy(puzzle, u_func):

    if puzzle.initial_state == puzzle.goal_state:
        closed.append(n)
        return puzzle.initial_state
    open = []
    open.append(puzzle.initial_state)
    closed = []
    expansion_count = 0
    while not open.isEmpty():
        utilities = []
        for node in open:
            utilities.append(u_func(node))
        max_util_pos = utilities.indexof(max(utilities))
        parent = open.pop(max_util_pos)
        if puzzle.goal_state == parent:
            closed.append(parent)
            return parent
        for child in puzzle.next_states(parent):
            if child is not puzzle.goal_state and u_func(child) < 0:
                pass
            if child in closed or child in open:
                pass
            else:
                expansion_count += 1
                open.append(child)

        if expansion_count % 2 == 0:
            '''
            utilities = []
            for node in open:
                utilities.append(u_func(node))
            pass
            '''




def u(node):
    '''
    utility = something here ****
    Involving w_t and w_f
    '''
    return utility

#test cases
start_state = (0, 1, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12)
new_puz = Puzzle(start_state)
print bugsy(new_puz, new_puz.next_states, u)
