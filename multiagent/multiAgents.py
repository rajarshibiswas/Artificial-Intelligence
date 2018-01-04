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
        # Useful information you can extract from a
        # GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        # newGhostStates is list of ghoststate instances
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]



        "*** YOUR CODE HERE ***"
        score = 0
        foods = list(newFood.asList())
        #print currentGameState.getPacmanPosition()
        #print "newpos", newPos
        #print "newFood", newFood
        #print "newGhsotStates", newGhostStates[0]

        for ghost in newGhostStates:
            distance_to_ghost = util.manhattanDistance(newPos, ghost.getPosition())
            if (distance_to_ghost <= 1):
                # Dont take this successor if there is one ghost
                # near the pacman agent
                score -= 1e5
                return score

        closestDistance = 1e5
        for food in foods:
            distance = manhattanDistance(food, newPos) + len(foods) * 100
            if distance < closestDistance:
                closestDistance = distance
        if len(foods) == 0:
            closestDistance = 0

        score = - (closestDistance)

        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 1e2


        return score
        #return successorGameState.getScore()

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

        num_agents = gameState.getNumAgents()

        def max_value(depth, game_state):
            max_score = -1e5
            legal_actions = game_state.getLegalActions(0)

            for action in legal_actions:
                max_score = max(max_score,
                                value(depth + 1,
                                game_state.generateSuccessor(0,
                                action)))

            #print max_score
            return max_score

        def min_value(depth, game_state):
            min_score = 1e5
            ghost_index = depth % num_agents
            legal_actions = game_state.getLegalActions(ghost_index)

            for action in legal_actions:
                # print "min value node"
                min_score = min(min_score,
                    value(depth + 1,
                    game_state.generateSuccessor(ghost_index,
                    action)))

            #print min_score
            return min_score

        def value(depth, game_state):
            if (depth >= self.depth * num_agents
                or game_state.isWin()
                or game_state.isLose()): # Handle terminal state
                return self.evaluationFunction(game_state)

            if (depth % num_agents == 0): # That is agent is pacman
                return max_value(depth, game_state)
            else: # GhostSS!!!
                return min_value(depth, game_state)


        score = -1e5
        temp_score = -1e5
        legal_actions = gameState.getLegalActions(0)
        final_action = legal_actions[0]

        #print gameState.getNumAgents()

        for action in legal_actions:
            state = gameState.generateSuccessor(0, action)
            score = value(1, state)
            # print score
            if (score > temp_score):
                temp_score = score
                final_action = action

        return final_action
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):

        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        num_agents = gameState.getNumAgents()

        def max_value(depth, alpha, beta, game_state):
            max_score = -1e5
            legal_actions = game_state.getLegalActions(0)

            for action in legal_actions:
                max_score = max(max_score,
                                value(depth + 1,
                                      alpha,
                                      beta,
                                      game_state.generateSuccessor(0,
                                                    action)))

                if (max_score > beta):
                    break
                alpha = max(alpha, max_score)
#            print max_score
            return max_score

        def min_value(depth, alpha, beta, game_state):
            min_score = 1e5
            ghost_index = depth % num_agents
            legal_actions = game_state.getLegalActions(ghost_index)

            for action in legal_actions:
                # print "min value node"
                min_score = min(min_score,
                                value(depth + 1,
                                      alpha,
                                      beta,
                                      game_state.generateSuccessor(ghost_index,
                                                                   action)))
                if (min_score < alpha):
                    break
                beta = min(beta, min_score)

           # print min_score
            return min_score

        def value(depth, alpha, beta, game_state):
            if (depth >= self.depth * num_agents
                or game_state.isWin()
                or game_state.isLose()):  # Handle terminal state
                return self.evaluationFunction(game_state)

            if (depth % num_agents == 0):  # That is agent is pacman
                return max_value(depth, alpha, beta, game_state)
            else:  # GhostSS!!!
                return min_value(depth, alpha, beta, game_state)

        score = -1e5
        temp_score = -1e5
        alpha = -1e5
        beta = 1e5

        legal_actions = gameState.getLegalActions(0)
        final_action = legal_actions[0]

        # print gameState.getNumAgents()

        for action in legal_actions:
            state = gameState.generateSuccessor(0, action)
            score = value(1, alpha, beta, state)
            # print score
            if (score > temp_score):
                temp_score = score
                final_action = action
            if (score > beta):
                break
            alpha = max(alpha, score)

        return final_action
        #util.raiseNotDefined()

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
        num_agents = gameState.getNumAgents()

        def max_value(depth, game_state):
            max_score = -1e5
            legal_actions = game_state.getLegalActions(0)

            for action in legal_actions:
                max_score = max(max_score,
                                value(depth + 1,
                                      game_state.generateSuccessor(0,
                                                                   action)))

            # print max_score
            return max_score

        def min_value(depth, game_state):
            scores = []
            ghost_index = depth % num_agents
            legal_actions = game_state.getLegalActions(ghost_index)

            for action in legal_actions:
                # print "min value node"
                score = value(depth + 1,
                            game_state.generateSuccessor(ghost_index,
                            action))
                scores.append(score)
            avg_score = sum(scores)/float(len(scores))
            # print min_score
            return avg_score

        def value(depth, game_state):

            if (depth >= self.depth * num_agents
                or game_state.isWin()
                or game_state.isLose()):  # Handle terminal state
                return self.evaluationFunction(game_state)

            if (depth % num_agents == 0):  # That is agent is pacman
                return max_value(depth, game_state)
            else:  # GhostSS!!!
                return min_value(depth, game_state)

        score = -1e5
        temp_score = -1e5
        legal_actions = gameState.getLegalActions(0)
        final_action = legal_actions[0]

        # print gameState.getNumAgents()

        for action in legal_actions:
            state = gameState.generateSuccessor(0, action)
            score = value(1, state)
            # print score
            if (score > temp_score):
                temp_score = score
                final_action = action

        return final_action
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    pac_pos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    pallets = currentGameState.getCapsules()
    foods = currentGameState.getFood().asList()
    #total_ghosts = currentGameState.getNumAgents()


    # *** score from ghost ***
    score_ghost = 0
    for ghost in ghosts:
        #print ghost
        dist_ghost = util.manhattanDistance(pac_pos,
                        ghost.getPosition())
        if (ghost.scaredTimer > 0): # ghosts are scared
            score += pow(dist_ghost, 2)
        else: # Not all ghosts
            score -= pow(dist_ghost, 2)


    # *** score the pallets pellet-nabbing
    score_pallet = 0
    for pallet in pallets:
        score_pallet = 100 * min(score_pallet,
                           1.0/util.manhattanDistance(pac_pos, pallet))

    # *** Score the Food ****
    score_food = 0
    for food in foods:
        score_food =  10 * min(score_food,
                          1.0/util.manhattanDistance(pac_pos, food))


    final_score = score + score_ghost + score_pallet + score_food
    return final_score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

