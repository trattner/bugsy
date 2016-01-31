class Puzzle:
    def __init__(self, starting_state):
        self.goal_state=(1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.initial_state=starting_state
        return None

    def next_states(self, s):
        i = s.index(0)
        validswaps=[]
        v1 = i-3
        v2 = i+3
        v3 = i - 1
        v4 = i + 1
        if v1>=0:
            validswaps.append(v1)
        if v2<=8:
            validswaps.append(v2)
        if v3%3<i%3:
            validswaps.append(v3)
        if v4%3>i%3:
            validswaps.append(v4)
        out = []
        for v in validswaps:
            old = list(s)
            new = list(s)
            new[i]=old[v]
            new[v]=old[i]
            out.append(tuple(new))
        return out
