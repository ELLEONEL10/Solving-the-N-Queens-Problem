import time
import os
import psutil

class DFSSolver:
    """
    Solves the N-Queens problem using an exhaustive Depth-First Search (DFS)
    with backtracking.
    """
    def __init__(self, n):
        self.n = n
        self.solutions = []
        self.board = [-1] * n
        # Optimization for is_safe: boolean arrays to track occupied columns and diagonals
        self.col_occupied = [False] * n
        self.diag1_occupied = [False] * (2 * n - 1) # r - c + n - 1
        self.diag2_occupied = [False] * (2 * n - 1) # r + c

    def is_safe(self, row, col):
        """Check if it's safe to place a queen at board[row][col] using boolean arrays."""
        return not self.col_occupied[col] and \
               not self.diag1_occupied[row - col + self.n - 1] and \
               not self.diag2_occupied[row + col]

    def place_queen(self, row, col):
        """Places a queen at (row, col) and updates occupied arrays."""
        self.board[row] = col
        self.col_occupied[col] = True
        self.diag1_occupied[row - col + self.n - 1] = True
        self.diag2_occupied[row + col] = True

    def remove_queen(self, row, col):
        """Removes a queen from (row, col) and updates occupied arrays."""
        self.board[row] = -1
        self.col_occupied[col] = False
        self.diag1_occupied[row - col + self.n - 1] = False
        self.diag2_occupied[row + col] = False

    def solve(self, row=0):
        """Recursively solve the N-Queens problem."""
        if row == self.n:
            # Found a solution
            self.solutions.append(list(self.board))
            return

        for col in range(self.n):
            if self.is_safe(row, col):
                self.place_queen(row, col)
                self.solve(row + 1)
                self.remove_queen(row, col) # Backtrack

    def print_board(self, board_config):
        """Prints the N-Queens board configuration using ASCII art."""
        print(f"\nBoard for N={self.n}:")
        # Top border
        print("+" + "---+" * self.n)
        for r in range(self.n):
            line = ""
            for c in range(self.n):
                if board_config[r] == c:
                    line += "| Q "
                else:
                    line += "|   "
            line += "|"
            print(line)
            # Middle/Bottom border
            print("+" + "---+" * self.n)
        print("\n")


def run_dfs(n):
    """
    Runner function to execute the DFS solver and measure performance.
    """
    process = psutil.Process(os.getpid())
    start_time = time.time()
    mem_before = process.memory_info().rss / 1024 / 1024  # in MB

    # For large N, DFS is impractical.
    if n > 15:
        print(f"DFS for N={n}: Skipped (computationally infeasible).")
        return float('inf'), float('inf'), False

    solver = DFSSolver(n)
    solver.solve()

    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024  # in MB

    execution_time = end_time - start_time
    memory_used = mem_after - mem_before
    success = len(solver.solutions) > 0

    print(f"DFS for N={n}: Time={execution_time:.4f}s, Memory={memory_used:.4f}MB, Success={success}, Solutions={len(solver.solutions)}")
    if success:
        print("First solution found:")
        solver.print_board(solver.solutions[0]) # Print the first solution
    elif n == 2 or n == 3:
        print(f"No solution exists for N={n}.")
    return execution_time, memory_used, success

if __name__ == '__main__':
    print("--- Running DFS Solver ---")
    for n in [4, 8, 10, 12, 30, 100, 200]: # Test smaller N for DFS visualization
        run_dfs(n)