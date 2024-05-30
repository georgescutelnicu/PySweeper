from board import Board
from difficulty import Difficulty


if __name__ == "__main__":
    difficulty = Difficulty()
    selected_difficulty = difficulty.choose_difficulty()
    minesweeper = Board(difficulty=selected_difficulty)
