import tkinter as tk
import tkinter.ttk as ttk
import json


class Statistics:
    def __init__(self):
        """
        Initialize the Statistics object.
        """

        self.filename = "statistics/statistics.json"
        self.statistics = self.load_statistics()

    def load_statistics(self):
        """
        Load statistics from a JSON file.
        """

        with open(self.filename, 'r') as file:
            return json.load(file)

    def update_statistics(self, grid, difficulty, win, time_taken):
        """
        Update the statistics based on the outcome of a game.

        Parameters:
        - grid (str): The grid size of the game.
        - difficulty (str): The difficulty level of the game.
        - win (bool): Whether the game was won or lost.
        - time_taken (int): The time taken to complete the game.
        """

        self.statistics[grid][difficulty]["total_games_played"] += 1

        if win:
            self.statistics[grid][difficulty]["total_wins"] += 1
        else:
            self.statistics[grid][difficulty]["total_losses"] += 1

        if time_taken < self.statistics[grid][difficulty]["best_time"]:
            self.statistics[grid][difficulty]["best_time"] = time_taken

        total_games = self.statistics[grid][difficulty]["total_games_played"]
        total_wins = self.statistics[grid][difficulty]["total_wins"]
        if total_games > 0:
            win_loss_ratio = total_wins / total_games * 100
            self.statistics[grid][difficulty]["win_loss_ratio"] = f"{win_loss_ratio:.2f}%"

    def show_statistics(self):
        """
        Display statistics in a new window.
        """

        statistics_window = tk.Toplevel()
        statistics_window.title("Statistics")
        statistics_window.geometry("750x250")
        statistics_window.resizable(False, False)
        statistics_window.iconphoto(False, tk.PhotoImage(file='images/icon.png'))

        tree = ttk.Treeview(statistics_window, columns=("Total Games", "Total Wins",
                                                        "Total Losses", "Best Time", "Win/Loss Ratio"))
        tree.heading("#1", text="Total Games")
        tree.heading("#2", text="Total Wins")
        tree.heading("#3", text="Total Losses")
        tree.heading("#4", text="Best Time")
        tree.heading("#5", text="Win/Loss Ratio")

        for idx, (grid_size, grid_data) in enumerate(self.statistics.items()):
            for difficulty, stats in grid_data.items():
                tree.insert("", "end", text=f"{grid_size} / {difficulty}", values=(
                    stats["total_games_played"],
                    stats["total_wins"],
                    stats["total_losses"],
                    stats["best_time"],
                    stats["win_loss_ratio"]
                ))
            if idx < len(self.statistics) - 1:
                tree.insert("", "end", text="")

        tree.pack(expand=True, fill="both")

        for col in tree["columns"]:
            tree.column(col, anchor="center", width=100)

        statistics_window.mainloop()
