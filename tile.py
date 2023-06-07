import tkinter as tk


class Tile(tk.Button):
    """Memory tile with name, image and matched flag."""

    def __init__(self, master, *, name, frontside, backside, click_command):
        super().__init__(master)

        self.name = name
        self.frontside = frontside
        self.backside = backside
        self.matched = False
        self.click = click_command

        self.hide_image()

    def show_image(self):
        """Shows the tile image."""
        self.config(image=self.frontside)
        self.unbind("<Button-1>")

    def hide_image(self):
        """Hides the tile image."""
        self.config(image=self.backside)
        self.bind("<Button-1>", self.click)

    def reveal(self):
        self.matched = True
