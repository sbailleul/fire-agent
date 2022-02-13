import pickle
from random import random, choice

from sklearn.neural_network import MLPRegressor

from constants import ACTIONS, STATES, EXPLORATION, X, Y, STATE_RADAR_FIRE_TILL, STATE_TILLS_COUNT, STATE_X_Y_POSITION
from tiles.tile import Tile


class Agent:
    __reward: float
    __last_action: str
    __last_state: Tile
    __exploration: float
    __mlp: MLPRegressor
    __learning_rate: float

    def __init__(self, environment):
        """
        :type environment: environment.Environment
        """
        self.__exploration = EXPLORATION
        self.__environment = environment
        self.__learning_rate = environment.learning_rate
        self.__discount_factor = environment.discount_factor
        self.__reward = 0.0
        self.__history = []
        self.__last_state = environment.start
        self.__last_action = None
        self.__mlp = MLPRegressor(hidden_layer_sizes=(10,),
                                  activation='logistic',
                                  solver='sgd',
                                  max_iter=1,
                                  warm_start=True,
                                  learning_rate_init=self.__learning_rate)
        self.__mlp.fit([
            [0] * (STATE_RADAR_FIRE_TILL + STATE_TILLS_COUNT + STATE_X_Y_POSITION)],
            [[0] * len(ACTIONS)
             ])

    @property
    def last_action(self) -> str:
        return self.__last_action

    @property
    def mlp(self) -> MLPRegressor:
        return self.__mlp

    @property
    def last_state(self) -> Tile:
        return self.__last_state

    @property
    def reward(self) -> float:
        return self.__reward

    @last_state.setter
    def last_state(self, value: Tile):
        self.__last_state = value

    @last_action.setter
    def last_action(self, value):
        self.__last_action = value

    @reward.setter
    def reward(self, value):
        self.__reward = value

    @property
    def history(self):
        return self.__history

    def to_pondered_vector(self, state: Tile) -> list[float]:
        vector_state = state.to_vector
        current_position = [vector_state[X] / self.__environment.columns_count,
                            vector_state[Y] / self.__environment.rows_count]
        all_types = [vector_state[i] / len(STATES) for i in range(2, len(vector_state))]
        radar = self.__environment.get_fire_direction_from_tile(state)
        return current_position + all_types + [radar[X] / self.__environment.columns_count,
                                               radar[Y] / self.__environment.rows_count]

    def update_neural(self, new_action: str, new_state: Tile, reward: float):
        maxQ = max(self.__mlp.predict([self.to_pondered_vector(new_state)])[0])
        desired = reward + self.__discount_factor * maxQ
        last_state_vector = [self.to_pondered_vector(self.last_state)]
        q_vector = self.__mlp.predict(last_state_vector)[0]
        i_action = ACTIONS.index(new_action)
        q_vector[i_action] = desired
        self.__mlp.fit(last_state_vector, [q_vector])

    # Sélectionne l'action avec la valeur la plus haute en reward
    def best_action(self):
        if random() < self.__exploration:
            self.__exploration *= 0.99
            return choice(ACTIONS)

        else:
            last_state_vector = [self.to_pondered_vector(self.last_state)]
            q_vector = self.__mlp.predict(last_state_vector)[0]
            i_best = 0
            for i in range(len(q_vector)):
                if q_vector[i] > q_vector[i_best]:
                    i_best = i
            return ACTIONS[i_best]

    def update(self, state: Tile, reward: float, action: str):
        self.update_neural(action, state, reward)
        self.last_action = action
        self.last_state = state
        self.reward += reward

    def reset(self, env):
        self.last_state = env.start
        self.__last_action = None
        self.reward = 0

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__mlp, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__mlp = pickle.load(file)

    def update_history(self):
        self.__history.append(self.reward)
