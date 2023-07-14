class Sudoku1:
    def __init__(self, dim, board) -> None:
        self.expandNodes = 0
        self.dim = dim
        self.board = board
    
    def solveSimpleBacktracking(self):
        location = self.getNextLocation()
        if location[0] == -1:
            return True
        else:
            self.expandNodes += 1
            for choice in range(1, self.dim+1):
                if self.isSafe(location[0], location[1], choice):
                    self.board[location[0]][location[1]] = str(choice)
                    if self.solveSimpleBacktracking():
                        return True
                    self.board[location[0]][location[1]] = '0'
        return False

    def getNextLocation(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] == '0':
                    return i, j
        return (-1,-1)

    def isSafe(self, l0, l1, val):
        val = str(val)
        for i in range(self.dim):
            if self.board[i][l1] == val:
                return False
        for j in range(self.dim):
            if self.board[l0][j] == val:
                return False
        for i in range(3):
            for j in range(3):
                if self.board[i+ int(l0/3)*3][j+int(l1/3)*3] == val:
                    return False
        return True

if __name__ == "__main__":
    with open('tableLVL3.txt') as f:
                content = f.readlines()
                sudokuboard = [list(x.strip()) for x in content]


    s = Sudoku1(9, sudokuboard)
    print(s.solveSimpleBacktracking())
    for line in s.board:
        print(line)

