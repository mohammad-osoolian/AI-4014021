from NQueens import NQueens

def hill_climbing(problem: NQueens):
    ''' Returns a state as the solution of the problem '''
    curstate = problem.initial()
    nextstate = curstate
    while True:
        if problem.goal_test(curstate):
            print(curstate)
            return curstate
        for neib in problem.neighbors(curstate):
            if problem.value(neib) > problem.value(nextstate):
                nextstate = neib
        if nextstate == curstate:
            return nextstate
        curstate = nextstate



def hill_climbing_random_restart(problem, limit = 10):
    state = problem.initial()
    cnt = 0
    while problem.goal_test(state) == False and cnt < limit:
        state = hill_climbing(problem)
        cnt += 1
    return state
