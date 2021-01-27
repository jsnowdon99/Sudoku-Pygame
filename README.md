# Sudoku-Pygame
![Demo](https://github.com/jsnowdon99/Sudoku-Pygame/blob/main/images/sud.PNG?raw=true)

Built utilizing the Pygame module, this program is loaded with an interactive GUI with a 9x9 board for the game, Sudoku. 

If you have never played Sudoku the rules are that each of the nine squares has to contain all the numbers 1-9 within its squares. Each number can only appear once in a row, column or box (3x3).

The game was developed as an exercise in recursive backtracking algorithms. The algorithm will attempt to place numbers in empty squares and backtrack if the given number set does not meet the Sudoku constraints.

For a large data set, this algorithm would not be efficient. Though given the board size, it is appropriate.
## To play

Ensure that both sudoku_logic.py and sudoku.csv (found in sudoku.zip) exist in the same directory. Compile
and run sudoku_loguic.py with python3.7+. 

The game utilizes the csv file to randomly select from >1000 possible board variations. All of which are solvable. 

