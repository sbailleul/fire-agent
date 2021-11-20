from abc import abstractclassmethod, abstractmethod


MAP = """
    #.#########
    #  T      #
    #  T   T  #
    #      T  #
    #  TTTTTT #
    #  T      #
    ###########
    """

UP = 'U'
LEFT = 'L'
DOWN = 'D'
RIGHT = 'R'

WATER = 'W'
CUT_TREE = 'C'

NONE = '0'

ACTIONS = [UP, DOWN, LEFT, RIGHT, 
        WATER, CUT_TREE,
        NONE]

START = '.'
LIMIT = '#'
TREE = 'T'
BURNING = 'M'
EMPTY = ' '

TREE_BURNED_REWARD = -2
BORDER_REWARD = -2
OUT_REWARD = -5
EMPTY_REWARD = -1

LEARNING_RATE = 1
DISCOUNT_FACTOR = 0.5


class Tile:

    @abstractmethod
    def endTurnAction(self):
        pass


class Tree(Tile):
    
    def endTurnAction(self):
        return super().endTurnAction()

class BurningTree(Tile):

    burningCount = 3

    @property
    def burnedToAshes(self) -> bool:
        return self.burningCount == 0 

    def endTurnAction(self):
        self.burningCount = self.burningCount - 1
        return super().endTurnAction()
    



class Environment:
    def __init__(self, text) :

        self.__states = {}

        lines = list(map(lambda x : x.strip(),  text.strip().split('\n')))

        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.__states[(row, col)] = lines[row][col]

# Définit la condition de victoire dynamiquement
                # if(lines[row][col] == GOAL):
                #     self.__goal = (row, col)


                if(lines[row][col] == START):
                    self.__start = (row, col)

    @property
    def goal(self):
        return self.__goal

    @property
    def start(self):
        return self.__start

    @property
    def states(self):
        return self.__states

    def apply(self, agent, action):
        state = agent.state
        if action == UP:
            new_state = (state[0] - 1, state[1])
        if action == DOWN:
            new_state = (state[0] + 1, state[1])
        if action == LEFT:
            new_state = (state[0], state[1] - 1)
        if action == RIGHT:
            new_state = (state[0], state[1] + 1)


        if new_state in self.states : 

            reward = None
            if self.states[new_state] == GOAL:
                reward = GOAL_REWARD
            elif self.states[new_state] in [BORDER , START]:
                reward = BORDER_REWARD
            elif self.states[new_state] == EMPTY:
                reward = EMPTY_REWARD
            

            agent.update(new_state, reward, action)
        else :
            agent.update(state, OUT_REWARD, action)

class Agent:


    def __init__(self, environment):
        self.reset_env(environment)
        self.__learning_rate = LEARNING_RATE
        self.__discount_factor = DISCOUNT_FACTOR

        self.__qtable = {}
        for s in environment.states:
            self.qtable[s] = {}
            for a in ACTIONS:
                self.qtable[s][a] = 0.0

    def reset_env(self, environment):
        self.__state = environment.start
        self.__score = 0
        self.__last_action = None

    

    def update(self, new_state, reward, action):

        # update qtable
        self.__qtable[self.__state][action] = self.__qtable[self.__state][action] + self.__learning_rate * \
            ( reward + self.__discount_factor *  \
            self.best_reward(new_state) - self.__qtable[self.__state][ action])

        self.__state = new_state
        self.__score += reward
        self.__last_action = action

     
    def best_action(self):
        rewards = self.__qtable[self.__state]

        best = None
        for r in rewards:
            if best is None or rewards[r] > rewards[best]:
                best = r 
        return best

    def best_reward(self, state):
        
        return max(self.__qtable[state].values())
    
    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score


    @property
    def qtable(self):
        return self.__qtable



if __name__ == "__main__":
    env = Environment(MAP)
    print(env.states)


    agent = Agent(env)
    while agent.state !=  env.goal:
        action = agent.best_action()
#        print(action)
        env.apply(agent, action)
#        print(agent.state, agent.score)
    print(agent.state, agent.score)
    print(agent.qtable)

    for i in range(100):
        agent.reset_env(env)
        it = 0
        while agent.state !=  env.goal:
            it += 1
            action = agent.best_action()
            env.apply(agent, action)
        print(i)
        print(agent.state, agent.score, it )
    
    
