#for leslie k
class Puzzle:
    def __init__(self, starting_state):
        self.goal_state=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
        self.initial_state=starting_state
        return None

    def next_states(self, s):
        i = s.index(0)
        validswaps=[]
        v1 = i-4
        v2 = i+4
        v3 = i - 1
        v4 = i + 1
        if v1>=0:
            validswaps.append(v1)
        if v2<=15:
            validswaps.append(v2)
        if v3%4<i%4:
            validswaps.append(v3)
        if v4%4>i%4:
            validswaps.append(v4)
        out = []
        for v in validswaps:
            old = list(s)
            new = list(s)
            new[i]=old[v]
            new[v]=old[i]
            out.append(tuple(new))
        return out

#make bugsy happen
def bugsy(puzzle, successors, u):

    return path

def u(g, d):
    utility = something here ****
    return utility

#test cases
start_state = (0, 1, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12)
new_puz = Puzzle(start_state)
print bugsy(new_puz, new_puz.next_states, u)
