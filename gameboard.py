from mdp import MarkovDecisionProcess
from grid import Grid


LEGAL_SQUARE_VALS = ['0', '2', '4', '8']


# todo: currently only considers 2x2 grid up to value 8
class GameBoard(MarkovDecisionProcess):
    def __init__(self):
        self.state = Grid(2)
        self.initial_state = self.state

    def get_states(self):
        pass

    def get_initial_state(self):
        return self.initial_state

    def get_legal_actions(self, state):
        pass

    def get_succ_states_and_prob(self, state, action):
        pass

    def get_reward(self, state, action, succ):
        pass

    def is_terminal(self, state):
        # a state is terminal if there are no legal moves or the target value has been reached
        return self.state.contains('8') or len(self.get_legal_actions(state)) == 0
