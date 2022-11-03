import tkinter as tk


class Timer(tk.Frame):
    """A stopwatch style timer for tkinter using its after() method"""

    def __init__(self, master):
        super().__init__(master)

        self.update_time = ""  # id for the .after method
        self.running = False
        self.hundredths = 0  # Base time counter, used for conversion to sec, min etc
        self.victory = False

        self.display = tk.Label(self, text="00:00:00",
                                font=("Monaco", 24))
        self.display.pack(side="left", padx=5)

    def format_time(self):
        """Makes time readable and update the display label"""

        sec, hun = divmod(self.hundredths, 100)
        min, sec = divmod(sec, 60)
        return f"{min:02d}:{sec:02d}:{hun:02d}"

    def start(self) -> None:
        """Starts the timer."""

        self.running = True
        self.display.after(100)  # Delay timer start by 1/10th of a sec
        self.run_timer()  # Runs the timer loop.

    def stop(self, game_over=False):
        """Stops the timer."""

        self.running = False
        self.display.after_cancel(self.update_time)  # Stops the timer

    def reset(self) -> None:
        """Resets the timer. Stops the run_timer loop if it"s running."""

        if self.running:
            self.display.after_cancel(self.update_time)
            self.running = False
        self.hundredths = 0
        self.display.config(text=f"{self.format_time()}")

    def run_timer(self) -> None:
        """Recursive timer loop. Increments by 1/100th of a second"""

        self.hundredths += 1
        self.display.config(text=self.format_time())
        self.update_time = self.display.after(10, self.run_timer)
