# Derived from Kite 2048 project
# Source: https://www.youtube.com/watch?v=b4XP2IcI-Bg

import time as t
import tkinter as tk
import colors as c
import random
from pynput.keyboard import Key, Controller
from gameboard import GameBoard
from matrix import *
from agents import ValueIterationAgent


BOARD_SIZE = 2
BOARD_DIM = 600
CELL_DIM = BOARD_DIM / BOARD_SIZE
WIN_SCORE = 16
WAIT_TIME = 1


class Game(tk.Frame):
    
    # list to store actions taken by the agent that lead to a win or loss
    actions = []
    
    def __init__(self):
        
        self.agent = None
        keyboard = Controller()

        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=BOARD_DIM, height=BOARD_DIM
        )
        self.main_grid.grid(pady=(100, 0))
        self.make_gui()
        self.start_game()

        self.master.bind('<Left>', self.left_handler)
        self.master.bind('<Right>', self.right_handler)
        self.master.bind('<Up>', self.up_handler)
        self.master.bind('<Down>', self.down_handler)

        self.mainloop()

    def set_agent(self, agent):
        self.agent = agent

    @staticmethod
    def delete_label(label):
        label.pack_forget()

    def make_gui(self):
        self.cells = []
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=CELL_DIM,
                    height=CELL_DIM
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
        self.matrix = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # select two random cells to initialize as 2
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text='2'
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, BOARD_SIZE-1)
            col = random.randint(0, BOARD_SIZE-1)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text='2'
        )
        self.score = 0

        mdp = GameBoard(self.matrix, BOARD_SIZE, WIN_SCORE)
        agent = ValueIterationAgent(mdp)
        self.set_agent(agent)

    def add_new_tile(self):
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)
        while self.matrix[row][col] != 0:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
        self.matrix[row][col] = random.choice([2, 4])

    def update_gui(self):
        keyboard = Controller()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
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

        policy = self.agent.get_policy(self.matrix)

        # if self.agent is not None:
        #     print(policy)        

        # takes the policy, presses the assigned key, and adds the action to a list
        if policy == None:
            # prints the actions that led to the win or loss
            print("Game Over" + "\n" + "\nPolicy found: ")
            print(*self.actions, sep = ", ")

        elif policy.__eq__("up"):
            print("Policy: " + policy)
            t.sleep(WAIT_TIME)
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            self.actions.append(policy)
            t.sleep(WAIT_TIME)
        elif policy.__eq__("down"):
            print("Policy: " + policy)
            t.sleep(WAIT_TIME)
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            self.actions.append(policy)
            t.sleep(WAIT_TIME)
        elif policy.__eq__("left"):
            print("Policy: " + policy)
            t.sleep(WAIT_TIME)
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            self.actions.append(policy)
            t.sleep(WAIT_TIME)
        elif policy.__eq__("right"):
            print("Policy: " + policy)
            t.sleep(WAIT_TIME)
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            self.actions.append(policy)
            t.sleep(WAIT_TIME)    

    def left_handler(self, event):
        if horizontal_move_exists(self.matrix):
            self.matrix, score_increment = left(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def right_handler(self, event):
        if horizontal_move_exists(self.matrix):
            self.matrix, score_increment = right(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def up_handler(self, event):
        if vertical_move_exists(self.matrix):
            self.matrix, score_increment = up(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def down_handler(self, event):
        if vertical_move_exists(self.matrix):
            self.matrix, score_increment = down(self.matrix)
            self.score += score_increment

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def check_game_over(self):
        if is_win_state(self.matrix, WIN_SCORE):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                game_over_frame,
                text='You win!',
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
        elif is_lose_state(self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                game_over_frame,
                text='Game over!',
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()


def main():
    Game()


if __name__ == '__main__':
    main()
