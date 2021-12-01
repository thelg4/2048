from abc import ABC, abstractmethod


class MarkovDecisionProcess(ABC):
    @abstractmethod
    def get_states(self):
        ...

    @abstractmethod
    def get_legal_actions(self, state):
        ...

    @abstractmethod
    def get_succ_states_and_prob(self, state, action):
        ...

    @abstractmethod
    def get_reward(self, state, action, succ):
        ...

    @abstractmethod
    def is_terminal(self, state):
        ...
