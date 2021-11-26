import functions
import tkinter as tk
from tkinter import Frame, Label, CENTER

# constants for the gui
NUM_CELLS = 3
EDGE_LENGTH = 300
CELL_PADDING = 10
FONT = ("Verdana", 40, "bold")

TILE_COLORS = {2: "#daeddf", 4: "#9ae3ae", 8: "#6ce68d", 16: "#42ed71",
                   32: "#17e650", 64: "#17c246", 128: "#149938",
                   256: "#107d2e", 512: "#0e6325", 1024: "#0b4a1c",
                   2048: "#031f0a", 4096: "#000000", 8192: "#000000",}

LABEL_COLORS = {2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
                   32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
                   256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
                   2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0",}


# keys needed for the game
UP_KEY = "w"
LEFT_KEY = "d"
RIGHT_KEY = "a"
DOWN_KEY = "s"


class Display(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key", self.key_press)

        self.commands = {
            # TODO: add key bindings for up, right, left, down
        }

        
    def build_grid(self):
        # TODO: builds the window in tkinter

        return