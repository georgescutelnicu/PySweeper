import tkinter as tk
import winsound
import random
import json

from cell import Cell


class Board(tk.Tk):

    def __init__(self, difficulty):
        """
        Initialize the game board.

        Parameters:
        - size (int): The size of the board. (It is chosen based on the difficulty)
        - mines (int): The number of mines to be placed on the board. (It is chosen based on the difficulty)
        """

        super().__init__()

        self.difficulty = difficulty
        self.size = 10 if self.difficulty == "easy" else 16
        self.mines = 10 if self.difficulty == "easy" else 40
        self.puzzles = self.load_puzzles('puzzles/puzzles.json')
        self.puzzle_window = None
        self.geometry(f"+{self.winfo_screenwidth() // 4}+{self.winfo_screenheight() // 8}")
        self.resizable(False, False)
        self.images = {
            "safe_tile": tk.PhotoImage(file="images/safe.png"),
            "0": tk.PhotoImage(file="images/0.png"),
            "1": tk.PhotoImage(file="images/1.png"),
            "2": tk.PhotoImage(file="images/2.png"),
            "3": tk.PhotoImage(file="images/3.png"),
            "4": tk.PhotoImage(file="images/4.png"),
            "5": tk.PhotoImage(file="images/5.png"),
            "6": tk.PhotoImage(file="images/6.png"),
            "7": tk.PhotoImage(file="images/7.png"),
            "8": tk.PhotoImage(file="images/8.png"),
            "question": tk.PhotoImage(file="images/question.png"),
            "bomb": tk.PhotoImage(file="images/bomb.png"),
            "bomb_red": tk.PhotoImage(file="images/bomb_red.png"),
            "flag": tk.PhotoImage(file="images/flag.png"),
            "tile": tk.PhotoImage(file="images/tile.png"),
            "yellow": tk.PhotoImage(file="images/yellow.png"),
            "green": tk.PhotoImage(file="images/green.png"),
            "red": tk.PhotoImage(file="images/red.png"),
            "timer": tk.PhotoImage(file="images/timer.png"),
            "window_icon": tk.PhotoImage(file="images/icon.png")
        }
        self.iconphoto(False, self.images["window_icon"])

        self.mines_label = None
        self.timer_label = None
        self.btn_img = None
        self.update_timer_id = None

        self.buttons = [[Cell(self, row, col) for col in range(self.size)] for row in range(self.size)]
        self.game_is_on = 1
        self.timer_value = 0

        self.puzzles_solved = 0
        self.correct_puzzles_solved = 0

        self.create_board()
        self.safe_tile = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        self.buttons[self.safe_tile[0]][self.safe_tile[1]].btn.config(image=self.images["safe_tile"])

        self.update_timer()
        self.generate_mines(safe_tile=self.safe_tile)

        self.mainloop()

    def create_board(self):
        """
        Create and initialize the graphical game board with buttons and labels.
        """

        self.title("Minesweeper")

        pad = self.size * 10 if self.size == 10 else self.size * 14

        label_frame = tk.Frame(self, relief="ridge", borderwidth=4)
        label_frame.grid(row=0, column=0, columnspan=self.size, pady=3)

        mines_img = tk.Label(label_frame, image=self.images["bomb"])
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
                    winsound.PlaySound('sounds/lose.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
                    self.game_is_on = 0
                    self.count_puzzles_solved()

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
            winsound.PlaySound('sounds/win.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.game_is_on = 2
            self.count_puzzles_solved()

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
                        cell.btn.config(image=self.images["bomb_red"])
            self.display_alert(title="Game Over!",
                               message=f"Total Puzzles Solved: {self.puzzles_solved}\n "
                                       f"Correct Puzzles Solved: {self.correct_puzzles_solved}")

        elif self.game_is_on == 2:
            self.btn_img.config(image=self.images["green"])
            for r in self.buttons:
                for cell in r:
                    if cell.has_mine:
                        cell.btn.config(image=self.images["flag"])
            self.mines_label.config(text="0")
            self.display_alert(title="You won!",
                               message=f"Total Puzzles Solved: {self.puzzles_solved}\n "
                                       f"Correct Puzzles Solved: {self.correct_puzzles_solved}")

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

    def restart_game(self):
        """
        Restart the game by destroying the current window and creating a new game instance.
        """

        self.after_cancel(self.update_timer_id)
        self.destroy()
        Board(difficulty=self.difficulty)

    def load_puzzles(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def display_puzzle_window(self, cell):
        """
        Display a new window with a puzzle when a revealed cell is clicked.

        Parameters:
        - cell (Cell): The cell object that was clicked.
        """

        self.puzzle_window = tk.Toplevel(self)
        self.puzzle_window.title("Puzzle")
        self.puzzle_window.geometry(f"+{self.winfo_screenwidth() // 4}+{self.winfo_screenheight() // 8}")
        self.puzzle_window.resizable(False, False)
        self.puzzle_window.protocol("WM_DELETE_WINDOW", self.display_main_window)

        puzzle_frame = tk.Frame(self.puzzle_window)
        puzzle_frame.pack(expand=True, fill="both")

        puzzle_text = cell.puzzle
        puzzle_message = tk.Message(puzzle_frame, text=puzzle_text, font=("Consolas", 12), width=400, justify="center")
        puzzle_message.pack(expand=True, fill="both")
        puzzle_height = puzzle_message.winfo_reqheight()

        self.puzzle_window.geometry(f"420x{puzzle_height + 100}")

        button_frame = tk.Frame(self.puzzle_window)
        button_frame.pack(side="bottom")

        for i in range(8):
            button = tk.Button(button_frame, width=35, height=35, relief='flat', borderwidth=0,
                               image=self.images[str(i + 1)],
                               command=lambda num=i + 1: self.update_cell_image(cell, str(num)))
            button.pack(side="left", padx=5)

        self.withdraw()

    def update_cell_image(self, cell, image_number):
        """
        Update the image of the cell's button and return to the main game window.

        Parameters:
        - cell (Cell): The cell object whose button image needs to be updated.
        - image_number (str): The key corresponding to the new image in the self.images dictionary.
        """

        cell.btn.config(image=self.images[image_number])
        cell.user_puzzle_solution = int(image_number)
        self.display_main_window()

    def display_main_window(self):
        """
        Display the main game window.
        """

        self.puzzle_window.destroy()
        self.deiconify()

    def count_puzzles_solved(self):
        """
        Count the number of puzzles solved and puzzles correctly solved.
        """

        for r in self.buttons:
            for cell in r:
                if cell.user_puzzle_solution > 0:
                    self.puzzles_solved += 1
                    if cell.neighbor_mine_count == cell.user_puzzle_solution:
                        self.correct_puzzles_solved += 1

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
        alert_window.iconphoto(False, self.images['window_icon'])

        stats_label = tk.Label(alert_window, text=message, font=("Helvetica", 12), pady=20)
        stats_label.pack()

        ok_button = tk.Button(alert_window, text="  OK  ", command=alert_window.destroy, font=("Helvetica", 12))
        ok_button.pack()
