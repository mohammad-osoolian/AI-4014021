from hashlib import new
from Algorithm import Algorithm
import heapq as hq
from Constants import NO_OF_CELLS

class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
    
    def ASTAR(self, init, goal, snake):
        init.g = 0
        init.f = 0
        hq.heappush(self.frontier, init)
        while len(self.frontier):
            n = hq.heappop(self.frontier)
            self.explored_set.append(n)
            if n.equal(goal):
                return n

            for neib in self.get_neighbors(n):
                if (not self.inside_body(snake, neib)) and (not self.outside_boundary(neib)):
                    neib.h = self.manhattan_distance(neib, goal)
                    if n.g + 1 + neib.h < neib.f:
                        neib.parent = n
                        neib.g = n.g + 1
                        neib.f = neib.g + neib.h
                        if neib not in self.frontier:
                            hq.heappush(self.frontier, neib)
                    hq.heapify(self.frontier)

    def finddepth(self, node):
        d = 0
        while node.parent != None:
            d +=1
            node = node.parent
        return d
    
    def reset_algo(self):
        self.frontier = []
        self.explored_set = []
        for i in range(NO_OF_CELLS):
            for j in range(NO_OF_CELLS):
                self.grid[i][j].parent = None
                self.grid[i][j].f = 1000000
                self.grid[i][j].g = 0
                self.grid[i][j].h = 0


    def scape(self, init, snake):
        self.frontier.append(init)

        mostdepth = 0
        deepnode = None
        while len(self.frontier) != 0:
            n = self.frontier.pop()
            self.explored_set.append(n)
            if self.finddepth(n) > mostdepth:
                mostdepth = self.finddepth(n)
                deepnode = n
        
            neibs = self.get_neighbors(n)
            for neib in neibs:
                if (not self.outside_boundary(neib)) and (not self.inside_body(snake, neib)) and (not (neib in self.explored_set)) and neib.y < 19:
                    neib.parent = n
                    self.frontier.append(neib)
        return deepnode

    def run_algorithm(self, snake):
        if len(self.path) > 0:
            return self.path.pop()
        
        self.reset_algo()
        init, goal = self.get_initstate_and_goalstate(snake)
        newgoal = self.ASTAR(init, goal, snake)
        if newgoal is None:
            self.reset_algo()
            empty = self.scape(init, snake)
            if empty is None:
                return None
            next = self.get_path(empty)
            self.path = []
            return next
        next = self.get_path(newgoal)
        return next
