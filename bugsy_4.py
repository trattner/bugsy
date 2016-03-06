#bugsy

import pdb
from heapq import heappush, heappop

import planGlobals as glob
from traceFile import debugMsg, debug, trAlways, tr

import time
import math

"""
Procedures and classes for BUGSY as described in
https://www.jair.org/media/4047/live-4047-7225-jair.pdf 
"""


class SearchNode:
    """A node in a search tree"""
    def __init__(self, action, state, parent, actionCost, heuristicCost = 0):
        self.state = state
        self.action = action
        self.actionCost = actionCost
        self.heuristicCost = heuristicCost
        """Action that moves from C{parent} to C{state}"""
        self.parent = parent
        if self.parent:
            self.cost = self.parent.cost + actionCost
            """The cost of the path from the root to C{self.state}"""
        else:
            self.cost = actionCost
        
    def path(self):
        """@returns: list of C{(action, state)} pairs from root to this node"""
        if self.parent is None:
            return [(self.action, self.state)]
        else:
            return self.parent.path() + [(self.action, self.state)]

    def costs(self):
        """@returns: list of C{(action, state)} pairs from root to this node"""
        if self.parent is None:
            return [self.cost]
        else:
            return self.parent.costs() + [self.cost]

    def inPath(self, s):
        """@returns: C{True} if state C{s} is in the path from here to
        the root"""
        if s == self.state:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.inPath(s)

    def __repr__(self):
        if self.parent is None:
            return str(self.state)
        else:
            return repr(self.parent) + \
                   "-"+str(self.action)+"->"+str(self.state)

    __str__ = __repr__


