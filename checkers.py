import copy
import sys


#No time to finish again :'(

MAX_ROW, MAX_COL = 8, 8

# key: board, value: minimax val
cache = {}

class Board:
    def __init__(self):
        self.squares = []
        self.rCount, self.bCount, self.RCount, self.BCount = 0, 0, 0, 0

    def print(self):
        for row in self.squares:
            string = ''
            for square in row:
                string += square + ' '
            print(string[:-1])

    def hash(self):
        string = ''

        for row in self.squares:
            for square in row:
                string += square

        return string

def terminal(board: Board):
    if board.rCount + board.RCount <= 0:
        return 'b'
    if board.bCount + board.BCount <= 0:
        return 'r'

def utility(board):
    redPoints = board.rCount + board.RCount * 2
    blackPoints = board.bCount + board.BCount * 2
    return redPoints - blackPoints

def getMoves(board: Board, player):
    moves = []

    for i in range(MAX_ROW):
        for j in range(MAX_COL):
            piece: str = board.squares[i][j]

            if piece.lower() == player:
                moves.extend(list(getValidMoves(board, piece, i, j).values()))

    return moves

def getValidMoves(board, piece, row, col, isConsecutive=False):
    moves = {}

    if piece in ['r', 'R', 'B']:
        moves.update(tryMove(board, piece, row, col, -1, -1, isConsecutive))
        moves.update(tryMove(board, piece, row, col, -1, 1, isConsecutive))
    if piece in ['b', 'R', 'B']:
        moves.update(tryMove(board, piece, row, col, 1, -1, isConsecutive))
        moves.update(tryMove(board, piece, row, col, 1, 1, isConsecutive))

    return moves

def tryMove(board, piece, oldRow, oldCol, deltaRow, deltaCol, isConsecutive):
    moves = {}

    newRow = oldRow + deltaRow
    newCol = oldCol + deltaCol

    if not isInBounds(newRow, newCol):
        return moves

    newSquare = board.squares[newRow][newCol]

    if newSquare == '.':
        if not isConsecutive:
            boardCopy = copy.deepcopy(board)
            movePiece(boardCopy, oldRow, oldCol, newRow, newCol)
            boardHash = boardCopy.hash()
            if boardHash not in moves:
                moves[boardHash] = boardCopy
        else:
            boardHash = board.hash()
            if boardHash not in moves:
                moves[boardHash] = board

    elif piece.lower != newSquare.lower:
        farRow = newRow + deltaRow
        farCol = newCol + deltaCol

        if not isInBounds(farRow, farCol):
            return moves

        farSquare = board.squares[farRow][farCol]
        if farSquare == '.':
            boardCopy = copy.deepcopy(board)
            # boardCopy.squares[newRow][newCol] = '.'
            capturePiece(boardCopy, newRow, newCol)
            if movePiece(boardCopy, oldRow, oldCol, farRow, farCol):
                boardHash = boardCopy.hash()
                if boardHash not in moves:
                    moves[boardHash] = boardCopy # piece was crowned so turn ends
            else:
                moves.update(getValidMoves(boardCopy, boardCopy.squares[farRow][farCol], farRow, farCol, True))

    return moves

def isInBounds(row, col):
    return 0 < row <  MAX_ROW and 0 < col < MAX_COL

def capturePiece(board, row, col):
    piece = board.squares[row][col]

    if piece == 'r':
        board.rCount -= 1
    if piece == 'R':
        board.RCount -= 1
    if piece == 'b':
        board.bCount -= 1
    if piece == 'B':
        board.BCount -= 1

    board.squares[row][col] = '.'

def movePiece(board, oldRow, oldCol, newRow, newCol):
    board.squares[oldRow][oldCol], board.squares[newRow][newCol] = \
        board.squares[newRow][newCol], board.squares[oldRow][oldCol]

    if (newRow == 0 or newRow == MAX_ROW - 1) and \
            board.squares[newRow][newCol] == board.squares[newRow][newCol].lower:
        board.squares[newRow][newCol].capitalize()

        if board.squares[newRow][newCol] == 'R':
            board.RCount += 1
            board.rCount -= 1
        else: # square == 'B'
            board.BCount += 1
            board.bCount -= 1

        return True

    return False

def heuristic(board):
    # TODO
    return utility(board)

