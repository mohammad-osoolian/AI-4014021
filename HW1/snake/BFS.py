from collections import deque
from operator import le
from Constants import NO_OF_CELLS
from Utility import Node
from Algorithm import Algorithm


class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def bfs(self, init, goal, snake):
        self.frontier.append(init)
        self.explored_set.append(init)
        while len(self.frontier) != 0:
            n = self.frontier.pop(0)
            if n.equal(goal):
                return n
            for neib in self.get_neighbors(n):
                if (not self.outside_boundary(neib)) and (not self.inside_body(snake, neib)) and (not (neib in self.explored_set)):
                    neib.parent = n
                    self.frontier.append(neib)
                    self.explored_set.append(neib)
                    
    def finddepth(self, node):
        d = 0
        while node.parent != None:
            d +=1
            node = node.parent
        return d

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
        if len(self.path) > 0 :
            return self.path.pop()

        self.frontier = []
        self.explored_set = []
        for i in range(NO_OF_CELLS):
            for j in range(NO_OF_CELLS):
                self.grid[i][j].parent = None

        init, goal = self.get_initstate_and_goalstate(snake)
        newgoal = self.bfs(init, goal, snake)
        if newgoal is None:
            self.frontier = []
            self.explored_set = []
            for i in range(NO_OF_CELLS):
                for j in range(NO_OF_CELLS):
                    self.grid[i][j].parent = None
            empty = self.scape(init, snake)
            if empty is None:
                return None
            next = self.get_path(empty)
            self.path = []
            return next

        next = self.get_path(newgoal)
        return next
