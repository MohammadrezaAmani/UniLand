 def arc_consistency(self):
        queue = []
        # Initialize the queue with all arcs in the Sudoku board
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
        # Iterate over the arcs in the queue
        while queue:
            (i, j), (i_, j_) = queue.pop(0)
            if self.revise(i, j, i_, j_):
                # If a value is removed from the domain of (i, j), propagate the changes
                # by adding all arcs (i_, k) where k is a neighbor of i_ (excluding j_)
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
        # If the Sudoku board is solved, mark it as solved
        if self.is_solved():
            self.solved = True

    def revise(self, i, j, i_, j_):
        revised = False
        # Remove values from the domain of (i, j) that are inconsistent with the value of (i_, j_)
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