def minimax(pos: Board, depth, isMax, alpha, beta):
    # TODO:
    # Ordering
    bestMove = None

    if depth == 0 or terminal(pos) is not None:
        return utility(pos), bestMove

    if isMax:
        if pos in cache:
            return cache[pos], bestMove

        maxUtil = -sys.maxsize - 1

        for move in getMoves(pos, 'r'):  # TODO: decide if move == board state or something else
            util = minimax(move, depth - 1, False, alpha, beta)[0]
            if util > maxUtil:
                maxUtil, bestMove = util, move
            if maxUtil >= beta:
                return maxUtil, bestMove
            alpha = max(alpha, maxUtil)

        cache[pos.hash()] = maxUtil
        return maxUtil, bestMove
    else:
        if pos in cache:
            return cache[pos], bestMove

        minUtil = sys.maxsize

        for move in getMoves(pos, 'b'):

            util = minimax(move, depth - 1, True, alpha, beta)[0]
            if util < minUtil:
                minUtil, bestMove = util, move
            if minUtil <= alpha:
                return minUtil, bestMove
            beta = min(alpha, minUtil)

        cache[pos.hash()] = minUtil
        return minUtil, bestMove

def cacheMinimax(pos: Board, depth, isMax, alpha, beta):
    # TODO:
    # Ordering
    bestMove = None

    if depth == 0 or terminal(pos) is not None:
        return utility(pos), bestMove

    if isMax:
        if pos in cache:
            return cache[pos], bestMove

        maxUtil = -sys.maxsize - 1

        for move in getMoves(pos, 'r'):  # TODO: decide if move == board state or something else
            util = minimax(move, depth - 1, False, alpha, beta)[0]
            if util > maxUtil:
                maxUtil, bestMove = util, move
            if maxUtil >= beta:
                return maxUtil, bestMove
            alpha = max(alpha, maxUtil)

        cache[pos.hash()] = maxUtil
        return maxUtil, bestMove
    else:
        if pos in cache:
            return cache[pos], bestMove

        minUtil = sys.maxsize

        for move in getMoves(pos, 'b'):
            util = minimax(move, depth - 1, True, alpha, beta)[0]
            if util < minUtil:
                minUtil, bestMove = util, move
            if minUtil <= alpha:
                return minUtil, bestMove
            beta = min(alpha, minUtil)

        cache[pos.hash()] = minUtil
        return minUtil, bestMove


def alphaBetaMiniMax(pos: Board, depth, isMax, alpha, beta):
    # TODO:
    # Caching
    # Ordering
    bestMove = None

    if depth == 0 or terminal(pos) is not None:
        return utility(pos), bestMove

    if isMax:
        maxUtil = -sys.maxsize - 1

        for move in getMoves(pos, 'r'):  # TODO: decide if move == board state or something else
            util = minimax(move, depth - 1, False, alpha, beta)[0]
            if util > maxUtil:
                maxUtil, bestMove = util, move
            if maxUtil >= beta:
                return maxUtil, bestMove
            alpha = max(alpha, maxUtil)

        return maxUtil, bestMove
    else:
        minUtil = sys.maxsize

        for move in getMoves(pos, 'b'):
            util = minimax(move, depth - 1, True, alpha, beta)[0]
            if util < minUtil:
                minUtil, bestMove = util, move
            if minUtil <= alpha:
                return minUtil, bestMove
            beta = min(alpha, minUtil)

        return minUtil, bestMove


def dfsMinimax(pos: Board, depth, isMax):
    # AB pruning
    # Caching
    # Ordering
    if depth == 0 or terminal(pos):
        return utility(pos), pos

    if isMax:
        minimaxMax(pos, depth)
    else:
        minimaxMin(pos, depth)


def minimaxMax(pos, depth):
    maxUtil = -sys.maxsize - 1
    bestMove = None

    for move in getMoves(pos, 'r'):
        util = dfsMinimax(move, depth - 1, False)[0]
        if util > maxUtil:
            maxUtil, bestMove = util, move

    return maxUtil, bestMove


def minimaxMin(pos, depth):
    minUtil = sys.maxsize
    bestMove = None

    for move in getMoves(pos, 'b'):
        util = dfsMinimax(move, depth - 1, True)[0]
        if util < minUtil:
            minUtil, bestMove = util, move

    return minUtil, bestMove

def readBoard(path: str):
    board = Board()

    with open(path) as f:
        lines = f.read().splitlines()

    for line in lines:
        row = []
        for char in line:
            row.append(char)

            if char == 'r':
                board.rCount += 1
            if char == 'R':
                board.RCount += 1
            if char == 'b':
                board.bCount += 1
            if char == 'B':
                board.BCount += 1

        board.squares.append(row)

    return board

def writeBoard(board: Board, path):
    with open(path, 'w') as f:
        for row in board.squares:
            string = ''
            for char in row:
                string += char
            f.write(string)
            f.write('\n')


# inputBoard = readBoard(sys.argv[1])
# writeBoard(minimax(inputBoard, 5, 'r', -sys.maxsize - 1, sys.maxsize)[1], sys.argv[2])