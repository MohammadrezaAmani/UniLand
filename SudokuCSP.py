"""
Description:
    Solving Sudoku with CSP (Constraint Satisfaction Problem) and Backtracking, Forward Checking and Arc Consistency methods
    Project for Amirkabir University of Technilogy (Tehran Polytechnic)
    Computer Scince department
    Artificial Inteligence Course

Student Name & ID: Pouria Alimoradpor 9912035
"""
import random
import time
from copy import deepcopy

class Sudoku():
    def __init__(self, n, c):
        self.n = n
        self.block_size = int(n**0.5)
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
                    if self.is_valid(x, y, value):
                        self.board[x][y] = value
                    else:
                        raise Exception(f"Value {value} is not valid for cell ({x}, {y})")
                else:
                    raise Exception(f"Cell ({x}, {y}) is already filled!")
            else:
                raise Exception(f"Cell ({x}, {y}) is not in the board or value is not in range [1, {self.n}]")

    def solve(self, method):
        if method == "backtracking":
            self.backtracking()
        elif method == "forward_checking":
            self.forward_checking()
        elif method == "arc_consistency":
            self.arc_consistency()
        else:
            raise Exception("Method must be one of [backtracking, forward_checking, arc_consistency]")

    def backtracking(self):
        self.tries += 1
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == 0:
                    for value in range(1, self.n + 1):
                        if self.is_valid(row, col, value):
                            self.board[row][col] = value
                            if self.backtracking():
                                return True
                            else:
                                self.board[row][col] = 0
                    return False
        if self.is_solved():
            self.solved = True
        return True

    def forward_checking(self):
        self.tries += 1
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == 0:
                    remaining_values = set(range(1, self.n+1))
                    for i in range(self.n):
                        if self.board[row][i] in remaining_values:
                            remaining_values.remove(self.board[row][i])
                        if self.board[i][col] in remaining_values:
                            remaining_values.remove(self.board[i][col])
                    block_x = row // self.block_size
                    block_y = col // self.block_size
                    for i in range(self.block_size):
                        for j in range(self.block_size):
                            x = block_x * self.block_size + i
                            y = block_y * self.block_size + j
                            if self.board[x][y] in remaining_values:
                                remaining_values.remove(self.board[x][y])
                    for value in remaining_values:
                        self.board[row][col] = value
                        if self.forward_checking():
                            return True
                        else:
                            self.board[row][col] = 0
                    return False
        if self.is_solved():
            self.solved = True
        return True

    def arc_consistency(self):
        queue = []
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    for k in range(self.n):
                        if k != j:
                            queue.append(((i, j), (i, k)))
                        if k != i:
                            queue.append(((i, j), (k, j)))
                    block_x = i // self.block_size
                    block_y = j // self.block_size
                    for x in range(self.block_size):
                        for y in range(self.block_size):
                            x_, y_ = block_x * self.block_size + x, block_y * self.block_size + y
                            if (x_, y_) != (i, j):
                                queue.append(((i, j), (x_, y_)))
        while queue:
            (i, j), (i_, j_) = queue.pop(0)
            if self.revise(i, j, i_, j_):
                for k in range(self.n):
                    if k != j_ and self.board[i_][k] == 0:
                        queue.append(((i_, k), (i, j_)))
                block_x = i_ // self.block_size
                block_y = j_ // self.block_size
                for x in range(self.block_size):
                    for y in range(self.block_size):
                        x_, y_ = block_x * self.block_size + x, block_y * self.block_size + y
                        if (x_, y_) != (i_, j_) and self.board[x_][y_] == 0:
                            queue.append(((x_, y_), (i, j_)))
        if self.is_solved():
            self.solved = True

    def revise(self, i, j, i_, j_):
        revised = False
        
        for value in range(1, self.n + 1):
            if self.board[i][j] == value:
                if not any(self.board[x][j_] == value for x in range(self.n) if x != i):
                    return False
            if self.board[i][j] != value:
                continue
            inconsistent = True
            for v in range(1, self.n + 1):
                if v == value:
                    continue
                if any(self.board[x][j_] == v for x in range(self.n) if x != i):
                    inconsistent = False
                    break
            if inconsistent:
                self.board[i][j] = 0
                revised = True
        return revised

    def is_valid(self, x, y, value):            # CSP
        for i in range(self.n):
            if self.board[x][i] == value or self.board[i][y] == value:
                return False
        block_x = x // self.block_size
        block_y = y // self.block_size
        for i in range(self.block_size):
            for j in range(self.block_size):
                if self.board[block_x * self.block_size + i][block_y * self.block_size + j] == value:
                    return False
        return True

    def is_solved(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    return False
        return True

    def print_board(self):
        horizontal_line = "+" + "+".join(["-" * (self.block_size*3+1)] * self.block_size) + "+"
        print()
        for i in range(self.n):
            if i % self.block_size == 0:
                print(horizontal_line)
            row = "| "
            for j in range(self.n):
                if self.board[i][j] == 0:
                    row += " . "
                else:
                    row += "{:2d} ".format(self.board[i][j])
                if (j + 1) % self.block_size == 0:
                    row += "| "
            print(row)
        print(horizontal_line)
        print()

    def __repr__(self):
        return f"Sudoku(n={self.n}, c={self.c})"

    def __str__(self):
        return "\n".join([" ".join([str(cell) for cell in row]) for row in self.board])

if __name__ == "__main__":
    try:
        # ----------------   defining Sudoku  ---------------- #
        n = int(input(f"Enter the number of rows (nxn) (4 - 9 - 16 - 25): "))
        c = int(input(f"Enter the number of cells you want to fill (less than {n**2}): "))
        if n in [4, 9, 16, 25] and c < n**2:
            Sudoku_Game = Sudoku(n, c)
            Sudoku_Game.initial_fill()
            print("Your Sudoku is: ")
            Sudoku_Game.print_board()
        else:
            raise Exception(f"Number of rows must be 4, 9, 16 or 25 (You've entered {n})",
                            f", and number of filled cells must be less than number of {n**2}")

        while True:
            # ----------------        start        ---------------- #
            method = int(input("Choose your method for solving from:\n" +
                            "1. Backtracking\n" +
                            "2. Forward Checking\n" +
                            "3. Arc Consistency\n" +
                            "Enter the number you choosed (or 0 to exit): "))
            if method == 0:
                print("Okay, Goodbye!")
                break
            elif method == 1:
                method = "backtracking"
            elif method == 2:
                method = "forward_checking"
            elif method == 3:
                method = "arc_consistency"

            start_time = time.perf_counter()
            Sudoku_Game.solve(method)
            end_time = time.perf_counter()
            # ----------------       result        ---------------- #
            if Sudoku_Game.solved:
                print(f"Your Sudoku is solved! (by {method}) in {Sudoku_Game.tries} tries")
                print(f"Time elapsed: {end_time - start_time} seconds")
                Sudoku_Game.print_board()
            else:
                print(f"Unsolvable CSP! (by {method}) in {Sudoku_Game.tries} tries")

    except Exception as err :
        print(err)
