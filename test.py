from checkers import *


inputBoard = readBoard('checkers_validate/input2.txt')
inputBoard.print()
print()

# moves = getMoves(inputBoard, 'r')
# for board in moves:
#     print(board)

# moves = getValidMoves(inputBoard, 'r', 4, 7)
# for board in moves:
#     board.print()

util, outputBoard = cacheMinimax(inputBoard, 10, 'r', float('-inf'), float('inf'))
print(util)
outputBoard.print()

print()
readBoard('checkers_validate/solution2.txt').print()

writeBoard(outputBoard, 'output0.txt')