# agents.py
# ----------
# Value iteration agents (synchronous, asynchronous, prioritized sweeping) used to solve MDP

from util import PriorityQueue
import pickle
import os
from matrix import *
from multiprocessing import Pool


class ValueIterationAgent:
    def __init__(self, mdp, gamma=0.9, iterations=100, pref='', use_cache=True, processes=-1):
        print('Constructing value iteration agent...')

        self.mdp = mdp
        self.gamma = gamma
        self.iterations = iterations

        self.cache_filepath = f'./out/{pref}value_iteration_agent_{self.mdp.board_size}_{self.mdp.win_score}.pkl'

        if use_cache and os.path.isfile(self.cache_filepath):
            self.load_agent()
        else:
            # initialize values of terminal states
            self.values = {}
            win_states = self.mdp.get_win_states()
            lose_states = self.mdp.get_lose_states()
            for s in win_states:
                self.values[s] = 1
            for s in lose_states:
                self.values[s] = -1
            print('Running value iteration...')
            self.run_value_iteration(processes)
            self.save_agent()

    def save_agent(self):
        with open(self.cache_filepath, 'wb') as f:
            pickle.dump(self.values, f)

    def load_agent(self):
        with open(self.cache_filepath, 'rb') as f:
            self.values = pickle.load(f)

    def evaluate(self, n):
        # perform the given number of evaluations
        print(f'Performing {n} evaluation runs...')
        win_count = 0
        for _ in range(n):
            # generate a start state
            state = generate_start_state(self.mdp.board_size)

            while not self.mdp.is_terminal(state):
                a = self.get_policy(state)
                if a == 'left':
                    state, _ = left(state)
                elif a == 'right':
                    state, _ = right(state)
                elif a == 'up':
                    state, _ = up(state)
                elif a == 'down':
                    state, _ = down(state)
                else:
                    raise ValueError(f'Invalid action: {a}')
                state = add_new_tile(state)
            if is_win_state(state, self.mdp.win_score):
                win_count += 1
        return win_count/n

    def run_value_iteration(self, processes):
        # run given num of iterations
        iter_count = 0
        if processes != -1:
            # run update calculations across multiple subprocesses
            for i in range(self.iterations):
                pool = Pool(processes)
                updated_state_vals = pool.map(self.get_updated_state_value, self.mdp.get_states())
                pool.close()
                pool.join()
                for s, new_val, op_count in updated_state_vals:
                    if s is not None:
                        self.values[s] = new_val
                        iter_count += op_count
        else:
            # run update calculations iteratively
            for i in range(self.iterations):
                # compute new value for each state on every iteration
                new_values = []
                for s in self.mdp.get_states():
                    # terminal values are known
                    if self.mdp.is_terminal(s):
                        continue

                    action_vals = []
                    actions = self.mdp.get_legal_actions(s)

                    # check all possible actions, choose one with optimal value
                    for a in actions:
                        # calculate expected value (trans prob) * (reward + discount * val(succ))
                        succ_states_and_prob = self.mdp.get_succ_states_and_prob(s, a)
                        action_val = 0
                        for succ, succ_prob in succ_states_and_prob:
                            r = self.mdp.get_reward(s, a, succ)
                            succ_val = self.values[succ] if succ in self.values else 0
                            action_val += succ_prob * (r + self.gamma * succ_val)
                            iter_count += 1
                        action_vals.append(action_val)

                    # store new state value to be updated after iteration completed
                    new_values.append((s, max(action_vals)))

                # iteration complete, update all state values
                for s, new_val in new_values:
                    self.values[s] = new_val

        print(f'Performed iterations (value iteration agent): {iter_count}')

    def get_updated_state_value(self, s):
        # terminal values are known
        if self.mdp.is_terminal(s):
            return None, None, None

        action_vals = []
        op_count = 0
        actions = self.mdp.get_legal_actions(s)

        # check all possible actions, choose one with optimal value
        for a in actions:
            # calculate expected value (trans prob) * (reward + discount * val(succ))
            succ_states_and_prob = self.mdp.get_succ_states_and_prob(s, a)
            action_val = 0
            for succ, succ_prob in succ_states_and_prob:
                r = self.mdp.get_reward(s, a, succ)
                succ_val = self.values[succ] if succ in self.values else 0
                action_val += succ_prob * (r + self.gamma * succ_val)
                op_count += 1
            action_vals.append(action_val)

        return s, max(action_vals), op_count

    def get_value(self, state):
        return self.values[state] if state in self.values else 0

    def get_q_value(self, state, action):
        q_val = 0
        for succ, succ_prob in self.mdp.get_succ_states_and_prob(state, action):
            succ_val = self.values[succ] if succ in self.values else 0
            q_val += succ_prob * (self.mdp.get_reward(state, action, succ) + self.gamma * succ_val)
        return q_val

    def get_policy(self, state):
        max_q = None
        best_a = None
        for a in self.mdp.get_legal_actions(state):
            q_a = self.get_q_value(state, a)
            if max_q is None or q_a > max_q:
                max_q = q_a
                best_a = a
        return best_a


