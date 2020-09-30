#Orignal work of Gaurav Arya (B17CS023)
#Collaborators - Shubhankar Gaikwad (B17CS052)
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


from util import manhattanDistance
from game import Directions
import random, util

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]
    def euclidean_new(self,position1, position2):
        xy1 = position1
        xy2 = position2
        return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

    def evaluationFunction(self, currentGameState, action):
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
        PacPos = successorGameState.getPacmanPosition()
        FoodList = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        GhostPosition = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        # print successorGameState
        # print newFood
        # print GhostPosition
        # print newPos
        # print newScaredTimes
        # next_food
        "*** YOUR CODE HERE ***"
        
        GhostDisfrmPac=[]
        for i in GhostPosition:
          GhostDisfrmPac.append(self.euclidean_new(i,PacPos))

        FoodDisfrmPac=[]
        for i in FoodList:
          FoodDisfrmPac.append(self.euclidean_new(i,PacPos))

        foodfrmSuccessor=[]
        for food in successorGameState.getFood().asList():
           if food:
             foodfrmSuccessor.append(food)

        if(len(FoodDisfrmPac)):
          ClosestFood=min(FoodDisfrmPac)
        else:
          ClosestFood=1

        if(len(GhostDisfrmPac)):
          ClosestGhost=min(GhostDisfrmPac)
        else:
          ClosestGhost=1
        
        if(len(newScaredTimes)):
          Scared_Time=min(newScaredTimes)
        else:
          Scared_Time=1
        

        ret=0
        ret+=successorGameState.getScore()
        if(ClosestGhost):
          ret-=2.0/ClosestGhost
        if(ClosestFood):
          ret+=2.0/ClosestFood

        if ClosestGhost < 2:
			    ret -= 50.0


        return ret+2*Scared_Time


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        
       
        return self.maximumVal(gameState,0,0)[1]
        util.raiseNotDefined()
    
    def minimumVal(self,gameState,i,depth):
      if(depth is self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
        return (self.evaluationFunction(gameState),'')
      minVal=999999999
      bestAction="min"
    
      for action in gameState.getLegalActions(i):
        if (i+1)%gameState.getNumAgents()==0:
          temp=self.maximumVal(gameState.generateSuccessor(i,action),(i+1)%gameState.getNumAgents(),depth+1)[0]
        else:
          temp=self.minimumVal(gameState.generateSuccessor(i,action),(i+1)%gameState.getNumAgents(),depth+1)[0]
        if(temp<minVal):
          minVal=temp
          bestAction=action
      return (minVal,bestAction)
    
    def maximumVal(self,gameState,i,depth):
      if(depth is self.depth*gameState.getNumAgents()or gameState.isWin() or gameState.isLose()):
        return (self.evaluationFunction(gameState),'')
      
      maxVal=-999999999
      
      bestAction="max"
      for action in gameState.getLegalActions(0):
        temp=self.minimumVal(gameState.generateSuccessor(0,action),1,depth+1)[0]
        if(temp>maxVal):
          maxVal=temp
          bestAction=action
      
      return (maxVal,bestAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maximumVal(gameState,0,0,-999999999,999999999)[1]
        util.raiseNotDefined()
    
    def minimumVal(self,gameState,i,depth,alpha,beta):
      if(depth is self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
        return (self.evaluationFunction(gameState),'')
      minVal=999999999
      bestAction="min"
    
      for action in gameState.getLegalActions(i):
        if (i+1)%gameState.getNumAgents()==0:
          temp=self.maximumVal(gameState.generateSuccessor(i,action),(i+1)%gameState.getNumAgents(),depth+1,alpha,beta)[0]
        else:
          temp=self.minimumVal(gameState.generateSuccessor(i,action),(i+1)%gameState.getNumAgents(),depth+1,alpha,beta)[0]
        if(temp<minVal):
          minVal=temp
          bestAction=action
        

        if(minVal<alpha):
          return (minVal,action)
        beta=min(minVal,beta)

      return (minVal,bestAction)
    
    def maximumVal(self,gameState,i,depth,alpha,beta):
      if(depth is self.depth*gameState.getNumAgents()or gameState.isWin() or gameState.isLose()):
        return (self.evaluationFunction(gameState),'')
      
      maxVal=-999999999
      
      bestAction="max"
      for action in gameState.getLegalActions(0):
        temp=self.minimumVal(gameState.generateSuccessor(0,action),1,depth+1,alpha,beta)[0]
        if(temp>maxVal):
          maxVal=temp
          bestAction=action


        if(maxVal>beta):
          return (maxVal,action)
        alpha=max(maxVal,alpha)


      return (maxVal,bestAction)

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

        # print (1*1.0)/2
        return self.maximumVal(gameState,0,0)[1]
        util.raiseNotDefined()
    
    def minimumVal(self,gameState,i,depth):
      if(depth is self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
        return (self.evaluationFunction(gameState),'')
      minVal=999999999
      bestAction="min"
      count=0
      temp=0
      for action in gameState.getLegalActions(i):
        if (i+1)%gameState.getNumAgents()==0:
          temp=temp+self.maximumVal(gameState.generateSuccessor(i,action),(i+1)%gameState.getNumAgents(),depth+1)[0]
        else:
          temp=temp+self.minimumVal(gameState.generateSuccessor(i,action),(i+1)%gameState.getNumAgents(),depth+1)[0]
        count=count+1
      return ((temp*1.0)/count,bestAction)
    
    def maximumVal(self,gameState,i,depth):
      if(depth is self.depth*gameState.getNumAgents()or gameState.isWin() or gameState.isLose()):
        return (self.evaluationFunction(gameState),'')
      
      maxVal=-999999999
      
      bestAction="max"
      for action in gameState.getLegalActions(0):
        temp=self.minimumVal(gameState.generateSuccessor(0,action),1,depth+1)[0]
        if(temp>maxVal):
          maxVal=temp
          bestAction=action
      
      return (maxVal,bestAction)
def euclidean_new(position1, position2):
        xy1 = position1
        xy2 = position2
        return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5
def betterEvaluationFunction(currentGameState):

    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
    PacPos = currentGameState.getPacmanPosition()
    FoodList = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    GhostPosition = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        # print successorGameState
        # print newFood
        # print GhostPosition
        # print newPos
        # print newScaredTimes
        # next_food
    "*** YOUR CODE HERE ***"
        
    GhostDisfrmPac=[]
    for i in GhostPosition:
      GhostDisfrmPac.append(euclidean_new(i,PacPos))

    FoodDisfrmPac=[]
    for i in FoodList:
      FoodDisfrmPac.append(euclidean_new(i,PacPos))

    foodfrmSuccessor=[]
    for food in currentGameState.getFood().asList():
      if food:
        foodfrmSuccessor.append(food)

    if(len(FoodDisfrmPac)):
          ClosestFood=min(FoodDisfrmPac)*10
    else:
      ClosestFood=10

    if(len(GhostDisfrmPac)):
      ClosestGhost=min(GhostDisfrmPac)*10
    else:
      ClosestGhost=10
        
    if(len(newScaredTimes)):
      Scared_Time=min(newScaredTimes)
    else:
      Scared_Time=10
        
    ret=0
    ret+=currentGameState.getScore()
    if(ClosestGhost):
      ret-=20.0/ClosestGhost
    if(ClosestFood):
      ret+=20.0/ClosestFood

    if ClosestGhost < 2:
			ret -= 50.0


        
    return ret+20*Scared_Time-len(foodfrmSuccessor)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

