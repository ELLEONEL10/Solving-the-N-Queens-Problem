import time
import random
import os
import psutil

class GeneticAlgorithmSolver:
    """
    Solves the N-Queens problem using a Genetic Algorithm.
    """
    def __init__(self, n, population_size=100, generations=1000, mutation_rate=0.1):
        self.n = n
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

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

    def fitness(self, chromosome):
        """
        Fitness function: Max possible non-attacking pairs minus current attacking pairs.
        Higher is better. A perfect score is (N * (N-1)) / 2.
        Uses the optimized count_conflicts.
        """
        max_fitness = (self.n * (self.n - 1)) / 2
        attacks = self.count_conflicts(chromosome)
        return max_fitness - attacks

    def selection(self, population):
        """Selects two parents using tournament selection."""
        tournament_size = 5
        parents = []
        for _ in range(2):
            # Ensure tournament_size does not exceed population size
            actual_tournament_size = min(tournament_size, len(population))
            tournament = random.sample(population, actual_tournament_size)
            winner = max(tournament, key=lambda ind: self.fitness(ind))
            parents.append(winner)
        return parents

    def crossover(self, parent1, parent2):
        """Performs a single-point crossover."""
        point = random.randint(1, self.n - 1)
        child = parent1[:point] + parent2[point:]
        return child

    def mutate(self, chromosome):
        """Mutates a chromosome by changing a random gene."""
        if random.random() < self.mutation_rate:
            index = random.randint(0, self.n - 1)
            value = random.randint(0, self.n - 1)
            chromosome[index] = value
        return chromosome

    def solve(self):
        # Initial population of random chromosomes
        population = [[random.randint(0, self.n - 1) for _ in range(self.n)] for _ in range(self.population_size)]

        for gen in range(self.generations):
            # Sort population by fitness (descending)
            population = sorted(population, key=lambda ind: self.fitness(ind), reverse=True)
            
            # Check for solution (best individual has perfect fitness)
            if self.fitness(population[0]) == (self.n * (self.n - 1)) / 2:
                return population[0] # Solution found

            # Elitism: keep top 10% for the next generation (at least 1 individual)
            elite_count = max(1, int(self.population_size * 0.1))
            next_generation = population[:elite_count] 

            # Fill the rest of the next generation through selection, crossover, and mutation
            while len(next_generation) < self.population_size:
                parent1, parent2 = self.selection(population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                next_generation.append(child)
            
            population = next_generation

        # After all generations, return the best individual found if it's a perfect solution
        if population:
            population = sorted(population, key=lambda ind: self.fitness(ind), reverse=True)
            if self.fitness(population[0]) == (self.n * (self.n - 1)) / 2:
                return population[0]
        return None # No perfect solution found within the given generations

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


def run_genetic_algorithm(n):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    mem_before = process.memory_info().rss / 1024 / 1024

    solver = GeneticAlgorithmSolver(n)
    solution = solver.solve()
    
    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024
    
    execution_time = end_time - start_time
    memory_used = mem_after - mem_before
    success = solution is not None and solver.count_conflicts(solution) == 0
    
    print(f"Genetic Algorithm for N={n}: Time={execution_time:.4f}s, Memory={memory_used:.4f}MB, Success={success}")
    if success:
        solver.print_board(solution)
    elif solution: # If a board was returned but not a perfect solution
        print(f"Best attempt (not a perfect solution) for N={n} with {solver.count_conflicts(solution)} conflicts:")
        solver.print_board(solution)
    else:
        print(f"No solution found for N={n}.")
    return execution_time, memory_used, success

if __name__ == '__main__':
    print("--- Running Genetic Algorithm Solver ---")
    for n in [10, 30, 50, 100, 200]:
        run_genetic_algorithm(n)