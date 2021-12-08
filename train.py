# train.py
# ----------
# Trains the selected value iteration agent

import argparse
from agents import ValueIterationAgent, AsynchronousValueIterationAgent, PrioritizedSweepingValueIterationAgent
from gameboard import GameBoard


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='agent', help='Agent to use for action selection (sync, async, sweeping).', default='sync')
    parser.add_argument('-s', dest='board_size', help='Board dimension (default 2).', default=2)
    parser.add_argument('-w', dest='win_score', help='Winning score (default 32).', default=32)
    parser.add_argument('-n', dest='neval', help='Number of evaluations to perform.', default=1000)
    parser.add_argument('-p', dest='processes', help='Number of processes to run for synchronous value iteration.', default=-1)
    args = parser.parse_args()

    agent_type = args.agent
    board_size = int(args.board_size)
    win_score = int(args.win_score)
    n_eval = int(args.neval)
    processes = int(args.processes)

    # initialize value iteration agent
    mdp = GameBoard(board_size, win_score)
    if agent_type == 'sync':
        agent = ValueIterationAgent(mdp, use_cache=False, processes=processes)
    elif agent_type == 'async':
        agent = AsynchronousValueIterationAgent(mdp, use_cache=False)
    elif agent_type == 'sweeping':
        agent = PrioritizedSweepingValueIterationAgent(mdp, use_cache=False)
    else:
        raise ValueError(f'Invalid agent type: {agent_type}')

    # run evaluation on trained agent
    print(f'{agent_type} agent win rate: {agent.evaluate(n_eval)}')


if __name__ == '__main__':
    main()
