class Sudoku2:
    def __init__(self, dim, fileDir):
        self.expandNodes = 0
        self.dim = dim
        self.fileDir = fileDir
        with open(fileDir) as f:
            content = f.readlines()
            self.board = [list(x.strip()) for x in content]
        self.rv = self.getRemainingValues()
    
    def csp(self):
        # self.rv = self.getRemainingValues()
        location = self.getNextLocation()
        if location[0] == -1:
            return True
        else:
            self.expandNodes += 1
            for choice in self.rv[location[0]][location[1]]:
                self.board[location[0]][location[1]] = str(choice)
                eddited = self.removeFromDomain(location[0], location[1], str(choice))
                if self.csp():
                    return True
                self.board[location[0]][location[1]] = '0'
                self.recoverDomain(eddited, str(choice))
        return False
    

    def forwardChecking(self, eddited):
        for cell in eddited:
            if len(self.rv[cell[0]][cell[1]]) == 0:
                return False
        return True

    def getNextLocation(self):
        bestchoice = (-1,-1)
        ops = 1000000
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] == '0':
                    if len(self.rv[i][j]) < ops:
                        bestchoice = i, j
                        ops = len(self.rv[i][j])
        return bestchoice

    def removeFromDomain(self, row, col, val):
        eddited = []
        for i in range(self.dim):
            if self.board[row][i] == '0':
                if val in self.rv[row][i]:
                    self.rv[row][i].remove(val)
                    eddited.append((row, i))
        for i in range(self.dim):
            if self.board[i][col] == '0':
                if val in self.rv[i][col]:
                    self.rv[i][col].remove(val)
                    eddited.append((i, col))
        boxRow = row - row%3
        boxCol = col - col%3
        for i in range(3):
            for j in range(3):
                if self.board[boxRow+i][boxCol+j] == '0':
                    if val in self.rv[boxRow+i][boxCol+j]:
                        self.rv[boxRow+i][boxCol+j].remove(val)
                        eddited.append((boxRow+i, boxCol+j))
        return eddited
    
    def recoverDomain(self, eddited, val):
        for cell in eddited:
            self.rv[cell[0]][cell[1]].append(val)
    
    def getDomain(self, row, col):
        RVCell = [str(i) for i in range(1, self.dim +1)]
        for i in range(self.dim):
            if self.board[row][i] != '0':
                if self.board[row][i] in RVCell:
                    RVCell.remove(self.board[row][i])
        for i in range(self.dim):
            if self.board[i][col] != '0':
                if self.board[i][col] in RVCell:
                    RVCell.remove(self.board[i][col])
        boxRow = row - row%3
        boxCol = col - col%3
        for i in range(3):
            for j in range(3):
                if self.board[boxRow+i][boxCol+j] != '0':
                    if self.board[boxRow+i][boxCol+j] in RVCell:
                        RVCell.remove(self.board[boxRow+i][boxCol+j])
        return RVCell


    def getRemainingValues(self):
        RV = [[None for i in range(self.dim)] for j in range(self.dim)]

        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row][col] != '0':
                    RV[row][col] = 'x'
                else:
                    RV[row][col] = self.getDomain(row, col)
        return RV


if __name__ == "__main__":
    s = Sudoku2(9, 'tableLVL2.txt')
    print(s.csp())
    for line in s.board:
        print(line)