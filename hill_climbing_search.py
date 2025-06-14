import time
import random
import os
import psutil

class HillClimbingSolver:
    """
    Solves the N-Queens problem using a simple Hill Climbing algorithm.
    It may get stuck in local optima.
    """
    def __init__(self, n, max_restarts=100):
        self.n = n
        self.max_restarts = max_restarts

    def count_conflicts(self, board):
        """
        Calculates the number of attacking queen pairs (conflicts) in O(N).
        This is an optimization over the original O(N^2) method.
        """
        conflicts = 0
        col_counts = [0] * self.n
        diag1_counts = [0] * (2 * self.n - 1) # r - c + n - 1 (offset to make index non-negative)
        diag2_counts = [0] * (2 * self.n - 1) # r + c

        for r in range(self.n):
            c = board[r]
            col_counts[c] += 1
            diag1_counts[r - c + self.n - 1] += 1
            diag2_counts[r + c] += 1

        # For 'k' queens in a line, there are k*(k-1)/2 conflicts
        for i in range(self.n): # Check columns
            if col_counts[i] > 1:
                conflicts += col_counts[i] * (col_counts[i] - 1) // 2
        for i in range(2 * self.n - 1): # Check diagonals
            if diag1_counts[i] > 1:
                conflicts += diag1_counts[i] * (diag1_counts[i] - 1) // 2
            if diag2_counts[i] > 1:
                conflicts += diag2_counts[i] * (diag2_counts[i] - 1) // 2
        return conflicts

    def get_best_neighbor(self, board):
        """
        Finds the best neighboring state by moving one queen to reduce conflicts.
        Uses the optimized conflict counter.
        """
        best_board = list(board)
        min_attacks = self.count_conflicts(board)

        for row_to_move in range(self.n):
            original_col = board[row_to_move]
            for target_col in range(self.n):
                if target_col == original_col:
                    continue

                # Temporarily move queen
                board[row_to_move] = target_col
                current_attacks = self.count_conflicts(board) # Use optimized conflict counter

                if current_attacks < min_attacks:
                    min_attacks = current_attacks
                    best_board = list(board) # Deep copy the best board configuration

            board[row_to_move] = original_col # Backtrack for the next queen's move

        return best_board, min_attacks

    def solve(self):
        """
        Attempts to find a solution using random-restart hill climbing.
        """
        for _ in range(self.max_restarts):
            # Start with a random board configuration (one queen per row)
            current_board = [random.randint(0, self.n - 1) for _ in range(self.n)]
            current_attacks = self.count_conflicts(current_board)

            while True:
                # Find the best neighbor
                neighbor_board, neighbor_attacks = self.get_best_neighbor(current_board)

                # If no improvement, we're stuck in a local optimum
                if neighbor_attacks >= current_attacks:
                    break
                
                current_board = neighbor_board
                current_attacks = neighbor_attacks
            
            if current_attacks == 0:
                return current_board # Solution found

        return None # Failed to find a solution after max_restarts

    def print_board(self, board_config):
        """Prints the N-Queens board configuration using ASCII art."""
        print(f"\nBoard for N={self.n}:")
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
            print("+" + "---+" * self.n)
        print("\n")


def run_hill_climbing(n):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    mem_before = process.memory_info().rss / 1024 / 1024

    solver = HillClimbingSolver(n)
    solution = solver.solve()
    
    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024
    
    execution_time = end_time - start_time
    memory_used = mem_after - mem_before
    success = solution is not None and solver.count_conflicts(solution) == 0 # Verify solution if found
    
    print(f"Hill Climbing for N={n}: Time={execution_time:.4f}s, Memory={memory_used:.4f}MB, Success={success}")
    if success:
        solver.print_board(solution)
    elif solution: # If a board was returned but not a perfect solution
        print(f"Best attempt (not a perfect solution) for N={n} with {solver.count_conflicts(solution)} conflicts:")
        solver.print_board(solution)
    else:
        print(f"No solution found for N={n} after {solver.max_restarts} restarts.")
    return execution_time, memory_used, success

if __name__ == '__main__':
    print("--- Running Hill Climbing Solver ---")
    # Example usage:
    # Try running for a moderately sized N like 10 or 30.
    # For N=10, it should often find a solution. For N=30 or higher, it may take more restarts.
    for n_test in [10, 30]: 
        print(f"\n--- Testing N = {n_test} ---")
        run_hill_climbing(n_test)
        