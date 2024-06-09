import tkinter as tk
import random
import json


class PuzzleManager:
    def __init__(self):
        """
        Initialize the PuzzleManager.
        """

        self.puzzle_window = None
        self.puzzles_solved = 0
        self.correct_puzzles_solved = 0
        self.puzzles = self.load_puzzles("puzzles/puzzles.json")

    def load_puzzles(self, filename):
        """
        Load puzzles from a JSON file.

        Parameters:
        - filename (str): The path to the JSON file containing the puzzles.
        """

        with open(filename, "r") as file:
            return json.load(file)

    def set_puzzle(self, difficulty, neighbor_mine_count):
        """
        Set the puzzle for the cell based on the current difficulty level and neighbor mine count.

        Parameters:
        - difficulty (str): The difficulty level of the puzzle.
        - neighbor_mine_count (int): The number of neighboring mines around the cell.
        """

        return random.choice(self.puzzles[difficulty][str(neighbor_mine_count)])

    def display_window(self, board, cell):
        """
        Display a new window with a puzzle when a revealed cell is clicked.

        Parameters:
        - board (Board): The game board containing the cells.
        - cell (Cell): The cell object that was clicked.
        """

        self.puzzle_window = tk.Toplevel(board)
        self.puzzle_window.title("Puzzle")
        self.puzzle_window.geometry(f"+{board.winfo_screenwidth() // 4}+{board.winfo_screenheight() // 8}")
        self.puzzle_window.resizable(False, False)
        self.puzzle_window.protocol("WM_DELETE_WINDOW", board.display_window)
        self.puzzle_window.iconphoto(False, board.images["icon"])

        puzzle_frame = tk.Frame(self.puzzle_window)
        puzzle_frame.pack(expand=True, fill="both")

        puzzle_text = cell.puzzle
        puzzle_message = tk.Message(puzzle_frame, text=puzzle_text, font=("Consolas", 12), width=400)
        puzzle_message.pack(expand=True, fill="both")
        puzzle_height = puzzle_message.winfo_reqheight()
        self.puzzle_window.geometry(f"420x{puzzle_height + 100}")

        button_frame = tk.Frame(self.puzzle_window)
        button_frame.pack(side="bottom")

        for i in range(8):
            button = tk.Button(button_frame, width=35, height=35, relief="flat", borderwidth=0,
                               image=board.images[str(i + 1)],
                               command=lambda num=i + 1: cell.update_cell(str(num)))
            button.pack(side="left", padx=5)

        board.withdraw()

    def count_puzzles_solved(self, board):
        """
        Count the number of puzzles solved correctly.

        Parameters:
        - board (Board): The game board containing the cells.
        """

        for r in board.buttons:
            for cell in r:
                if cell.user_puzzle_solution > 0:
                    self.puzzles_solved += 1
                    if cell.neighbor_mine_count == cell.user_puzzle_solution:
                        self.correct_puzzles_solved += 1
