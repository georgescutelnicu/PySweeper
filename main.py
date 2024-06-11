from board import Board
from settings import Settings


if __name__ == "__main__":
    difficulty = Settings()
    selected_difficulty, grid_size = difficulty.choose_difficulty_and_grid_size()
    pysweeper = Board(difficulty=selected_difficulty, grid=grid_size)
