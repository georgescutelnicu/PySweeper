import random


class Cell:

    def __init__(self, board, row, col):
        """
        Initialize a cell object.

        Parameters:
        - board (Board): The game board this cell belongs to.
        - row (int): The row index of the cell.
        - col (int): The column index of the cell.
        """

        self.row = row
        self.col = col
        self.has_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mine_count = 0
        self.puzzle = None
        self.btn = None
        self.board = board

    def set_puzzle(self):
        self.puzzle = random.choice(self.board.puzzles[self.board.difficulty][str(self.neighbor_mine_count)])

    def reveal_cell(self):
        """
        Reveals the cell and updates its appearance.

        If the cell contains a mine, it will display the mine; otherwise, it displays the
        number of neighboring mines. If the cell has no neighboring mines, it reveals
        adjacent cells as well.
        """

        if self.board.game_is_on == 1:
            if not self.is_revealed:
                self.is_revealed = True
                if self.has_mine:
                    self.btn.config(relief="raised", image=self.board.images["bomb"])
                else:
                    if self.neighbor_mine_count == 0:
                        self.btn.config(image=self.board.images["0"])
                        self.board.reveal_neighbors(self.row, self.col)
                    else:
                        self.btn.config(image=self.board.images["question"])
                        self.set_puzzle()
                    if self.is_flagged:
                        self.board.update_mines_label(1)

                self.board.is_game_in_progress()

            elif not self.has_mine and self.neighbor_mine_count > 0:
                self.board.display_puzzle_window(self)

    def flag(self):
        """
        Toggles is_flag variable on or off.

        If the cell is not revealed and not already flagged, it flags the cell.
        If the cell is already flagged, it unflags it.
        """

        if self.board.game_is_on == 1:
            if not self.is_revealed and self.is_flagged:
                self.btn.config(image=self.board.images["tile"])
                self.is_flagged = False
                self.board.update_mines_label(1)
            elif int(self.board.mines_label.cget("text")) <= 0:
                return
            elif not self.is_revealed and not self.is_flagged:
                self.btn.config(image=self.board.images["flag"])
                self.is_flagged = True
                self.board.update_mines_label(-1)
