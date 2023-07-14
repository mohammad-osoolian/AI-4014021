import random

class TrainedData:
    """ This class is used to writed trained data in text file
        and read data from files for the test. """

    def __init__(self, Qpath="Q.txt"):
        self.Qpath = Qpath
    
    def writeData(self, Q):
        with open(self.Qpath, 'w') as file:
            for item in Q.items():
                file.write(str(item[0][0]) + " - " + str(item[0][1]) + " = " + str(item[1]) + '\n')
    
    def readData(self):
        try:
            with open(self.Qpath, 'r') as file:
                Q = {}
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split(' = ')
                    value = float(value.strip())
                    s, a = key.strip().split(' - ')
                    s = tuple([float(_.strip(' ()')) for _ in s.strip().split(',')])
                    a = tuple([float(_.strip(' ()')) for _ in a.strip().split(',')])
                    Q[(s, a)] = value
        except:
            Q = {}
        return Q


class Discretizer:
    """ this class is used to descretize continues values of
        observations and actions. it also has methods to descretize
        actions spaces """

    def __init__(self, sstep, astep, actionRange):
        self.sstep = sstep
        self.astep = astep
        self.actionRange = actionRange
    
    def round(self, value, step=1):
        factor = 1/step
        if factor != int(factor):
            raise Exception("step is not a counter of 1")
        return round(value*factor)/factor
    
    def roundValues(self, values, step=1):
        return [self.round(_, step) for _ in values]
    
    def discretizeRange(self, rng:tuple, step):
        disrng = []
        i = rng[0]
        while i <= rng[1]:
            disrng.append(self.round(i, step))
            i+=step
        return disrng

    def roundState(self, s):
        return self.roundValues(s, self.sstep)
    
    def roundAction(self, a):
        return self.roundValues(a, self.astep)
    
    def discreteActionRange(self):
        return self.discretizeRange(self.actionRange, self.astep)


class QLearning:
    """ this class has the main functionalities of the Qlearning
        algorithm. """

    def __init__(self, alpha, gamma, epsilon, Q:dict, dis:Discretizer):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.Q = Q
        self.dis = dis
    
    def makeActionSpace(self):
        actionSpace = []
        actionRng = self.dis.discreteActionRange()
        for joint1 in actionRng:
            for joint2 in actionRng:
                for joint3 in actionRng:
                    for joint4 in actionRng:
                        actionSpace.append((joint1, joint2, joint3, joint4))
        return actionSpace

    def optimalAction(self, s):
        actionSpace = self.makeActionSpace()
        optact = actionSpace[-1]
        maxQ = self.Q.get((s,optact), 0)
        for a in actionSpace:
            if self.Q.get((s,a), 0) > maxQ:
                maxQ = self.Q.get((s,a), 0)
                optact = a
        return optact, maxQ

    def sample(self, r, sp):
        ap, maxQ = self.optimalAction(sp) 
        return r + self.gamma*maxQ
    
    def extractState(self, observation):
        return tuple(self.dis.roundState(observation)[:14])
    
    def extractAction(self, action):
        return tuple(self.dis.roundAction(action))
    
    def updateQ(self, s, a, r, sp):
        samp = self.sample(r, sp)
        self.Q[(s,a)] = (1-self.alpha)*self.Q.get((s,a), 0) + self.alpha*samp
        return self.Q[(s,a)]

    def randomAction(self):
        actionSpace = self.makeActionSpace()
        return random.choice(actionSpace)
    
    def pickAction(self, s):
        coin = random.random()
        # self.epsilon *= 0.9997
        # print(self.epsilon)
        if coin < self.epsilon:
            return self.randomAction()
        else:
            a, maxQ = self.optimalAction(s)
            return a

