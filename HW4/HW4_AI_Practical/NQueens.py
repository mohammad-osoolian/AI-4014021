from random import randrange


class NQueens:
    def __init__(self, N):
        self.N = N

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))

    def goal_test(self, state):
        ''' Returns True if the given state is a goal state '''
        return self.value(state) == 0
        # the highest value is 0. other values are less than zero

    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        # the highest value is 0. other values are less than zero
        cnt = 0
        for i in range(self.N):
            for j in range(i+1, self.N):
                if not self.check_two_queens((i, state[i]), (j, state[j])):
                    cnt-=1
        return cnt

    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''
        ps = []
        for i in range(self.N):
            for j in range(self.N):
                newstate = list(state)
                newstate[i] = j
                if newstate != state:
                    ps.append(tuple(newstate))
        return ps
            
    
    def check_two_queens(self, pos1, pos2):
        if pos1[0] == pos2[0] or pos1[1] == pos2[1] or abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]):
            return False
        return True
