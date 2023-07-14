from importlib.resources import path
from Utility import Node
from Constants import *
from Algorithm import Algorithm


class DFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def dfs_recursive(self, init, goal, snake):
        self.explored_set.append(init)
        if init == goal:
            return
        for neib in self.get_neighbors(init):
            if not self.outside_boundary(neib) and not self.inside_body(snake, neib) and not (neib in self.explored_set):
                neib.parent = init
                self.dfs(neib, goal, snake)
    
    def dfs(self, init, goal, snake):
        self.frontier.append(init)
        while len(self.frontier) != 0:
            n = self.frontier.pop()

            if n.equal(goal):
                return n

            self.explored_set.append(n)
            neibs = self.get_neighbors(n)
            for neib in neibs:
                if (not self.outside_boundary(neib)) and (not self.inside_body(snake, neib)) and (not (neib in self.explored_set)):
                    neib.parent = n
                    self.frontier.append(neib)

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
        newgoal = self.dfs(init, goal, snake)
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
