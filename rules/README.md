## PySweeper - Game Rules

### Objective
The objective of PySweeper is to clear a rectangular board without revealing any hidden "snakes." Use the numbers on revealed cells to deduce which adjacent cells are safe to click.

### How to Play
1. **Reveal Cells**: Click on a cell to reveal it.
    - If the cell contains a snake, the game is over.
    - If the cell does not contain a snake, a number will appear, indicating how many snakes are adjacent to that cell.
    - If there are no snakes adjacent, a blank cell appears, and all neighboring cells are automatically revealed.

2. **Flag Snakes**: Right-click to mark a cell you suspect contains a snake.
    - Flagging cells helps you remember which ones you believe contain snakes.
    - You can unflag a cell by right-clicking again.

3. **Solve Puzzles (Medium and Hard Difficulty Levels Only)**:  
    - When playing on **Medium** or **Hard** difficulty, revealing certain cells will display a question mark (`?`) instead of a number.
    - To reveal the true number of adjacent snakes, click on the cell with the question mark.
    - You will then be prompted to solve a puzzle.  
        - Solve the puzzle by selecting the number that matches the solution provided by the puzzle.
        - If you answer incorrectly, the game continues, but your progress may be affected.

4. **Win the Game**: Reveal all cells that do not contain snakes without triggering any snakes to win the game.

### Tips
- Use logic and deduction based on the numbers revealed to avoid the snakes.
- Start by clicking the marked cell to reveal more cells at once.
- Pay attention to the question mark cells and solve puzzles carefully when playing on Medium or Hard difficulties.
