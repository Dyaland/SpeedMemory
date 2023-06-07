import tkinter as tk
from tkinter import font
import logging

from memory_game import MemoryGame


class Main(tk.Tk):
    """Class for initiating the tkinter window"""

    def __init__(self) -> None:
        super().__init__()

        # Window settings
        self.geometry('800x700+270+120')
        self.title("Speed Memory")
        self.resizable(False, False)

        # Default font and styles
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Courier New", size=16)
        self.option_add("*Font", default_font)
        self.option_add("*HighlightThickness", 0)

        MemoryGame(self).pack()


if __name__ == '__main__':
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    Main().mainloop()
