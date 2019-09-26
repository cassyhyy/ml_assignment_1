"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    exploredSet = set()
    # 用stack记录行进路线，路线存放变量为list类型，即[(tuple),()]（tuple例子：((35,1),'West',1)）
    stack = util.Stack()
    # 先push开始结点，为保证tuple一致化，初始化方向为None，cost为0
    stack.push([(problem.getStartState(), None, 0)])

    while not stack.isEmpty():
        actions = stack.pop()
        top = actions[-1]
        if problem.isGoalState(top[0]):
            # 到达终点，需要返回一系列actions如['West','East'....]，则需要取出栈顶的list中的tuple的第2个元素，去掉第一个元素，因为第一个元素是开始结点，第一个action不可取
            return [y for x, y, z in actions][1:]
        if top[0] not in exploredSet:
            # print('Exploring:', top[0], '...')
            exploredSet.add(top[0])
            # 得到successor后，需要将其分别与当前路线list合并，并push到栈中
            for successor in problem.getSuccessors(top[0]):
                stack.push(actions+[successor])
            # print(exploredSet)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    exploredSet = set()
    # 用queue记录行进路线，路线存放变量为list类型，即[(tuple),()]（tuple例子：((35,1),'West',1)）
    queue = util.Queue()
    queue.push([(problem.getStartState(), None, 0)])

    while not queue.isEmpty():
        actions = queue.pop()
        top = actions[-1]
        if problem.isGoalState(top[0]):
            # 到达终点，需要返回一系列actions如['West','East'....]，则需要取出栈顶的list中的tuple的第2个元素
            return [y for x, y, z in actions][1:]
        if top[0] not in exploredSet:
            # print('Exploring:', top[0], '...')
            exploredSet.add(top[0])
            # 得到successor后，需要将其分别与当前路线list合并，并push到队列中
            for successor in problem.getSuccessors(top[0]):
                queue.push(actions+[successor])
            # print(exploredSet)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    exploredSet = set()
    queue = util.PriorityQueue()
    queue.push([(problem.getStartState(), None, 0)], 0)

    while not queue.isEmpty():
        actions = queue.pop()
        top = actions[-1]
        if problem.isGoalState(top[0]):
            # 到达终点，需要返回一系列actions如['West','East'....]，则需要取出栈顶的list中的tuple的第2个元素
            return [y for x, y, z in actions][1:]
        if top[0] not in exploredSet:
            # print('Exploring:', top[0], '...')
            exploredSet.add(top[0])
            # 得到successor后，需要将其分别与当前路线list合并，并push到队列中
            for successor in problem.getSuccessors(top[0]):
                # priority = g(n)，即累加cost
                priority = 0
                for x, y, cost in actions + [successor]:
                    priority += cost
                queue.push(actions+[successor], priority)
            # print(exploredSet)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    exploredSet = set()
    # 用queue记录行进路线，路线存放变量为list类型，即[(tuple),()]（tuple例子：((35,1),'West',1)）
    queue = util.PriorityQueue()
    queue.push([(problem.getStartState(), None, 0)], 0)

    while not queue.isEmpty():
        actions = queue.pop()
        top = actions[-1]
        if problem.isGoalState(top[0]):
            # 到达终点，需要返回一系列actions如['West','East'....]，则需要取出栈顶的list中的tuple的第2个元素
            return [y for x, y, z in actions][1:]
        if top[0] not in exploredSet:
            # print('Exploring:', top[0], '...')
            exploredSet.add(top[0])
            # 得到successor后，需要将其分别与当前路线list合并，并push到队列中
            for successor in problem.getSuccessors(top[0]):
                # priority = g(n) + h(n)，h(n)通过heuristic函数计算
                ucs_g = 0
                for x, y, cost in actions + [successor]:
                    ucs_g += cost
                queue.push(actions+[successor], ucs_g+heuristic(successor[0], problem))
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
