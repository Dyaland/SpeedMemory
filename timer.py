import tkinter as tk


class Timer(tk.Label):
    """A stopwatch style timer for tkinter using its after() method"""

    def __init__(self, master):
        super().__init__(master, text="00:00:00", font=("Monaco", 24))

        self.update_time = ""  # id for the .after method
        self.running = False
        self.hundredths = 0  # Base time counter, used for conversion to sec, min

    def format_time(self):
        """Makes time readable and update the display label"""

        seconds, hundredths = divmod(self.hundredths, 100)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{hundredths:02d}"

    def start(self) -> None:
        """Starts the timer."""

        self.running = True
        self.run()  # Runs the timer loop.

    def stop(self):
        """Stops the timer."""

        self.running = False
        self.after_cancel(self.update_time)  # Stops the timer

    def reset(self) -> None:
        """Resets the timer. Stops the run_timer loop if it"s running."""

        if self.running:
            self.after_cancel(self.update_time)
            self.running = False
        self.hundredths = 0
        self.config(text=f"{self.format_time()}")

    def run(self) -> None:
        """Recursive timer loop. Increments by 1/100th of a second"""

        self.hundredths += 1
        self.config(text=self.format_time())
        self.update_time = self.after(10, self.run)
