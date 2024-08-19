import tkinter as tk
import random

from utils import play_sound, open_github
from statistics import Statistics
from puzzle import PuzzleManager
from cell import Cell


class Board(tk.Tk):

    def __init__(self, difficulty, grid):
        """
        Initialize the game board.

        Parameters:
        - size (int): The size of the board. (It is chosen based on the difficulty)
        - mines (int): The number of mines to be placed on the board. (It is chosen based on the difficulty)
        """

        super().__init__()

        self.difficulty = difficulty
        self.grid = grid
        self.size = 10 if grid == "10x10" else (16 if grid == "16x16" else 20)
        self.mines = 10 if grid == "10x10" else (40 if grid == "16x16" else 70)

        self.statistics = Statistics()
        self.statistics.load_statistics()

        self.puzzle_manager = PuzzleManager()

        self.geometry(f"+{self.winfo_screenwidth() // 4}+{self.winfo_screenheight() // 8}")
        self.resizable(False, False)

        self.image_files = [
            "safe", "0", "1", "2", "3", "4", "5", "6", "7", "8",
            "question", "py", "py_green", "flag", "tile", "yellow",
            "green", "red", "timer", "icon"
        ]
        self.images = {name: tk.PhotoImage(file=f"images/{name}.png") for name in self.image_files}
        self.iconphoto(False, self.images["icon"])

        self.mines_label = None
        self.timer_label = None
        self.btn_img = None
        self.update_timer_id = None

        self.buttons = [[Cell(self, row, col) for col in range(self.size)] for row in range(self.size)]
        self.game_is_on = 1
        self.timer_value = 0

        self.create_board()
        self.create_menu()
        self.safe_tile = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        self.buttons[self.safe_tile[0]][self.safe_tile[1]].btn.config(image=self.images["safe"])

        self.update_timer()
        self.generate_mines(safe_tile=self.safe_tile)

        self.mainloop()

    def create_board(self):
        """
        Create and initialize the graphical game board with buttons and labels.
        """

        self.title("PySweeper")

        pad = self.size * 10 if self.size == 10 else (self.size * 14 if self.size == 16 else self.size * 16)

        label_frame = tk.Frame(self, relief="ridge", borderwidth=4)
        label_frame.grid(row=0, column=0, columnspan=self.size, pady=3)

        mines_img = tk.Label(label_frame, image=self.images["py"])
        mines_img.grid(row=0, column=0, sticky="w")
        self.mines_label = tk.Label(label_frame, text=self.mines, font=("normal", 15), width=3)
        self.mines_label.grid(row=0, column=1, sticky="w")

        self.timer_label = tk.Label(label_frame, text="", font=("normal", 15), width=3)
        self.timer_label.grid(row=0, column=self.size - 1, sticky="e")
        timer_img = tk.Label(label_frame, image=self.images["timer"])
        timer_img.grid(row=0, column=self.size, sticky="e")

        self.btn_img = tk.Button(label_frame, image=self.images["yellow"], command=self.restart_game)
        self.btn_img.grid(row=0, column=self.size // 2, padx=pad)

        for r in range(self.size):
            for c in range(self.size):
                button = tk.Button(self, width=40, height=40, relief="flat", borderwidth=0,
                                   command=self.buttons[r][c].reveal_cell, image=self.images["tile"])
                button.grid(row=r + 1, column=c)
                button.bind("<Button-3>", lambda event, row=r, col=c: self.buttons[row][col].flag())
                self.buttons[r][c].btn = button

    def create_menu(self):
        """
        Create the menu bar for the application.
        """

        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        difficulty_menu = tk.Menu(settings_menu, tearoff=0)
        grid_menu = tk.Menu(settings_menu, tearoff=0)
        about_menu = tk.Menu(menu_bar, tearoff=0)

        file_menu.add_command(label="New Game", command=self.restart_game)
        file_menu.add_command(label="Statistics", command=self.statistics.show_statistics)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        settings_menu.add_command(label="Reset Statistics", command=self.statistics.reset_statistics)

        for _dif in ["easy", "medium", "hard"]:
            difficulty_menu.add_radiobutton(
                label=_dif.capitalize(),
                command=lambda difficulty=_dif: self.restart_game(difficulty=difficulty, grid=self.grid)
            )
        for _grid in ["10x10", "16x16", "20x20"]:
            grid_menu.add_radiobutton(
                label=_grid,
                command=lambda grid_size=_grid: self.restart_game(difficulty=self.difficulty, grid=grid_size)
            )

        about_menu.add_command(label="Open GitHub", command=open_github)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_cascade(label="Difficulty", menu=difficulty_menu)
        settings_menu.add_cascade(label="Grid Size", menu=grid_menu)
        menu_bar.add_cascade(label="About", menu=about_menu)
        self.config(menu=menu_bar)

    def generate_mines(self, safe_tile):
        """
        Randomly generate mine locations and update neighbor mine counts.
        """

        mines_generated = []

        while len(mines_generated) < self.mines:
            mine = (tuple(random.randint(0, self.size - 1) for _ in range(2)))
            row_range = range(safe_tile[0] - 1, safe_tile[0] + 2)
            column_range = range(safe_tile[1] - 1, safe_tile[1] + 2)
            adjacent_mine = False
            for i in row_range:
                for j in column_range:
                    if (0 <= i < self.size) and (0 <= j < self.size):
                        if mine == (i, j):
                            adjacent_mine = True
                            break
            if not adjacent_mine and mine not in mines_generated:
                mines_generated.append(mine)

        for mine in mines_generated:
            self.buttons[mine[0]][mine[1]].has_mine = True
            row_range = range(mine[0] - 1, mine[0] + 2)
            column_range = range(mine[1] - 1, mine[1] + 2)
            for i in row_range:
                for j in column_range:
                    if (0 <= i < self.size) and (0 <= j < self.size):
                        self.buttons[i][j].neighbor_mine_count += 1

    def reveal_neighbors(self, row, col):
        """
        Recursively reveal neighboring cells when a cell with no neighboring mines is revealed.

        Parameters:
        - row (int): The row index of the cell.
        - col (int): The column index of the cell.
        """

        neighbors = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                r = row + i
                c = col + j
                neighbors.append((r, c))

        for n in neighbors:
            if (0 <= n[0] < self.size) and (0 <= n[1] < self.size):
                neighbor_cell = self.buttons[n[0]][n[1]]

                if not neighbor_cell.is_revealed:
                    neighbor_cell.reveal_cell(user_initiated=False)

    def check_loss(self):
        """
        Check if the game has been lost by revealing a mine.
        """

        for r in self.buttons:
            for cell in r:
                if cell.has_mine and cell.is_revealed:
                    play_sound("sounds/lose.wav")
                    self.game_is_on = 0
                    if self.difficulty != "easy":
                        self.puzzle_manager.count_puzzles_solved(self)

    def check_win(self):
        """
        Check if the game has been won by revealing all non-mine cells.
        """

        squares_discovered = 0

        for r in self.buttons:
            for cell in r:
                if not cell.has_mine and cell.is_revealed:
                    squares_discovered += 1

        if squares_discovered == ((self.size * self.size) - self.mines):
            play_sound("sounds/win.wav")
            self.game_is_on = 2
            if self.difficulty != "easy":
                self.puzzle_manager.count_puzzles_solved(self)

    def is_game_in_progress(self):
        """
        Check the current state of the game (ongoing(1), lost(0), or won(2)) and update UI accordingly.
        """

        self.check_loss()
        self.check_win()

        if self.game_is_on == 0:
            self.btn_img.config(image=self.images["red"])
            for r in self.buttons:
                for cell in r:
                    if cell.has_mine:
                        cell.btn.config(image=self.images["py_green"])
            if self.difficulty != "easy":
                self.display_alert(title="Game Over!",
                                   message=f"Total Puzzles Solved: {self.puzzle_manager.puzzles_solved}\n "
                                           f"Correct Puzzles Solved: {self.puzzle_manager.correct_puzzles_solved}")
            self.statistics.update_statistics(grid=self.grid, difficulty=self.difficulty,
                                              win=False, time_taken=self.timer_value)

        elif self.game_is_on == 2:
            self.btn_img.config(image=self.images["green"])
            for r in self.buttons:
                for cell in r:
                    if cell.has_mine:
                        cell.btn.config(image=self.images["flag"])
            self.mines_label.config(text="0")
            if self.difficulty != "easy":
                self.display_alert(title="You won!",
                                   message=f"Total Puzzles Solved: {self.puzzle_manager.puzzles_solved}\n "
                                           f"Correct Puzzles Solved: {self.puzzle_manager.correct_puzzles_solved}")
            self.statistics.update_statistics(grid=self.grid, difficulty=self.difficulty,
                                              win=True, time_taken=self.timer_value)

    def update_mines_label(self, value):
        """
        Update the mines label with the current number of flagged mines.

        Parameters:
        - value (int): The change in the number of flagged mines.
        """

        current_value = int(self.mines_label.cget("text"))
        new_value = current_value + value
        self.mines_label.config(text=str(new_value))

    def update_timer(self):
        """
        Update the timer label to display the elapsed time.
        """

        if self.game_is_on == 1:
            self.timer_label.config(text=f"{self.timer_value} ")
            self.timer_value += 1
            self.update_timer_id = self.after(1000, self.update_timer)

    def restart_game(self, difficulty=None, grid=None):
        """
        Restart the game by destroying the current window and creating a new game instance.

        Parameters:
        - difficulty (str, optional): The difficulty level for the new game. Can be "easy", "medium", or "hard".
                                      If None, the current difficulty is used.
        - grid (str, optional): The grid size for the new game. Can be "10x10", "16x16", or "20x20".
                                If None, the current grid size is used.
        """

        self.difficulty = difficulty if difficulty is not None else self.difficulty
        self.grid = grid if grid is not None else self.grid

        self.after_cancel(self.update_timer_id)
        self.destroy()
        Board(difficulty=self.difficulty, grid=self.grid)

    def display_window(self):
        """
        Display the main game window.
        """

        self.puzzle_manager.puzzle_window.destroy()
        self.deiconify()

    def display_alert(self, title, message):
        """
        Display an alert message with puzzles stats.

        Parameters:
        - title (str): The title of the alert window.
        - message (str): The message content to be displayed in the alert.
        """

        alert_window = tk.Toplevel(self)

        x = self.winfo_x() + (self.winfo_width() - 300) // 2
        y = self.winfo_y() + (self.winfo_height() - 125) // 2

        alert_window.title(title)
        alert_window.geometry("300x125")
        alert_window.geometry(f"+{x}+{y}")
        alert_window.resizable(False, False)
        alert_window.iconphoto(False, self.images["icon"])

        stats_label = tk.Label(alert_window, text=message, font=("Helvetica", 12), pady=20)
        stats_label.pack()

        ok_button = tk.Button(alert_window, text="  OK  ", command=alert_window.destroy, font=("Helvetica", 12))
        ok_button.pack()
