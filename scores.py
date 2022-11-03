import tkinter as tk
import sqlite3


class HighScore(tk.Frame):
    """Class managing saving, loading and displaying high-score data"""

    def __init__(self, master, table_name):
        super().__init__(master)

        self.tables = ['2x2', '4x4', '6x6', '8x8']
        self.headers = ['Player', 'Score', 'Time']
        self.loaded_scores = []
        self.table_selected = table_name

        # Default styles
        self.hs_font = {"font": ("Monaco", 20)}

        # Layout: High-scores
        top_frame = tk.Frame(self)
        top_frame.pack()

        hs_label = tk.Label(top_frame, text="High-score:")
        hs_label.pack(side='left')

        self.score_choice = tk.StringVar(top_frame, table_name)
        score_chooser = tk.OptionMenu(top_frame, self.score_choice,
                                      *self.tables, command=self.load_scores)
        score_chooser.pack(side='left', padx=5)

        sort_frame = tk.Frame(self)
        sort_frame.pack()
        sort_label = tk.Label(sort_frame, text="Sort by:")
        sort_label.pack(side='left')
        self.sort_choice = tk.StringVar(sort_frame, 'Score')
        sort_chooser = tk.OptionMenu(sort_frame, self.sort_choice,
                                     *['Score', 'Time'],
                                     command=self.update_scores)
        sort_chooser.pack(side='left')

        scores_frame = tk.Frame(self)
        scores_frame.pack()
        self.scores_headers = tk.Text(scores_frame, bg='gold', bd=2,
                                      relief='raised', height=1, width=25)
        self.scores_headers.pack(side='top')
        self.scores_table = tk.Text(scores_frame, bg='gold', bd=2,
                                    relief='ridge', height=14, width=25)
        self.scores_table.pack(side='bottom')

    def load_scores(self, *_) -> None:
        """Fetch saved high-scores for selected board size"""

        table_name = self.score_choice.get()

        with sqlite3.connect("save_data.db") as connection:
            cursor = connection.execute(
                f"""SELECT * FROM "memory{table_name}" """)
            cursor.execute(
                f"""SELECT * FROM "memory{table_name}" ORDER BY Score """)
            self.loaded_scores = [[i for i in row]
                                  for row in cursor.fetchall()]

        self.update_scores(table_name)

    def update_scores(self, *_) -> None:
        """run the sorter, format data into strings and display in respective Text widget"""

        sorted_scores = self.sort_scores()

        headers_str = f" {self.headers[0].center(8)} {self.headers[1].center(5)} {self.headers[2].center(8)}"

        # Format the data into strings
        scores_str = ""
        for row in sorted_scores:
            row_str = f" {row[0].center(8)} {str(row[1]).center(5)} {row[2]}\n"
            scores_str += row_str

        # self.score_choice.set(table_name)
        self.scores_table['state'] = 'normal'

        for widget in [self.scores_headers, self.scores_table]:
            widget.config(state="normal")
            widget.delete('1.0', "end")

        self.scores_headers.insert('1.0', headers_str)
        self.scores_table.insert('1.0', scores_str)
        self.scores_table['state'] = 'disabled'

    def sort_scores(self) -> list:
        """Sort scores by selected header index"""
        return sorted(self.loaded_scores, key=lambda x: x[self.headers.index(self.sort_choice.get())])


def save_new_score(new_score, table_name) -> None:
    """Saves a row of new high-score data"""

    with sqlite3.connect("save_data.db") as connection:
        cursor = connection.cursor()
        header_string = ", ".join([keys for keys in new_score])
        data_row = tuple([new_score[keys] for keys in new_score])
        cursor.execute(
            f"""INSERT INTO "memory{table_name}" ({header_string}) VALUES {data_row}""")
        connection.commit()


def create_memory_save() -> None:
    """Create data tables for the memory game high scores"""

    default_high_score = ('hi-score', 999, '59:59:99'),

    with sqlite3.connect("save_data.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            """CREATE TABLE "memory2x2"(Player TEXT, Score INT, Time TEXT)""")
        cursor.executemany(
            """INSERT INTO "memory2x2" VALUES(?, ?, ?);""", default_high_score)

        cursor.execute(
            """CREATE TABLE "memory4x4"(Player TEXT, Score INT, Time TEXT)""")
        cursor.executemany(
            """INSERT INTO "memory4x4" VALUES(?, ?, ?);""", default_high_score)

        cursor.execute(
            """CREATE TABLE "memory6x6"(Player TEXT, Score INT, Time TEXT)""")
        cursor.executemany(
            """INSERT INTO "memory6x6" VALUES(?, ?, ?);""", default_high_score)

        cursor.execute(
            """CREATE TABLE "memory8x8"(Player TEXT, Score INT, Time TEXT)""")
        cursor.executemany(
            """INSERT INTO "memory8x8" VALUES(?, ?, ?);""", default_high_score)
