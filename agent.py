from constants import ACTIONS
from tiles.tile import Tile


class Agent:
    __reward: float
    __last_action: str
    __q_table: dict[list[tuple[tuple[int, int], str]], dict[str, float]]
    __last_state: Tile
    __last_state_resume: list[tuple[tuple[int, int], str]]

    def __init__(self, environment):
        """
        :type environment: environment.Environment
        """
        self.__reward = 0.0
        self.__last_state = environment.start
        self.__last_action = None
        self.__last_state_resume = None
        self.__q_table = {}

    @property
    def last_action(self) -> str:
        return self.__last_action

    @property
    def q_table(self) -> dict[list[tuple[tuple[int, int], str]], dict[str, float]]:
        return self.__q_table

    @property
    def last_state(self) -> Tile:
        return self.__last_state

    @property
    def reward(self) -> float:
        return self.__reward

    @last_state.setter
    def last_state(self, value: Tile):
        self.__last_state = value
        self.__last_state_resume = value.resume()

    # @property
    # def last_state_resume(self) -> list[tuple[tuple[int, int], str]]:
    #     if self.__last_state_resume is None:
    #         self.__last_state_resume = self.last_state.resume()
    #     return self.__last_state_resume

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
    def update_q_table(self, new_action: str, new_state: Tile, reward: float, learning_rate: float,
                       discount_factor: float):

        max_reward = max(self.q_table[new_state.resume()].values()) if new_state in self.q_table else 0.0
        self.set_state_if_not_exist(self.__last_state_resume)
        self.q_table[self.__last_state_resume][new_action] = self.q_table[self.__last_state_resume][
                                                                 new_action] + learning_rate * (
                                                                     reward + discount_factor * max_reward)

    # Sélectionne l'action avec la valeur la plus haute en reward
    def best_action(self):
        self.set_state_if_not_exist(self.__last_state_resume)
        actions = self.q_table.get(self.__last_state_resume)
        best_action = None
        for action in actions:
            if best_action is None or actions[action] > actions[best_action]:
                best_action = action
        return best_action

    def set_state_if_not_exist(self, state: list[tuple[tuple[int, int], str]]):
        if state not in self.q_table:
            self.__q_table[state] = {a: 0.0 for a in ACTIONS}

    def update(self, state: Tile, reward: float, action: str, learning_rate: float, discount_factor: float):
        self.update_q_table(action, state, reward, learning_rate, discount_factor)
        self.last_action = action
        self.last_state = state
        self.reward += reward

    def reset(self, env):
        self.last_state = env.start
        self.__last_action = None
        self.reward = 0
