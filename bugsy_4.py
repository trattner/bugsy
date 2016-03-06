#bugsy

def bugsy(initialState, goalTest, actions, successor,
           heuristic = lambda s: 0, maxNodes = 10000,
           visitF = None, expandF = None, hmax = float('inf'),
           prevExpandF = None, checkExpandF = None,
           multipleSuccessors = False,
           verbose = False, printFinal = True, maxHDelta = None,
           maxCost = float('inf'),
           fail = True,
           postFailScan = True,
           returnFirstGoal = False,
           w_f, w_t):