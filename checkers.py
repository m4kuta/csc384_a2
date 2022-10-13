import sys

MAX_ROW, MAX_COL = 8, 8

class Board:
    def __init__(self):
        self.squares = []
        self.player = None
        self.winner = None
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


def utility(board, color):
    redPoints = board.rCount + board.RCount * 2
    blackPoints = board.bCount + board.BCount * 2
    if color == 'r':
        return redPoints - blackPoints
    if color == 'b':
        return blackPoints - redPoints

# def utility(board: Board, color: str):
#     redPoints = 0
#     blackPoints = 0
#
#     for piece in board.squares:
#         if piece == 'r':
#             redPoints += 1
#         if piece == 'R':
#             redPoints += 2
#         if piece == 'b':
#             redPoints += 1
#         if piece == 'B':
#             redPoints += 2
#
#     if color == 'r':
#         return redPoints - blackPoints
#     if color == 'b':
#         return blackPoints - redPoints

def terminal(board: Board):
    return board.winner is not None

def getMoves(board: Board, player):
    moves = []
    for i in range(MAX_ROW):
        for j in range(MAX_COL):
            piece: str = board.squares[i][j]
            if piece.lower == player:
                for move, skip in getValidMoves(board, piece, i, j).items():
                    pass

    return []

def getValidMoves(board, piece, row, col):
    moves = {}
    row = row
    left = col - 1
    right = col + 1
    up = ['r', 'R', 'B']
    down = ['b', 'R', 'B']
    if piece in up:
        board.squares[row - 1][col - 1]




    return moves

def tryUpLeft(board, row, col, captured = []):
    moves = {}

    newRow = row - 1
    newCol = col - 1

    if newRow < 0 or newCol < 0:
        return moves

    if board.squares[newRow][newCol] == '.':
        moves[(newRow, newCol)] = []






def moveSquare(board, row1, col1, row2, col2):
    square = board.squares[row1][col1]
    board.squares[row1][col1], board.squares[row2][col2] = board.squares[row2][col2], board.squares[row1][col1]
    # if square == 'r' and row2 == 0:
    #     square = 'R'
    # if square == 'b' and row2 == MAX_ROW:
    #     square = 'B'
    if row2 == 0 or row2 == MAX_ROW - 1:
        square.capitalize()
        if square == 'R':
            board.RCount += 1
            board.rCount -= 1
        else: # square == 'B'
            board.BCount += 1
            board.bCount -= 1



def result(board, move):
    return board

def player(board):
    return board.player

def heuristic(board):
    # Implement custom heuristic
    return utility(board)

# key: board, value: minimax val
cache = {}

def minimax(pos: Board, depth, isMax):
    # Also take color?
    # Depth limit
    # AB pruning
    # Ordering
    # Check if nextBoard in cache
    # Store value of new nextBoard into cache
    if depth == 0 or terminal(pos):
        return utility(pos, isMax), pos

    if isMax:
        minimaxMax(pos, depth)
    else:
        minimaxMin(pos, depth)

def minimaxMax(pos, depth):
    maxUtil = float('-inf')
    bestMove = None

    for move in getMoves(pos, 'r'): # TODO: decide if move == board state or something else
        util = minimax(move, depth - 1, False)[0]
        if util > maxUtil:
            maxUtil, bestMove = util, move

    return maxUtil, bestMove

def minimaxMin(pos, depth):
    minUtil = float('inf')
    bestMove = None

    for move in getMoves(pos, 'b'):
        util = minimax(move, depth - 1, True)[0]
        if util < minUtil:
            minUtil, bestMove = util, move

    return minUtil, bestMove

def readBoard(path: str):
    board = Board()
    board.player = 'r'

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


inputBoard = readBoard(sys.argv[1])
inputBoard.print()
writeBoard(inputBoard, sys.argv[2])

# outPutBoard = minimax(inputBoard)
# outputPath = sys.argv[2]