# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from icecream import ic
from multiagentTestClasses import MultiagentTreeState
from util import manhattanDistance
from game import Directions, Grid
import random
import util
from pacman import GameState

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState:GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        oldPos = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        oldGhostStates = currentGameState.getGhostStates()
        oldScaredTimes = [
            ghostState.scaredTimer for ghostState in oldGhostStates]
        

        old_sum_food_dis = self.sumDistance(oldPos, oldFood.asList())
        new_sum_food_dis = self.sumDistance(newPos, newFood.asList())
        old_min_food_dis = self.minDistance(oldPos, oldFood.asList())
        new_min_food_dis = self.minDistance(newPos, newFood.asList())

        # print("old =", old_sum_food_dis, "oldPos =", oldPos)
        # print("new =", new_sum_food_dis, "newPos =", newPos)
        # print('-----------------------------')
        # print(len(self.getFoodsPos(newFood)))
        # ic(newFood.asList())
        newScore = successorGameState.getScore()
        newScore += 0.1*(old_sum_food_dis - new_sum_food_dis)
        newScore += 1000* currentGameState.getNumFood() - successorGameState.getNumFood()
        newScore += 10/self.minDistance(newPos, newFood.asList())
        newScore -= 1000*(1 if self.minDistance(newPos, successorGameState.getGhostPositions()) == 1 else 0)
        return newScore
    

    def sumDistance(self, pacmanPos, poss):
        s = 0
        for fpos in poss:
            s += manhattanDistance(pacmanPos, fpos)
        return s
    
    def minDistance(self, pacmanPos, poss):
        m = 1000000
        for fpos in poss:
            m = min(manhattanDistance(pacmanPos, fpos), m)
        return m



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nodesCount = 0


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: MultiagentTreeState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        self.nodesCount = 0
        "*** YOUR CODE HERE ***"
        # actions = gameState.getLegalActions(0)
        # maxval = self.maxValue(gameState, 0, 1)
        # for a in actions:
        #     if self.minValue(gameState.generateSuccessor(0,a), 1, 1) == maxval:
        #         return a
        v = -1000000
        act = None
        actions = gameState.getLegalActions(0)
        for a in actions:
            temp = self.minValue(gameState.generateSuccessor(0,a), 1, 1)
            if temp > v:
                v = temp
                act = a
        
        with open('MinimaxAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        return act
                
    
    def minValue(self, s:MultiagentTreeState, agent, curdepth):
        self.nodesCount+=1
        if curdepth > self.depth or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
        actions = s.getLegalActions(agent)
        v = 1000000
        if agent == s.getNumAgents()-1:
            for a in actions:
                v = min(v, self.maxValue(s.generateSuccessor(agent, a), 0, curdepth+1))
        else:
            for a in actions:
                v = min(v, self.minValue(s.generateSuccessor(agent,a), agent+1, curdepth))
        return v
             
    
    def maxValue(self, s:MultiagentTreeState, agent, curdepth):
        self.nodesCount+=1
        if curdepth > self.depth or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
        v = -1000000
        actoins = s.getLegalActions(agent)
        for a in actoins:
            v = max(v, self.minValue(s.generateSuccessor(agent,a), 1, curdepth))
        return v



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        self.nodesCount = 0
        "*** YOUR CODE HERE ***"
        # actions = gameState.getLegalActions(0)
        # maxval = self.maxValue(gameState, 0, 1, -1000000, 1000000)
        # for a in actions:
        #     if self.minValue(gameState.generateSuccessor(0,a), 1, 1, -1000000, 1000000) == maxval:
        #         return a
        v = -1000000
        alpha = -1000000
        beta = 1000000
        act = None
        actions = gameState.getLegalActions(0)
        for a in actions:
            temp = self.minValue(gameState.generateSuccessor(0,a), 1, 1, alpha, beta)
            if temp > v:
                v = temp
                act = a
            if v > beta:
                break
            alpha = max(alpha, v)
        
        with open('AlphaBetaAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        return act
    
    def minValue(self, s:MultiagentTreeState, agent, curdepth, alpha, beta):
        self.nodesCount += 1
        if curdepth > self.depth or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
        actions = s.getLegalActions(agent)
        v = 1000000
        if agent == s.getNumAgents()-1:
            for a in actions:
                v = min(v, self.maxValue(s.generateSuccessor(agent, a), 0, curdepth+1, alpha, beta))
                if v<alpha:
                    return v
                beta = min(v, beta)
        else:
            for a in actions:
                v = min(v, self.minValue(s.generateSuccessor(agent,a), agent+1, curdepth, alpha, beta))
                if v<alpha:
                    return v
                beta = min(v, beta)
        return v
             
    
    def maxValue(self, s:MultiagentTreeState, agent, curdepth, alpha, beta):
        self.nodesCount += 1
        if curdepth > self.depth or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
        v = -1000000
        actoins = s.getLegalActions(agent)
        for a in actoins:
            v = max(v, self.minValue(s.generateSuccessor(agent,a), 1, curdepth, alpha, beta))
            # print("V =",v)
            if v > beta:
                return v
            alpha = max(v, alpha)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        maxval = self.maxValue(gameState, 0, 1)
        for a in actions:
            if self.minValue(gameState.generateSuccessor(0,a), 1, 1) == maxval:
                return a
    

    def minValue(self, s:MultiagentTreeState, agent, curdepth):
        if curdepth > self.depth or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
        actions = s.getLegalActions(agent)
        sum = 0
        if agent == s.getNumAgents()-1:
            for a in actions:
                sum += self.maxValue(s.generateSuccessor(agent, a), 0, curdepth+1)
        else:
            for a in actions:
                sum += self.minValue(s.generateSuccessor(agent,a), agent+1, curdepth)
        return sum/len(actions)
             
    
    def maxValue(self, s:MultiagentTreeState, agent, curdepth):
        if curdepth > self.depth or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
        v = -1000000
        actoins = s.getLegalActions(agent)
        for a in actoins:
            v = max(v, self.minValue(s.generateSuccessor(agent,a), 1, curdepth))
        return v


def betterEvaluationFunction(currentGameState:GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    oldPos = currentGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    oldCap = currentGameState.getCapsules()
    oldGhostStates = currentGameState.getGhostStates()
    oldScaredTimes = [
        ghostState.scaredTimer for ghostState in oldGhostStates]
    

    sum_food_dis = sumDistance(oldPos, oldFood.asList())
    min_food_dis = minDistance(oldPos, oldFood.asList())
    min_cap_dis = minDistance(oldPos, oldCap)

    # print("old =", old_sum_food_dis, "oldPos =", oldPos)
    # print("new =", new_sum_food_dis, "newPos =", newPos)
    # print('-----------------------------')
    # print(len(self.getFoodsPos(newFood)))
    # ic(newFood.asList())
    newScore = currentGameState.getScore()
    newScore -= 0.1*(sum_food_dis )
    newScore += 10/min_food_dis
    newScore += 20/min_cap_dis
    # newScore -= 1000*(1 if minDistance(oldPos, currentGameState.getGhostPositions()) == 1 else 0)
    # newScore += 1000* currentGameState.getNumFood() - successorGameState.getNumFood()
    # newScore += 10/minDistance(newPos, newFood.asList())
    # newScore -= 1000*(1 if minDistance(newPos, successorGameState.getGhostPositions()) == 1 else 0)
    return newScore

def sumDistance(pacmanPos, poss):
    s = 0
    for fpos in poss:
        s += manhattanDistance(pacmanPos, fpos)
    return s

def minDistance(pacmanPos, poss):
    m = 1000000
    for fpos in poss:
        m = min(manhattanDistance(pacmanPos, fpos), m)
    return m

# Abbreviation
better = betterEvaluationFunction
