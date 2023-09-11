from board import Board
from difficulty import Difficulty


if __name__ == "__main__":
    difficulty = Difficulty()
    selected_difficulty = difficulty.choose_difficulty()

    if not selected_difficulty or selected_difficulty == 'easy':
        size = 10
        mines = 10
    elif selected_difficulty == 'medium':
        size = 16
        mines = 40
    else:
        size = 20
        mines = 70

    minesweeper = Board(size=size, mines=mines)