import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        # 记录循环次数
        loopTimes = 0
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            # 新的停止条件：attacks为0或者循环次数超过30
            if currentNumberOfAttacks == 0 or loopTimes >= 30:
                break
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks <= newNumberOfAttacks and i >= 30:
                # 如果递归次数超过30并且attack次数一直不减，重新开始一次新的循环
                i = 0
                newBoard = Board([[]])
                loopTimes += 1
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        board = self.squareArray
        costBoard = self.getCostBoard().squareArray
        minAttacks = []
        for c in range(8):
            minAttacks.append(min([r[c] for r in costBoard]))
        # 得到最小cost
        minNumOfAttack = min(minAttacks)
        resultList = []
        # 依据最小cost，将第一个扫描到的最小cost位置记录为newRow,newCol
        for c in range(8):
            board_column = [row[c] for row in board]
            costBoard_column = [row[c] for row in costBoard]
            if minNumOfAttack in costBoard_column:
                newRow = costBoard_column.index(minNumOfAttack)
                newCol = c
                oldRow = board_column.index(1)
                # 结果list，存放newRow,newCol,oldRow，便于通过board转换为betterBoard
                resultList.append((newRow, newCol, oldRow))
                # 添加到结果list后重置board
        # 在结果list中随机取一个
        (newRow, newCol, oldRow) = resultList[random.randint(0, len(resultList)-1)]
        board[oldRow][newCol] = 0
        board[newRow][newCol] = 1
        return (Board(board), minNumOfAttack, newRow, newCol)
        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        board = self.squareArray
        attacks = [[],[],[],[],[],[],[],[]]
        for c in range(8):
            for r in range(8):
                if board[r][c] == 1:
                    # 检测同一行是否有attack的
                    for cc in range(c + 1, 8):
                        if board[r][cc] == 1:
                            attacks[c].append(cc)
                    # 检测斜右下对角是否有attack的
                    rr = r + 1
                    cc = c + 1
                    while rr < 8 and cc < 8:
                        if board[rr][cc] == 1:
                            attacks[c].append(cc)
                        rr += 1
                        cc += 1
                    # 检测斜右上对角是否有attack的
                    rr = r - 1
                    cc = c + 1
                    while rr >= 0 and cc < 8:
                        if board[rr][cc] == 1:
                            attacks[c].append(cc)
                        rr -= 1
                        cc += 1
        result = 0
        for queen in attacks:
            result += len(queen)
        return result
        util.raiseNotDefined()

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
