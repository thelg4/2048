from util import PriorityQueue


class ValueIterationAgent:
    def __init__(self, mdp, gamma=0.9, iterations=100):
        self.mdp = mdp
        self.gamma = gamma
        self.iterations = iterations
        self.values = {}
        self.run_value_iteration()

    def run_value_iteration(self):
        # run given num of iterations
        for i in range(self.iterations):
            new_values = []
            # compute new value for each state on every iteration
            for s in self.mdp.get_states():
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
                    action_vals.append(action_val)

                # store new state value to be updated after iteration completed
                new_values.append((s, max(action_vals)))

            # iteration complete, update all state values
            for s, new_val in new_values:
                self.values[s] = new_val

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
    def __init__(self, mdp, gamma=0.9, iterations=1000):
        ValueIterationAgent.__init__(mdp, gamma, iterations)

    def run_value_iteration(self):
        # run given num of iterations
        states = self.mdp.get_states()
        for i in range(self.iterations):
            # get state for curr iteration
            s = states[i % len(states)]

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
                action_vals.append(action_val)

            # update curr state value
            self.values[s] = max(action_vals)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    def __init__(self, mdp, gamma=0.9, iterations=100, theta=1e-5):
        self.theta = theta
        ValueIterationAgent.__init__(mdp, gamma, iterations)

    def run_value_iteration(self):
        # 1. compute predecessors of all states
        predecessors = {}
        states = self.mdp.get_states()
        for s in states:
            for a in self.mdp.get_legal_actions(s):
                succ_states_and_prob = self.mdp.get_succ_states_and_prob(s, a)
                for succ, succ_prob in succ_states_and_prob:
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
                q_a = self.get_q_value(s, a)
                if q_max is None or q_a > q_max:
                    q_max = q_a
            diff = abs(self.values[s] - q_max)

            # 3b. push s to priority queue w/ priority -diff
            pq.push(s, -diff)

        # 4. for iteration in 0->iterations-1...
        for i in range(self.iterations):
            # 4a. empty priority queue -> terminate
            if pq.isEmpty():
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
                    succ_val = self.values[succ]
                    action_val += succ_prob * (reward + self.gamma * succ_val)
                action_vals.append(action_val)
            # update value function for state
            self.values[s] = max(action_vals)

            # 4d. for each predecessor p of s...
            for p in predecessors[s]:
                # 4di. diff = | V(p) - Q(p,a)_max |
                q_max = None
                for a in self.mdp.get_legal_actions(p):
                    q_a = self.get_q_value(p, a)
                    if q_max is None or q_a > q_max:
                        q_max = q_a
                diff = abs(self.values[p] - q_max)

                # 4dii. diff > theta -> push p to priority queue (if not already in pq with equal of lower priority)
                if diff > self.theta:
                    pq.update(p, -diff)
