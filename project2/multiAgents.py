# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    newFoodList = newFood.asList()
    # information
    newFoodDistList = [manhattanDistance(newPos,newFood) for newFood in newFoodList]
    newGhostPosList = [newGhost.getPosition() for newGhost in newGhostStates]
    newGhostDireList = [newGhost.getDirection() for newGhost in newGhostStates]
    newGhostDistList = [manhattanDistance(newPos,newGhostPos) for newGhostPos in newGhostPosList] 
   
    if successorGameState.isWin():
        return float("inf")
    if successorGameState.isLose():
        return -float("inf")
    closestFoodDist = min(newFoodDistList)
    closestGhostDist = min(newGhostDistList)
    if closestGhostDist == 1:
        return -float("inf")
    return successorGameState.getScore() + 1.0/closestFoodDist - 1.0/closestGhostDist 
    # might die in the middle but not influence tht result

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    # util.raiseNotDefined()
    def getMin(gameState,depth,ghostInd):
	if terminalTest(gameState,depth) == True: return self.evaluationFunction(gameState)
	value = float("inf")
	actionList = gameState.getLegalActions(ghostInd)
	numGhost = gameState.getNumAgents() - 1
        for action in actionList:
            childState = gameState.generateSuccessor(ghostInd,action)
	    if ghostInd < numGhost:
                value = min(value, getMin(childState,depth,ghostInd + 1))
	    else:
		value = min(value, getMax(childState,depth - 1))
	return value

    def getMax(gameState,depth):
        if terminalTest(gameState,depth) == True: return self.evaluationFunction(gameState)
        value = -float("inf")
        actionList = gameState.getLegalActions(0)
        for action in actionList:
            if action != Directions.STOP:
                childState = gameState.generateSuccessor(0, action)
	        value = max(value, getMin(childState,depth, 1))
	return value
    
    def terminalTest(gameState,depth):
    	return True if (gameState.isWin() == True) or (gameState.isLose() == True) or (depth == 0) else False

    actionList = gameState.getLegalActions(0)
    maxU = -float("inf")
    bestAction = actionList[0]
    for action in actionList:
    	if action != Directions.STOP:
            childState = gameState.generateSuccessor(0, action)
            res = getMin(childState,self.depth, 1)
            if res >= maxU:
          	maxU = res
          	bestAction = action
    return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    def getMin(gameState, depth, ghostInd, a, b):
        if terminalTest(gameState,depth) == True: return self.evaluationFunction(gameState)
        value = float("inf")
        actionList = gameState.getLegalActions(ghostInd)
        numGhost = gameState.getNumAgents() - 1
        for action in actionList:
            childState = gameState.generateSuccessor(ghostInd,action)
            if ghostInd < numGhost:
                value = min(value, getMin(childState,depth,ghostInd + 1, a, b))
            else:
                value = min(value, getMax(childState,depth - 1, a, b))
            if value <= a: return value
            b = min(b, value)
        return value

    def getMax(gameState, depth, a, b):
        if terminalTest(gameState,depth) == True: return self.evaluationFunction(gameState)
        value = -float("inf")
        actionList = gameState.getLegalActions(0)
        for action in actionList:
            if action != Directions.STOP:
                childState = gameState.generateSuccessor(0, action)
                value = max(value, getMin(childState,depth, 1, a, b))
                if value >= b: return value
                a = max (value, a)
        return value

    def terminalTest(gameState,depth):
        return True if (gameState.isWin() == True) or (gameState.isLose() == True) or (depth == 0) else False

    actionList = gameState.getLegalActions(0)
    maxU = -float("inf")
    bestAction = actionList[0]
    for action in actionList:
        if action != Directions.STOP:
            childState = gameState.generateSuccessor(0, action)
            res = getMin(childState,self.depth, 1, -float("inf"), float("inf"))
            if res >= maxU:
                maxU = res
                bestAction = action
    return bestAction

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
    # util.raiseNotDefined()
    def getExp(gameState, depth, ghostInd):
        if terminalTest(gameState,depth) == True: return self.evaluationFunction(gameState)
        value = 0
        actionList = gameState.getLegalActions(ghostInd)
	p = 1.0 / len(actionList)
        numGhost = gameState.getNumAgents() - 1
        for action in actionList:
            childState = gameState.generateSuccessor(ghostInd,action)
            if ghostInd < numGhost:
                value += p * getExp(childState,depth,ghostInd + 1)
            else:
                value += p * getMax(childState,depth - 1) 
        return value

    def getMax(gameState, depth):
        if terminalTest(gameState,depth) == True: return self.evaluationFunction(gameState)
        value = -float("inf")
        actionList = gameState.getLegalActions(0)
        for action in actionList:
            if action != Directions.STOP:
                childState = gameState.generateSuccessor(0, action)
                value = max(value, getExp(childState, depth, 1))
        return value

    def terminalTest(gameState,depth):
        return True if (gameState.isWin() == True) or (gameState.isLose() == True) or (depth == 0) else False

    actionList = gameState.getLegalActions(0)
    maxU = -float("inf")
    bestAction = actionList[0]
    for action in actionList:
        if action != Directions.STOP:
            childState = gameState.generateSuccessor(0, action)
            res = getExp(childState,self.depth, 1)
            if res >= maxU:
                maxU = res
                bestAction = action
    return bestAction

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  # util.raiseNotDefined()
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newCapsules = currentGameState.getCapsules()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  ghostPosList = currentGameState.getGhostPositions()
  newFoodlist = newFood.asList()
  
  FoodDist = [0]
  for position in newFoodlist:
      FoodDist.append(manhattanDistance(newPos,position))
  newGhostPos=[]
  for ghost in newGhostStates:
      newGhostPos.append(ghost.getPosition())
  GhostDist = [0]
  for position in newGhostPos:
      GhostDist.append(manhattanDistance(newPos,position))

  powerpellets = len(currentGameState.getCapsules())
  newScore = 0
  noFood = len (newFood.asList(False))
  sumScaredTimes = sum(newScaredTimes)
  sumGhostDist = sum(GhostDist)
  rFoodDist = 0
  if sum(FoodDist) > 0:
	rFoodDist = 1.0 / sum(FoodDist)
  newScore += currentGameState.getScore() + rFoodDist + noFood
  if sumScaredTimes > 0:
      newScore += sumScaredTimes + (-1 * powerpellets) + (-1 * sumGhostDist)
  else:
      newScore += sumGhostDist + powerpellets
  return newScore
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    def getMax (gameState, Depth):
      currentDepth = Depth +1
      if gameState.isWin() | gameState.isLose() | currentDepth == self.depth:
        return self.evaluationFunction(gameState)
      value = -float("inf")
      actionList = gameState.getLegalActions(0)
      for action in actionList:
        successor = gameState.generateSuccessor(0, action)
        value = max(value, getExpected(successor, 1, currentDepth))
      return value
    def getExpected (gameState, agentIndex, Depth):
      if gameState.isWin() | gameState.isLose():
        return self.evaluationFunction(gameState) 
      actions = gameState.getLegalActions(agentIndex)
      expValue = 0
      for action in actions:
        successor = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == (gameState.getNumAgents() - 1):
          value = getMax (successor, Depth)
        else:
          value = getExpected(successor, agentIndex + 1, Depth)
        expValue += value
      return float(expValue) / float(len(actionList))
    actionList = gameState.getLegalActions(0)
    Score = -float("inf")
    for action in actionList:
      successor = gameState.generateSuccessor(0, action)
      score = getExpected(successor, 1, 0)
      if score > Score:
        bestAction = action
        bestScore = score
    return bestAction
