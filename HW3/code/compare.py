from part1 import Sudoku1
from part2 import Sudoku2
import time


def testTime(fileDir):
    with open(fileDir) as f:
        content = f.readlines()
        sudokuboard = [list(x.strip()) for x in content]
    s1 = Sudoku1(9, sudokuboard)
    now = time.time()
    print("backtracking")
    print(s1.solveSimpleBacktracking())
    then = time.time()
    for line in s1.board:
        print(line)
    print("expanded nodes:", s1.expandNodes)
    print("time:", int((then-now)*1000), 'ms\n')

    s2 = Sudoku2(9, fileDir)
    now = time.time()
    print("csp with ordering")
    print(s2.csp())
    then = time.time()
    for line in s1.board:
        print(line)
    print("expand nodes:", s2.expandNodes)
    print("time:", int((then-now)*1000), 'ms')

print("Test1\n---------------------------------------")
testTime('table.txt')
print("\nTest2\n---------------------------------------")
testTime('tableLVL2.txt')
print("\nTest3\n---------------------------------------")
testTime('tableLVL3.txt')


    

