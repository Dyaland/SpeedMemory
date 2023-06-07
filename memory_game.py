import tkinter as tk
from random import shuffle
import os
import sqlite3
import logging

from tile import Tile
from timer import Timer
from scores import HighScore, create_memory_save, save_new_score


class MemoryGame(tk.Frame):
    """Tk frame contianing the game."""

    def __init__(self, master) -> None:
        super().__init__(master)

        # Game-wide variables
        self.match_attempts = 0  # Counter for score keeping
        self.game_tiles = []  # Container for tiles in a game
        self.clicked_tiles = []  # Container for clicked tiles to compare
        game_sizes = ["2x2", "4x4", "6x6", "8x8"]

        self.save_file = "save_data.db"

        # Create highscores file.
        if not os.path.exists(self.save_file):
            try:
                create_memory_save(self.save_file)
            except sqlite3.OperationalError as e:
                logging.debug(e)

        # Load the backside of the game tiles
        self.backside = tk.PhotoImage(file="tile_back.png")
        # Load 50 unique frontside images and save them to a list
        self.image_bank = []
        for file in os.listdir("memory_tiles"):
            try:
                img = tk.PhotoImage(file=f"memory_tiles/{file}")
                self.image_bank.append(img)
            except tk.TclError:
                logging.warning(f"image load failed for '{file}'")

        # Layout: Menu / Options
        options_frame = tk.Frame(self)
        options_frame.pack(pady=5)
        self.options_label = tk.Label(
            options_frame, text="\nSpeed Memory\n\nSelect game board size:\n")
        self.options_label.pack(side="top")

        self.size_selected = tk.StringVar(options_frame, game_sizes[0])
        self.size_options = tk.OptionMenu(options_frame,
                                          self.size_selected, *game_sizes)
        self.size_options.pack(side="left", padx=(30, 0), pady=10)

        self.play_button = tk.Button(options_frame, width=10, text="Play!",
                                     command=self.create_new_game)
        self.play_button.pack(side="right", pady=10)

        # Layout: Game timer, game board and bottom text
        self.board_frame = tk.Frame(self, bg="black", bd=3, relief="ridge")
        self.game_message = tk.Label(self, text="")
        self.game_message.pack(pady=5)
        self.timer_frame = tk.Frame(self)
        self.timer = Timer(self.timer_frame)
        self.pause_button = tk.Button(self.timer_frame, text=" Pause  ", state="disabled",
                                      command=self.pause)

    def create_new_game(self) -> None:
        """Hide initial options, and generate game board."""

        # Reset widgets and variables
        self.options_label.pack_forget()
        self.size_options.pack_forget()
        self.play_button.config(text="Game Menu")
        self.play_button.bind("<Button-1>", self.reset_game)
        self.game_message.config(text="Pick a tile")

        # Prep layout and generate game tiles.
        self.timer_frame.pack()
        self.timer.pack(side="left", padx=10)
        self.pause_button.pack(side="right")
        self.board_frame.pack()
        self.generate_tiles()

    def generate_tiles(self) -> None:
        """Purge any previous tilesand create new ones. Finally, place them on in the board_frame"""

        shuffle(self.image_bank)  # Shuffle the image bank

        # Creates two buttons for each tile image
        for i in range(int(self.size_selected.get()[0]) ** 2 // 2):
            for j in range(2):
                tile = Tile(self.board_frame,
                            name=f"tile{i}", frontside=self.image_bank[i], backside=self.backside, click_command=self.click_tile)
                tile.hide_image()
                self.game_tiles.append(tile)
        shuffle(self.game_tiles)

        # Place the tiles
        for i, tile in enumerate(self.game_tiles):
            y, x = divmod(i, int(self.size_selected.get()[0]))
            tile.grid(row=y, column=x, padx=2, pady=2)

    def click_tile(self, _) -> None:
        """Turn a tile and either check for match or ask for another one"""

        # Show a clicked tile's image.
        _.widget.show_image()
        self.clicked_tiles.append(_.widget)
        self.game_message.config(text="Pick another one")

        # Start the timer (only for the first click of a game.)
        if not self.timer.running:
            self.pause(self.board_frame)
            self.pause_button["state"] = "normal"

        # Match check when 2 tiles have been turned
        if len(self.clicked_tiles) == 2:
            self.compare_tiles()

        # Hide non-matching tiles when a 3rd tile is turned.
        elif len(self.clicked_tiles) == 3:
            for tile in self.clicked_tiles[:2]:
                tile.hide_image()
            self.clicked_tiles = [self.clicked_tiles[-1]]

    def pause(self, game_over=False):
        """Stops and starts the timer. Hides/shows game board accordingly."""

        # Pause the game timer.
        if self.timer.running:

            self.timer.stop()
            self.pause_button.config(text="Continue")

            # If the game is not over, hide the game board.
            if not game_over:
                self.board_frame.pack_forget()
                self.game_message.config(
                    text="Game paused. Click to continue.")

        # If the game was paused, unpause it.
        else:
            self.board_frame.pack()
            self.timer.start()
            self.game_message.config(text="Game is running again.")
            self.pause_button.config(text=" Pause  ")

    def compare_tiles(self) -> None:
        """If two turned tiles are a match, they are set to matched=True."""

        self.match_attempts += 1

        if self.clicked_tiles[0].name != self.clicked_tiles[1].name:
            self.game_message.config(text="Not a match")
            return

        else:
            for tile in self.clicked_tiles:
                tile.matched = True
            self.game_message.config(text="You got a match!")
            self.clicked_tiles = []

            if self.check_win():
                self.high_score_input()

    def check_win(self) -> bool:
        """Checks for any non-turned tiles"""

        for tile in self.game_tiles:
            if tile.matched is False:
                return False
        return True

    def high_score_input(self):
        """Asks for player input (name) in order to to save highscore."""
        self.game_message.config(
            text=f"Congratulations! You won after {self.match_attempts} tries.")
        self.pause(game_over=True)
        self.pause_button.config(state="disabled", text="Victory")

        # Layout: Submit high-score
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(pady=5)
        entry_label = tk.Label(self.entry_frame, text="Name:")
        entry_label.pack(side="left")
        self.entry_field = tk.Entry(self.entry_frame, width=8, bg="white")
        self.entry_field.pack(side="left", padx=5)
        ok_button = tk.Button(self.entry_frame, text="Submit Score",
                              command=self.show_high_score)
        ok_button.pack(side="left", padx=5)

    def show_high_score(self) -> None:
        """Save name and score in highscore db file and displays highscores"""

        # Gather game stats
        board_size = self.size_selected.get()
        user = self.entry_field.get()[:8]
        if len(user) < 3:
            return
        score = self.match_attempts
        game_time = self.timer.cget("text")

        # Save new score to sqlite db.
        new_score = dict(zip(
            ["Player", "Score", "Time"],
            [user, score, game_time]))

        try:
            save_new_score(new_score, board_size, self.save_file)
        except sqlite3.OperationalError:
            logging.warning("Save Failed")

        self.board_frame.pack_forget()
        self.entry_frame.pack_forget()
        self.timer_frame.pack_forget()
        self.game_message.pack_forget()
        # self.game_message.config(text = f"{board_size}   {user}   {score}   {game_time}")

        # Load highscore module and display scores.
        self.high_scores = HighScore(self, self.size_selected.get(), self.save_file)
        self.high_scores.pack()

    def reset_game(self, *args):
        """Simply re-creates the MemoryGame class object with the same master"""

        self.pack_forget()
        MemoryGame(self.master).pack()
        self.destroy()
