from constants import ACTIONS
from tiles.tile import Tile


class Agent:
    __q_table: dict[tuple[int, int], dict[str, float]]

    def __init__(self, environment):
        """
        :type environment: environment.Environment
        """
        self.__reward = 0.0
        self.__last_state = environment.start
        self.__last_action = None
        self.__q_table = {}

    @property
    def last_action(self) -> str:
        return self.__last_action

    @property
    def q_table(self) -> dict[tuple[int, int], dict[str, float]]:
        return self.__q_table

    @property
    def last_state(self) -> Tile:
        return self.__last_state

    @property
    def reward(self) -> float:
        return self.__reward

    @last_state.setter
    def last_state(self, value):
        self.__last_state = value

    @q_table.setter
    def q_table(self, value):
        self.__q_table = value

    @last_action.setter
    def last_action(self, value):
        self.__last_action = value

    @reward.setter
    def reward(self, value):
        self.__reward = value

    # Mise à jour de la q_table en suivant la formule suivante du Q-Learning :
    # Q(s,a) = Q(s,a) + lr x (r + df * maxR)
    # Q : Table Q fais correspondre des états avec des actions effectuées par l'agent
    # s : L'état de l'agent
    # a : L'action de l'agent
    # lr : Taux d'apprentissage
    # r : Récompense
    # df : Taux de diminution des renforcements
    # maxR : Récompense la plus haute pour une action dans l'état s(t+1)
    def update_q_table(self, new_action: str, new_state: tuple[int, int], reward: float, learning_rate: float,
                       discount_factor: float):
        max_reward = max(self.q_table[new_state].values())
        self.q_table[self.last_state][new_action] = self.q_table[self.last_state][new_action] + learning_rate * (
                reward + discount_factor * max_reward)

    # Sélectionne l'action avec la valeur la plus haute en reward
    def best_action(self):
        if self.q_table.get(self.last_state) == None:
            self.instantiate_table(self.last_state)

        actions = self.q_table.get(self.last_state)

        best_action = None
        for action in actions:
            if best_action is None or actions[action] > actions[best_action]:
                best_action = action
        return best_action


    def instantiate_table(self, state: Tile):
        self.__q_table[state] =


    def update(self, state: tuple[int, int], reward: float, action: str, learning_rate: float, discount_factor: float):
        self.update_q_table(action, state, reward, learning_rate, discount_factor)
        self.last_action = action
        self.last_state = state
        self.reward += reward

    def reset(self, env):
        self.last_state = env.start
        self.__last_action = None
        self.reward = 0