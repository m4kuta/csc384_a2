from checkers import *


inputBoard = readBoard('checkers_validate/input3.txt')
inputBoard.print()
print()

moves = getMoves(inputBoard, 'r')
for board in moves:
    board.print()
    print(utility(board))
    print()

# moves = getValidMoves(inputBoard, 'r', 4, 7)
# # for board in moves:
#     # board.print()

# util, outputBoard = cacheMinimax(inputBoard, 10, 'r', -sys.maxsize-1, sys.maxsize)
# outputBoard.print()
# print(util)
# writeBoard(outputBoard, 'output0.txt')
#
# print()
# optimalBoard = readBoard('checkers_validate/solution2.txt')
# optimalBoard.print()
# print(utility(optimalBoard))


