import tkinter as tk
import sqlite3
import logging


class HighScore(tk.Frame):
    """Class managing saving, loading and displaying high-score data"""

    def __init__(self, master, table_name, save_file):
        super().__init__(master)

        self.tables = ['2x2', '4x4', '6x6', '8x8']
        self.headers = ['Player', 'Score', 'Time']
        self.loaded_scores = []
        self.table_selected = table_name

        self.save_file = save_file

        # Layout: High-scores
        board_size_frame = tk.Frame(self)
        board_size_frame.pack()

        high_score_label = tk.Label(board_size_frame, text="High-score:")
        high_score_label.pack(side='left')

        self.score_choice = tk.StringVar(board_size_frame, table_name)
        score_chooser = tk.OptionMenu(board_size_frame, self.score_choice,
                                      *self.tables, command=self.load_scores)
        score_chooser.pack(side='left', padx=5)

        sort_frame = tk.Frame(self)
        sort_frame.pack()
        sort_label = tk.Label(sort_frame, text="Sort by:")
        sort_label.pack(side='left')
        self.sort_choice = tk.StringVar(sort_frame, 'Score')
        sort_chooser = tk.OptionMenu(sort_frame, self.sort_choice,
                                     *['Score', 'Time'],
                                     command=self.display_scores)
        sort_chooser.pack(side='left')

        scores_frame = tk.Frame(self)
        scores_frame.pack()
        self.scores_headers = tk.Text(scores_frame, bg='gold', bd=2,
                                      relief='raised', height=1, width=25)
        self.scores_headers.pack(side='top')
        self.scores_table = tk.Text(scores_frame, bg='gold', bd=2,
                                    relief='ridge', height=14, width=25)
        self.scores_table.pack(side='bottom')

        self.load_scores(self.table_selected)

    def load_scores(self, *_) -> None:
        """Fetch saved high-scores for selected board size"""

        table_name = self.score_choice.get()
        try:
            connection = sqlite3.connect(self.save_file)
            cursor = connection.execute(
                f"""SELECT * FROM "memory{table_name}" """)
            cursor.execute(
                f"""SELECT * FROM "memory{table_name}" ORDER BY Score """)
            self.loaded_scores = [[i for i in row]
                                  for row in cursor.fetchall()]
            self.display_scores(table_name)
        except Exception as e:
            logging.debug(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    def display_scores(self, *_) -> None:
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


def save_new_score(new_score, table_name, save_file) -> None:
    """Saves a row of new high-score data"""
    try:
        connection = sqlite3.connect(save_file)
        cursor = connection.cursor()
        headers = tuple(([key for key in new_score]))
        data_row = tuple([new_score[key] for key in new_score])
        cursor.execute(
            f"""INSERT INTO "memory{table_name}" {headers} VALUES {data_row}""")
        connection.commit()
    except Exception as e:
        logging.debug(e)
        raise
    finally:
        if connection:
            cursor.close()
            connection.close()


def create_memory_save(save_file) -> None:
    """Create high score save file if none exists"""

    try:
        connection = sqlite3.connect(save_file)
        cursor = connection.cursor()

        for table in ["2x2", "4x4", "6x6", "8x8"]:
            cursor.execute(
                f"""CREATE TABLE "memory{table}"(Player TEXT, Score INT, Time TEXT)""")

    except Exception as e:
        print("broken")
        logging.debug(e)
        raise
    finally:
        if connection:
            cursor.close()
            connection.close()
