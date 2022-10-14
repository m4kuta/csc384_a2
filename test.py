from checkers import *


inputBoard = readBoard('checkers_validate/input0.txt')
inputBoard.print()
print()

moves = getMoves(inputBoard, 'r')
for board in moves:
    print(board)
