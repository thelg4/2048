# 2048

An implementation of a simplified version of the 2048 game on 2x2 and 3x3 grids, represented as a Markov Decision Process. Value iteration agents are trained to perform optimally in the simplified 2048 environment.

## Organization
- `agents.py` value iteration agents for evaluating an optimal policy from an MDP
- `gameboard.py` representation of 2048 game as a Markov Decision Process
- `grid.py` grid representation used for storing game state
- `mdp.py` abstract definition of a Markov Decision Process
- `util.py` priority queue implementation, from open source Berkeley AI codebase