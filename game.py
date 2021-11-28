# Derived from Kite 2048 project
# Source: https://www.youtube.com/watch?v=b4XP2IcI-Bg

import tkinter as tk
import colors as c
import random

BOARD_SIZE = 4
BOARD_DIM = 600
CELL_DIM = BOARD_DIM / BOARD_SIZE
WIN_SCORE = 2048


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=BOARD_DIM, height=BOARD_DIM
        )
        self.main_grid.grid(pady=(100, 0))
        self.make_gui()
        self.start_game()

        self.master.bind('<Left>', self.left)
        self.master.bind('<Right>', self.right)
        self.master.bind('<Up>', self.up)
        self.master.bind('<Down>', self.down)

        self.mainloop()

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

    # push all non-zero squares in a row to the left
    @staticmethod
    def stack(mat):
        stacked_mat = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            fill_pos = 0
            for j in range(BOARD_SIZE):
                if mat[i][j] != 0:
                    stacked_mat[i][fill_pos] = mat[i][j]
                    fill_pos += 1
        return stacked_mat

    # reverse matrix rows
    @staticmethod
    def reverse(mat):
        reversed_mat = []
        for i in range(BOARD_SIZE):
            reversed_mat.append([])
            for j in range(BOARD_SIZE):
                reversed_mat[i].append(mat[i][BOARD_SIZE - 1 - j])
        return reversed_mat

    # transpose matrix over its diagonal
    @staticmethod
    def transpose(mat):
        transposed_mat = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                transposed_mat[i][j] = mat[j][i]
        return transposed_mat

    # combine all adjacent equal squares to the left
    def combine(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE-1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]

    def add_new_tile(self):
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)
        while self.matrix[row][col] != 0:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
        self.matrix[row][col] = random.choice([2, 4])

    def update_gui(self):
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

    def left(self, event):
        if any(0 in row for row in self.matrix) or self.horizontal_move_exists():
            self.matrix = self.stack(self.matrix)
            self.combine()
            self.matrix = self.stack(self.matrix)

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def right(self, event):
        if any(0 in row for row in self.matrix) or self.horizontal_move_exists():
            self.matrix = self.reverse(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.combine()
            self.matrix = self.stack(self.matrix)
            self.matrix = self.reverse(self.matrix)

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def up(self, event):
        if any(0 in row for row in self.matrix) or self.vertical_move_exists():
            self.matrix = self.transpose(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.combine()
            self.matrix = self.stack(self.matrix)
            self.matrix = self.transpose(self.matrix)

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def down(self, event):
        if any(0 in row for row in self.matrix) or self.vertical_move_exists():
            self.matrix = self.transpose(self.matrix)
            self.matrix = self.reverse(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.combine()
            self.matrix = self.stack(self.matrix)
            self.matrix = self.reverse(self.matrix)
            self.matrix = self.transpose(self.matrix)

            self.add_new_tile()
            self.update_gui()
            self.check_game_over()

    def horizontal_move_exists(self):
        stacked_mat = self.stack(self.matrix)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE-1):
                if stacked_mat[i][j] == stacked_mat[i][j+1]:
                    return True
        return False

    def vertical_move_exists(self):
        stacked_transposed_mat = self.stack(self.transpose(self.matrix))
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE-1):
                if stacked_transposed_mat[i][j] == stacked_transposed_mat[i][j+1]:
                    return True
        return False

    def check_game_over(self):
        if self.is_win_state():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                game_over_frame,
                text='You win!',
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
        elif self.is_lose_state():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                game_over_frame,
                text='Game over!',
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()

    def is_win_state(self):
        return any(WIN_SCORE in row for row in self.matrix)

    def is_lose_state(self):
        return not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists()


if __name__ == '__main__':
    Game()
