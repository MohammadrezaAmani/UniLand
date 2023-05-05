"""
Description:
    Solving Sudoku with CSP (Constraint Satisfaction Problem) and Backtracking, Forward Checking and Arc Consistency methods
    Project for Amirkabir University of Technilogy (Tehran Polytechnic)
    Computer Scince department
    Artificial Inteligence Course

Student Name & ID: Pouria Alimoradpor 9912035
"""
import random
from copy import deepcopy

class Sudoku():
    def __init__(self, n, c):
        self.n = n
        self.c = c
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.solved = False
        self.tries = 0
    
    def initial_fill(self):
        print(f"Enter your goal cells like (x, y, value): (x, y) ∈ [0, {self.n - 1}]², value ∈ [1, {self.n}]")
        for i in range(self.c):
            x, y, value = map(int, input(f"Cell {i + 1}: ").split())
            if x in range(self.n) and y in range(self.n) and value in range(1, self.n + 1):
                if self.board[x][y] == 0:
                    self.board[x][y] = value
                else:
                    raise Exception(f"Cell ({x}, {y}) is already filled")
            else:
                raise Exception(f"Cell ({x}, {y}) is not in the board or value is not in range [1, {self.n}]")

    def solve(self, method):
        if method == 1:             # backtracking
            self.backtracking()
        elif method == 2:           # forward checking
            self.forward_checking()
        elif method == 3:           # arc consistency
            self.arc_consistency()
        else:
            raise Exception("Method must be one of [backtracking, forward_checking, arc_consistency]")

    def simple_fill(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == 0:
                    for value in range(1, self.n + 1):
                        if self.is_valid(row, col, value):
                            self.board[row][col] = value
                            if self.is_solved():
                                self.solved = True
                                return
                            break
                        else:
                            self.board[row][col] = 0
        if self.is_solved():
            self.solved = True
            return

    def backtracking(self):
        pass

    def forward_checking(self):
        pass

    def arc_consistency(self):
        pass

    def is_valid(self, x, y, value):
        for i in range(self.n):
            if self.board[x][i] == value or self.board[i][y] == value:
                return False
        block_size = int(self.n**0.5)
        block_x = x // block_size
        block_y = y // block_size
        for i in range(block_size):
            for j in range(block_size):
                if self.board[block_x * block_size + i][block_y * block_size + j] == value:
                    return False
        return True

    def is_solved(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    return False
        return True

    def print_board(self):
        block_size = int(self.n ** 0.5)
        horizontal_line = "+" + "+".join(["-" * (block_size*3+1)] * block_size) + "+"

        for i in range(self.n):
            if i % block_size == 0:
                print(horizontal_line)
            row = "| "
            for j in range(self.n):
                if self.board[i][j] == 0:
                    row += " . "
                else:
                    row += "{:2d} ".format(self.board[i][j])
                if (j + 1) % block_size == 0:
                    row += "| "
            print(row)
        print(horizontal_line)

    def __repr__(self):
        return f"Sudoku(n={self.n}, c={self.c})"

    def __str__(self):
        return "\n".join([" ".join([str(cell) for cell in row]) for row in self.board])

if __name__ == "__main__":
    try:
        # ----------------   defining Sudoku  ---------------- #
        n = int(input(f"Enter the number of rows (n×n) (4 - 9 - 16 - 25): "))
        c = int(input(f"Enter the number of cells you want to fill (less than {n**2}): "))
        if n in [4, 9, 16, 25] and c < n**2:
            Sudoku_Game = Sudoku(n, c)
            Sudoku_Game.initial_fill()
            print("Your Sudoku is: ")
            Sudoku_Game.print_board()
        else:
            raise Exception(f"Number of rows must be 4, 9, 16 or 25 (You've entered {n})",
                            f", and number of filled cells must be less than number of {n**2}")
        # ----------------        start        ---------------- #
        method = int(input("Choose your method for solving from:\n" +
                        "1. Backtracking\n" +
                        "2. Forward Checking\n" +
                        "3. Arc Consistency\n" +
                        "Enter the number you choosed: "))
        Sudoku_Game.solve(method)
        # ----------------       result        ---------------- #
        if Sudoku_Game.solved:
            print("Your Sudoku is solved!")
            Sudoku_Game.print_board()
        else:
            print(f"Unsolvable CSP! (by method{method})")

    except Exception as err :
        print(err)