class AsynchronousValueIterationAgent(ValueIterationAgent):
    def __init__(self, mdp, gamma=0.9, iterations=1000000, use_cache=True):
        ValueIterationAgent.__init__(self, mdp, gamma, iterations, pref='async_', use_cache=use_cache)

    def run_value_iteration(self):
        # run given num of iterations
        states = self.mdp.get_states()
        states.reverse()
        iter_count = 0
        for i in range(self.iterations):
            # get state for curr iteration
            s = states[i % len(states)]
            if self.mdp.is_terminal(s):
                continue

            # compute new value for curr state
            action_vals = []
            actions = self.mdp.get_legal_actions(s)

            # check all possible actions, choose one with optimal value
            for a in actions:
                # calculate expected value (trans prob) * (reward + discount * val(succ))
                succ_states_and_prob = self.mdp.get_succ_states_and_prob(s, a)
                action_val = 0
                for succ, succ_prob in succ_states_and_prob:
                    r = self.mdp.get_reward(s, a, succ)
                    succ_val = self.values[succ] if succ in self.values else 0
                    action_val += succ_prob * (r + self.gamma * succ_val)
                    iter_count += 1
                action_vals.append(action_val)

            # update curr state value
            self.values[s] = max(action_vals)
        print(f'Performed iterations (async value iteration agent): {iter_count}')


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    def __init__(self, mdp, gamma=0.9, iterations=1000, theta=1e-5, use_cache=True):
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, gamma, iterations, pref='sweeping_', use_cache=use_cache)

    def run_value_iteration(self):
        # 1. compute predecessors of all states
        predecessors = {}
        states = self.mdp.get_states()
        states.reverse()
        iter_count = 0
        for s in states:
            if self.mdp.is_terminal(s):
                continue

            for a in self.mdp.get_legal_actions(s):
                succ_states_and_prob = self.mdp.get_succ_states_and_prob(s, a)
                for succ, succ_prob in succ_states_and_prob:
                    iter_count += 1
                    if succ_prob > 0:
                        if succ not in predecessors:
                            predecessors[succ] = []
                        predecessors[succ].append(s)

        # 2. init empty priority queue
        pq = PriorityQueue()

        # 3. for each non-terminal state s...
        for s in states:
            if self.mdp.is_terminal(s):
                continue

            # 3a. diff = | V(s) - Q(s,a)_max |
            q_max = None
            for a in self.mdp.get_legal_actions(s):
                iter_count += 1
                q_a = self.get_q_value(s, a)
                if q_max is None or q_a > q_max:
                    q_max = q_a
            diff = abs(self.values[s] if s in self.values else 0 - q_max)

            # 3b. push s to priority queue w/ priority -diff
            pq.push(s, -diff)

        # 4. for iteration in 0->iterations-1...
        for i in range(self.iterations):
            # 4a. empty priority queue -> terminate
            if pq.isEmpty():
                print(f'Performed iterations (prioritized sweeping value iteration agent): {iter_count}')
                return

            # 4b. pop s from priority queue
            s = pq.pop()

            # 4c. update s in self.values
            # check all possible actions for max value
            action_vals = []
            actions = self.mdp.get_legal_actions(s)
            if len(actions) == 0 or self.mdp.is_terminal(s):
                self.values[s] = 0
                continue
            for a in actions:
                # for each action in the state, sum across (trans prob)*[reward + (discount)*val(s')]
                succ_states_and_prob = self.mdp.get_succ_states_and_prob(s, a)
                action_val = 0
                for succ, succ_prob in succ_states_and_prob:
                    reward = self.mdp.get_reward(s, a, succ)
                    succ_val = self.values[succ] if succ in self.values else 0
                    action_val += succ_prob * (reward + self.gamma * succ_val)
                    iter_count += 1
                action_vals.append(action_val)
            # update value function for state
            self.values[s] = max(action_vals)

            # 4d. for each predecessor p of s...
            if s in predecessors:
                for p in predecessors[s]:
                    # 4di. diff = | V(p) - Q(p,a)_max |
                    q_max = None
                    for a in self.mdp.get_legal_actions(p):
                        iter_count += 1
                        q_a = self.get_q_value(p, a)
                        if q_max is None or q_a > q_max:
                            q_max = q_a
                    diff = abs(self.values[p] if p in self.values else 0 - q_max)

                    # 4dii. diff > theta -> push p to priority queue (if not already in pq with equal of lower priority)
                    if diff > self.theta:
                        pq.update(p, -diff)
