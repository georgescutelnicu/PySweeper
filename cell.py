from utils import play_sound


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
        self.user_puzzle_solution = 0
        self.btn = None
        self.board = board

    def reveal_cell(self, user_initiated=True):
        """
        Reveals the cell and updates its appearance.

        If the cell contains a mine, it will display the mine; otherwise, it displays the
        number of neighboring mines. If the cell has no neighboring mines, it reveals
        adjacent cells as well.

        Parameters:
        - user_initiated (bool): Indicates whether the cell reveal was initiated by the user.
          If True, a sound will be played upon revealing a non-mine cell. Default is True.
        """

        if self.board.game_is_on == 1:
            if not self.is_revealed:
                self.is_revealed = True
                if self.has_mine:
                    self.btn.config(relief="raised", image=self.board.images["py"])
                else:
                    if user_initiated and self.board.sound == "ON":
                        play_sound("sounds/reveal.wav")
                    if self.neighbor_mine_count == 0:
                        self.btn.config(image=self.board.images["0"])
                        self.board.reveal_neighbors(self.row, self.col)
                    else:
                        if self.board.difficulty != "easy":
                            self.btn.config(image=self.board.images["question"])
                            self.puzzle = self.board.puzzle_manager.set_puzzle(self.board.difficulty,
                                                                               self.neighbor_mine_count)
                        else:
                            self.btn.config(image=self.board.images[str(self.neighbor_mine_count)])
                    if self.is_flagged:
                        self.board.update_mines_label(1)

                self.board.is_game_in_progress()

            elif self.board.difficulty != "easy" and not self.has_mine and self.neighbor_mine_count > 0:
                self.board.puzzle_manager.display_window(self.board, self)

    def flag(self):
        """
        Toggles is_flag variable on or off.

        If the cell is not revealed and not already flagged, it flags the cell.
        If the cell is already flagged, it unflags it.
        """

        if self.board.game_is_on == 1:
            if not self.is_revealed and self.is_flagged:
                if self.board.sound == "ON":
                    play_sound("sounds/flag.wav")
                self.btn.config(image=self.board.images["tile"])
                self.is_flagged = False
                self.board.update_mines_label(1)
            elif int(self.board.mines_label.cget("text")) <= 0:
                return
            elif not self.is_revealed and not self.is_flagged:
                if self.board.sound == "ON":
                    play_sound("sounds/flag.wav")
                self.btn.config(image=self.board.images["flag"])
                self.is_flagged = True
                self.board.update_mines_label(-1)

    def update_cell(self, image_number):
        """
        Update the image of the cell's button, the user's puzzle solution and return to the main game window.

        Parameters:
        - image_number (str): The key corresponding to the new image in the self.images dictionary.
        """

        self.btn.config(image=self.board.images[image_number])
        self.user_puzzle_solution = int(image_number)
        self.board.display_window()
