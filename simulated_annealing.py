import time
import random
import math
import os
import psutil

class SimulatedAnnealingSolver:
    """
    Solves the N-Queens problem using Simulated Annealing to escape local optima.
    """
    def __init__(self, n, initial_temp=1000, cooling_rate=0.995):
        self.n = n
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate

    def count_conflicts(self, board):
        """
        Calculates the number of attacking queen pairs (conflicts) in O(N).
        """
        conflicts = 0
        col_counts = [0] * self.n
        diag1_counts = [0] * (2 * self.n - 1) # r - c + n - 1
        diag2_counts = [0] * (2 * self.n - 1) # r + c

        for r in range(self.n):
            c = board[r]
            col_counts[c] += 1
            diag1_counts[r - c + self.n - 1] += 1
            diag2_counts[r + c] += 1

        for i in range(self.n):
            if col_counts[i] > 1:
                conflicts += col_counts[i] * (col_counts[i] - 1) // 2
        for i in range(2 * self.n - 1):
            if diag1_counts[i] > 1:
                conflicts += diag1_counts[i] * (diag1_counts[i] - 1) // 2
            if diag2_counts[i] > 1:
                conflicts += diag2_counts[i] * (diag2_counts[i] - 1) // 2
        return conflicts

    def solve(self):
        current_board = [random.randint(0, self.n - 1) for _ in range(self.n)]
        current_energy = self.count_conflicts(current_board) # Energy = conflicts (lower is better)
        temp = self.initial_temp

        best_board = list(current_board) # Keep track of the best solution found so far
        best_energy = current_energy

        while temp > 1e-5 and best_energy > 0: # Anneal as long as temp is significant and no solution found
            # Generate a random neighbor by moving one queen to a new random column in its row
            neighbor_board = list(current_board)
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            neighbor_board[row] = col
            
            neighbor_energy = self.count_conflicts(neighbor_board)
            
            delta_energy = neighbor_energy - current_energy # Change in energy (conflicts)

            if delta_energy < 0: # If neighbor is better (fewer conflicts)
                current_board = neighbor_board
                current_energy = neighbor_energy
            else: # If neighbor is worse or equal, accept with a probability based on temperature
                if math.exp(-delta_energy / temp) > random.random():
                    current_board = neighbor_board
                    current_energy = neighbor_energy
            
            # Update the best solution found so far
            if current_energy < best_energy:
                best_energy = current_energy
                best_board = list(current_board)

            temp *= self.cooling_rate # Cool down the temperature

        return best_board if best_energy == 0 else None # Return solution if found, else None

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

def run_simulated_annealing(n):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    mem_before = process.memory_info().rss / 1024 / 1024

    solver = SimulatedAnnealingSolver(n)
    solution = solver.solve()
    
    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024
    
    execution_time = end_time - start_time
    memory_used = mem_after - mem_before
    success = solution is not None and solver.count_conflicts(solution) == 0
    
    print(f"Simulated Annealing for N={n}: Time={execution_time:.4f}s, Memory={memory_used:.4f}MB, Success={success}")
    if success:
        solver.print_board(solution)
    elif solution: # If a board was returned but not a perfect solution
        print(f"Best attempt (not a perfect solution) for N={n} with {solver.count_conflicts(solution)} conflicts:")
        solver.print_board(solution)
    else:
        print(f"No solution found for N={n}.")
    return execution_time, memory_used, success

if __name__ == '__main__':
    print("--- Running Simulated Annealing Solver ---")
    for n in [10, 30, 50, 100, 200]:
        run_simulated_annealing(n)
        