# Derived from Kite 2048 project
# Source: https://www.youtube.com/watch?v=b4XP2IcI-Bg

import time as t
import tkinter as tk
import colors as c
import random
import argparse
from pynput.keyboard import Key, Controller
from gameboard import GameBoard
from matrix import *
from agents import ValueIterationAgent, AsynchronousValueIterationAgent, PrioritizedSweepingValueIterationAgent


class Game(tk.Frame):
    def __init__(self, agent='sync', board_size=2, win_score=32, use_cache=True):
        # board params
        self.board_size = board_size
        self.win_score = win_score
        self.board_dim = 600
        self.cell_dim = self.board_dim / self.board_size
        self.wait_time = 0.5
        self.actions = []
        random.seed(47)
        
        # initialize value iteration agent
        mdp = GameBoard(self.board_size, self.win_score)
        if agent == 'sync':
            self.agent = ValueIterationAgent(mdp, use_cache=use_cache)
        elif agent == 'async':
            self.agent = AsynchronousValueIterationAgent(mdp, use_cache=use_cache)
        elif agent == 'sweeping':
            self.agent = PrioritizedSweepingValueIterationAgent(mdp, use_cache=use_cache)
        else:
            raise ValueError(f'Invalid agent type: {agent}')

        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=self.board_dim, height=self.board_dim
        )
        self.main_grid.grid(pady=(100, 0))
        self.make_gui()
        self.start_game()

        self.master.bind('<Left>', self.left_handler)
        self.master.bind('<Right>', self.right_handler)
        self.master.bind('<Up>', self.up_handler)
        self.master.bind('<Down>', self.down_handler)

        self.make_move()

        self.mainloop()

    @staticmethod
    def delete_label(label):
        label.pack_forget()

    def make_gui(self):
        self.cells = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=self.cell_dim,
                    height=self.cell_dim
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {
                    'frame': cell_frame,
                    'number': cell_number
                }
                row.append(cell_data)
            self.cells.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor='center')
        tk.Label(
            score_frame,
            text='Score',
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text='0', font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * self.board_size for _ in range(self.board_size)]

        # select two random cells to initialize as 2
        row = random.randint(0, self.board_size-1)
        col = random.randint(0, self.board_size-1)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text='2'
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, self.board_size-1)
            col = random.randint(0, self.board_size-1)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text='2'
        )
        self.score = 0

    def make_move(self):
        keyboard = Controller()
        policy = self.agent.get_policy(self.matrix)

        # takes the policy, presses the assigned key, and adds the action to a list
        t.sleep(self.wait_time)
        print(f'Policy: {policy}')

        # perform policy action
        if policy == 'up':
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        elif policy == 'down':
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        elif policy == 'left':
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        elif policy == 'right':
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        else:
            raise ValueError(f'Invalid policy {policy}')

        self.actions.append(policy)
        t.sleep(self.wait_time)

        self.update_idletasks()

    def add_new_tile(self):
        row = random.randint(0, self.board_size - 1)
        col = random.randint(0, self.board_size - 1)
        while self.matrix[row][col] != 0:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
        self.matrix[row][col] = random.choice([2, 4])

    def update_gui(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell_val = self.matrix[i][j]
                if cell_val == 0:
                    self.cells[i][j]['frame'].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]['number'].configure(bg=c.EMPTY_CELL_COLOR, text='')
                else:
                    self.cells[i][j]['frame'].configure(bg=c.CELL_COLORS[cell_val])
                    self.cells[i][j]['number'].configure(
                        bg=c.CELL_COLORS[cell_val],
                        fg=c.CELL_NUMBER_COLORS[cell_val],
                        font=c.CELL_NUMBER_FONTS[cell_val],
                        text=str(cell_val)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left_handler(self, event):
        if horizontal_move_exists(self.matrix):
            self.matrix, score_increment = left(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            if not self.check_game_over():
                self.make_move()
            else:
                print(f'Agent policy: {self.actions}')

    def right_handler(self, event):
        if horizontal_move_exists(self.matrix):
            self.matrix, score_increment = right(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            if not self.check_game_over():
                self.make_move()
            else:
                print(f'Agent policy: {self.actions}')

    def up_handler(self, event):
        if vertical_move_exists(self.matrix):
            self.matrix, score_increment = up(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            if not self.check_game_over():
                self.make_move()
            else:
                print(f'Agent policy: {self.actions}')

    def down_handler(self, event):
        if vertical_move_exists(self.matrix):
            self.matrix, score_increment = down(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            if not self.check_game_over():
                self.make_move()
            else:
                print(f'Agent policy: {self.actions}')

    def check_game_over(self):
        if is_win_state(self.matrix, self.win_score):
            self.update_gui_win()
            return True
        elif is_lose_state(self.matrix):
            self.update_gui_lose()
            return True
        return False

    def update_gui_lose(self):
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(
            game_over_frame,
            text='Game over!',
            bg=c.LOSER_BG,
            fg=c.GAME_OVER_FONT_COLOR,
            font=c.GAME_OVER_FONT
        ).pack()

    def update_gui_win(self):
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(
            game_over_frame,
            text='You win!',
            bg=c.WINNER_BG,
            fg=c.GAME_OVER_FONT_COLOR,
            font=c.GAME_OVER_FONT
        ).pack()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='agent', help='Agent to use for action selection (sync, async, sweeping).', default='sync')
    parser.add_argument('-s', dest='board_size', help='Board dimension (default 2).', default=2)
    parser.add_argument('-w', dest='win_score', help='Winning score (default 32).', default=32)
    parser.add_argument('-c', dest='use_cache', help='Boolean flag to use cache.', action='store_true')
    args = parser.parse_args()

    Game(agent=args.agent, board_size=int(args.board_size), win_score=int(args.win_score), use_cache=args.use_cache)


if __name__ == '__main__':
    main()