# using general parameters/format found in ucSearchPQ.py from Leslie Kaelbling
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
               
        """
        @param initialState: root of the search
        @param goalTest: function from state to Boolean
        @param actions: function from state to list of actions
        @param successor: function from state and action to next state and cost
        @param heuristic: function from state to estimated cost to reach a goal;
            defaults to a heuristic of 0, making this uniform cost bugsy
        @param maxNodes: kill the search after it expands this many nodes
        @param visitF: function occurring on visits
        @param expandF: function occurring on expansion
        @param hmax: max heuristic val
        @param prevExpandF: function occurring if previously node has been expanded
        @param checkExpandF: check legality of expanding node n?
        @param multipleSuccessors: are there multiple successors of a state allowed?
        @param verbose: print a bunch of things while running
        @param printFinal: print final solution
        @param maxHDelta: maximum change in heuristic across parent-child nodes
        @param maxCost: maximum cost of a state allowed
        @param fail: ?
        @param postFailScan: perform a scan after failure
        @param returnFirstGoal: I want to return first goal found
        @param w_f: weight on estimated cost of solution
        @param w_t: weight on estimated time to reach solution from current expansion
        
        @returns: path from initial state to a goal state as a list of
               (action, state) tuples and a list of path costs from start to
               each state in the path
        """
        
        ########### HELPER METHODS #############
        def getH(state):
            if not state in hVals:
                hv = heuristic(state)
                hVals[state] = hv
            return hVals[state]
        
        def getUtil(node, delay, t_exp, w_f, w_t):
            """
            calculate the utility of a state based on estimated cost and time to obtain solution
            
            @param node: a SearchNode
            @param delay: estimated delay expansions for each of the remaining steps from current node
            @param t_exp: estimated time to expand a node, in seconds
            @param w_f: weight on the cost function
            @param w_t: weight on the time to obtain solution
            
            @returns: floating point utility of a node
            """
            return w_f*(node.cost + node.heuristicCost) + w_t*(node.heuristicCost * delay * t_exp)

        def updateEstimates(delay, t_exp, agenda, w_f, w_t):
            """
            @param delay: most recent global delay estimate
            @param t_exp: most recent global t_exp estimate
            @param agenda: agenda to be re-sorted based on most recent estimates, assumes agenda has elements of the form (utility, count, SearchNode)
            @param w_f: weight on cost function
            @param w_t: weight on time to obtain solution
            
            @returns: newly heapified agenda
            """
            newAgenda = []
            for item in agenda:
                heappush(newAgenda, (getUtil(item[2], delay, t_exp, w_f, w_t), item[1], item[2]))
            return newAgenda
        def newDelay(delayList, current_count, node_count):
            """
            @param delayList: list of past delay estimates
            @param current_count: count of the expansions completed
            @param node_count: count of expansions at generation of agenda item
            
            @returns: a new global average delay estimate to be added to list
            """
            n_d = len(delayList) + 1.
            new_delay = (1/n_d) * (current_count - node_count) + (n_d-1)/n_d * delayList[-1]
            return new_delay
        def newT_exp(t_exp_list, t_exp):
            """
            @param t_exp_list: list of past t_exp estimates
            @param t_exp: new estimate to average
            
            @returns: a new global average t_exp estimate to be added to list
            """
            n_t = len(t_exp_list) + 1.
            new_t_exp = (1/n_t) * t_exp + (n_t-1)/n_t * t_exp_list[-1]
            return new_t_exp
        def searchFinished(n, somewhatVerbose, verbose, count):
            """
            things we do when goal state is expanded
            
            @param n: current node
            @somewhatVerbose: how much printing
            @verbose: more conditionals on printing
            @param count: steps of expansion taken
            
            @returns: 
            """
            if somewhatVerbose or verbose:
                print 'Found goal state', n.state
            if somewhatVerbose or verbose or printFinal:
                print count, 'nodes visited;', \
                        countExpanded, 'states expanded;', \
                        'solution cost:', n.cost
            if getH(n.state) > 0:
                debugMsg('heuristic', 'positive value at goal state',
                         n.state, getH(n.state))
            return None            
        ########### End Helper Methods ############
        
        
        ########### BUGSY INITIALIZATION #############
        delayList = []
        t_expList = []
        global_delay = 0
        global_t_exp = 0
        epsilon_0 = 10**(-12)
        somewhatVerbose = verbose
        verbose = False
        hVals = {}
        startNode = SearchNode(None, initialState, None, 0,
                               getH(initialState))
        if goalTest(initialState):
            return startNode.path(), [0]
        if startNode.heuristicCost >= hmax:
            trAlways('Root has infinite heuristic value', pause = True)
            return None, None   
        agenda = []
        count = 1
        countExpanded = 0
        heappush(agenda, (0, count, startNode)) #agenda objects have cost = utility, count = nodes visited, node class
        expanded = set([]) #set of states, different than agenda objects
        ############ End Initialization #############
        
        ############## BUGSY SEARCH #################
        while not agenda == [] and maxNodes > count:
        ### 0. BUGSY ESTIMATES UPDATE: on powers of 2, update agenda with current estimates
            if (abs(math.log(count, 2)-math.floor(math.log(count, 2))) < epsilon_0 or \
                    abs(math.log(count, 2)-math.ceil(math.log(count, 2))) < epsilon_0) and \
                    count > 1:
                global_delay = delayList[-1]
                global_t_exp = t_expList[-1]
                agenda = updateEstimates(global_delay, global_t_exp, agenda, w_f, w_t)
                if verbose:
                    print 'updated delay: ', global_delay, ', updated t_exp: ', global_t_exp 
                
        ### 1. PREPARE TO EXPAND: pop off of heap, test if goal, and check legal actions/maxCost. print a bunch of things
            if verbose:
                print "agenda: ", agenda
            (util, n_count, n) = heappop(agenda)
            start_expansion_time = time.clock()
            if count > 1: delayList.append(newDelay(delayList, count, n_count))
            if n.state in expanded: #should this ever happen?
                if prevExpandF: prevExpandF(n)
                if verbose:
                    print  "previously expanded: ", n.cost, n.state
                    raw_input('okay?')
                continue
            expanded.add(n.state)
            countExpanded += 1
            if checkExpandF:            # check legality on demand
                n = checkExpandF(n)      # possibly modify the node or set to None
                if n is None: continue      
            if expandF: expandF(n)
            if verbose: print  "expanding node: ", n.cost, n.state
            if goalTest(n.state):
                searchFinished(n, somewhatVerbose, Verbose, count)
                return n.path(), n.costs()
            if n.cost > maxCost:
                if True: #somewhatVerbose or verbose:
                    print "Search failed: exceeded max cost ", n.cost
                return None, None
            if getH(n.state)== 0:
                debugMsg('heuristic', 'zero value at non-goal state', n.state)
            applicableActions = actions(n.state)
            if len(applicableActions) == 0 and verbose:
                raw_input('no children')
            if somewhatVerbose or verbose:
                print "   ", n.cost, ":   expanding: ",  n
                print "         ", len(applicableActions), 'actions'
            if countExpanded % 10000 == 0:
                print 'cost', n.cost, 'nodes', count
            successors = set()  
            
        ### 2. EXPAND BY EXPLORING ACTIONS: add children to agenda
            for a in applicableActions:
                succ = successor(n.state, a)
                if not succ: continue
                if not multipleSuccessors:
                    succ = [succ]
                if verbose: print '        ', len(succ), 'successors'
                for (newS, cost) in succ:
                    if newS in successors: continue
                    else: successors.add(newS)
                    if verbose or somewhatVerbose:
                        print '           ', cost, newS
                    hValue = getH(newS)
                    if newS in expanded:
                        if prevExpandF and visitF:
                            newN = SearchNode(a, newS, n, cost, hValue)
                            visitF(n.state, n.cost, n.heuristicCost, a,
                                   newS, newN.cost, hValue)
                            prevExpandF(newN)
                            if maxHDelta and n.heuristicCost - hValue > maxHDelta:
                                print 'current h =', n.heuristicCost, 'new h =', hValue
                                raw_input('H delta exceeded')
                            if verbose:
                                print  "previously expanded: ", \
                                      newN.cost, newN.state
                                raw_input('okay?')
                    else:
                        count += 1
                        tr('h', hValue)
                        if hValue >= hmax: continue
                        newN = SearchNode(a, newS, n, cost, hValue)
                        if visitF: visitF(n.state, n.cost, n.heuristicCost, 
                                          a, newS, newN.cost, hValue)
                        if maxHDelta and n.heuristicCost - hValue > maxHDelta:
                            print 'current h =', n.heuristicCost, \
                              'new h =', hValue
                            raw_input('H delta exceeded')
                        if returnFirstGoal and goalTest(newS):
                            return newN.path(), newN.costs()
                        util = getUtil(newN, global_delay, global_t_exp, w_f, w_t)
                        heappush(agenda,
                                 (util, count, newN))
            #done expanding, add new time of expansion estimate                     
            t_exp_list.append(newT_exp(t_exp_list, time.clock() - start_expansion_time))
        ### 3. EXPANSIONS TERMINATED: the BUGSY search failed to return a solution        
        if somewhatVerbose or verbose or count >= maxNodes:
            print "Search failed after visiting ", count, " states."
        if postFailScan:
            while not agenda == []:
                (util, _, n) = heappop(agenda)
                if n.state in expanded: continue
                if checkExpandF:        # check legality on demand
                    n = checkExpandF(n) # possibly modify the node or set to None
                    if n is None: continue
                if goalTest(n.state):
                    if expandF: expandF(n)  # Treat like an expansion
                    print 'Found goal on agenda, returning it'
                    return n.path(), n.costs()
        return None, None