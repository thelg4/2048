# 2048

An implementation of a simplified version of the 2048 game on n-dimensional, represented as a Markov Decision Process. Value iteration agents are trained to perform optimally in the modified 2048 environment.

## Organization
- `agents.py` value iteration agents for evaluating an optimal policy from an MDP
- `colors.py` hex values for GUI colors, fonts
- `game.py` driver file, handles GUI components
- `gameboard.py` representation of 2048 game as a Markov Decision Process
- `matrix.py` handles matrix operations
- `mdp.py` abstract definition of a Markov Decision Process
- `util.py` priority queue implementation from open source Berkeley AI codebase