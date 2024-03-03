import tkinter as tk
import random
from cell import Cell


class Board(tk.Tk):

    def __init__(self, size, mines):
        """
        Initialize the game board.

        Parameters:
        - size (int): The size of the board. (It is chosen based on the difficulty)
        - mines (int): The number of mines to be placed on the board. (It is chosen based on the difficulty)
        """

        super().__init__()

        self.size = size
        self.mines = mines
        self.geometry(f"+{self.winfo_screenwidth() // 4}+{self.winfo_screenheight() // 8}")
        self.resizable(False, False)
        self.images = {
            'safe_tile': tk.PhotoImage(file='images/safe.png'),
            '0': tk.PhotoImage(file='images/0.png'),
            '1': tk.PhotoImage(file='images/1.png'),
            '2': tk.PhotoImage(file='images/2.png'),
            '3': tk.PhotoImage(file='images/3.png'),
            '4': tk.PhotoImage(file='images/4.png'),
            '5': tk.PhotoImage(file='images/5.png'),
            '6': tk.PhotoImage(file='images/6.png'),
            '7': tk.PhotoImage(file='images/7.png'),
            '8': tk.PhotoImage(file='images/8.png'),
            'bomb': tk.PhotoImage(file='images/bomb.png'),
            'flag': tk.PhotoImage(file='images/flag.png'),
            'tile': tk.PhotoImage(file='images/tile.png'),
            'yellow': tk.PhotoImage(file='images/yellow.png'),
            'green': tk.PhotoImage(file='images/green.png'),
            'red': tk.PhotoImage(file='images/red.png'),
            'timer': tk.PhotoImage(file='images/timer.png'),
            'window_icon': tk.PhotoImage(file='images/icon.png')
        }
        self.iconphoto(False, self.images['window_icon'])

        self.mines_label = None
        self.timer_label = None
        self.btn_img = None
        self.update_timer_id = None

        self.buttons = [[Cell(self, row, col) for col in range(size)] for row in range(size)]
        self.game_is_on = 1
        self.timer_value = 0

        self.create_board()
        self.safe_tile = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        self.buttons[self.safe_tile[0]][self.safe_tile[1]].btn.config(image=self.images['safe_tile'])

        self.update_timer()
        self.generate_mines(safe_tile=self.safe_tile)

        self.mainloop()

    def create_board(self):
        """
        Create and initialize the graphical game board with buttons and labels.
        """

        self.title("Minesweeper")

        pad = self.size * 10 if self.size == 10 else self.size * 14

        label_frame = tk.Frame(self, relief='ridge', borderwidth=4)
        label_frame.grid(row=0, column=0, columnspan=self.size, pady=3)

        mines_img = tk.Label(label_frame, image=self.images['bomb'])
        mines_img.grid(row=0, column=0, sticky='w')
        self.mines_label = tk.Label(label_frame, text=self.mines, font=('normal', 15), width=3)
        self.mines_label.grid(row=0, column=1, sticky='w')

        self.timer_label = tk.Label(label_frame, text="", font=('normal', 15), width=3)
        self.timer_label.grid(row=0, column=self.size - 1, sticky='e')
        timer_img = tk.Label(label_frame, image=self.images['timer'])
        timer_img.grid(row=0, column=self.size, sticky='e')

        self.btn_img = tk.Button(label_frame, image=self.images['yellow'], command=self.restart_game)
        self.btn_img.grid(row=0, column=self.size // 2, padx=pad)

        for r in range(self.size):
            for c in range(self.size):
                button = tk.Button(self, width=40, height=40, relief='flat', borderwidth=0,
                                   command=self.buttons[r][c].reveal_cell, image=self.images['tile'])
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
                    neighbor_cell.reveal_cell()

    def check_loss(self):
        """
        Check if the game has been lost by revealing a mine.
        """

        for r in self.buttons:
            for cell in r:
                if cell.has_mine and cell.is_revealed:
                    self.game_is_on = 0

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
                        self.game_is_on = 2

    def is_game_in_progress(self):
        """
        Check the current state of the game (ongoing(1), lost(0), or won(2)) and update UI accordingly.
        """

        self.check_loss()
        self.check_win()

        if self.game_is_on == 0:
            self.btn_img.config(image=self.images['red'])
            for r in self.buttons:
                for cell in r:
                    if cell.has_mine:
                        cell.btn.config(image=self.images['bomb'])

        elif self.game_is_on == 2:
            self.btn_img.config(image=self.images['green'])
            for r in self.buttons:
                for cell in r:
                    if cell.has_mine:
                        cell.btn.config(image=self.images['flag'])
            self.mines_label.config(text='0')

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
        Board(size=self.size, mines=self.mines)
