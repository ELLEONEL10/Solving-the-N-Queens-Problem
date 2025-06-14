
# 🧠 N-Queens Solver Benchmark

This repository provides a comparative study of **four algorithmic approaches** to solving the classical **N-Queens problem**:

- 🧮 Exhaustive Search via **Depth-First Search (DFS)**
- 🔼 Greedy Local Search via **Hill Climbing**
- 🌡️ Meta-Heuristic Search via **Simulated Annealing**
- 🧬 Evolutionary Search via **Genetic Algorithm**

Each algorithm is implemented in Python and evaluated based on:
- ✅ Solution success
- ⏱️ Execution time
- 🧠 Memory usage

📘 **Read the full report on Overleaf**:  
👉 [Latex Report (Overleaf)](https://www.overleaf.com/read/mvbdfhkhznyx#98dbc2)

---

## 📁 Project Files

| File                        | Description                                 |
|----------------------------|---------------------------------------------|
| `dfs_exhaustive_search.py` | DFS backtracking approach (exact, slow)     |
| `hill_climbing_search.py`  | Hill Climbing (fast, prone to local optima) |
| `simulated_annealing.py`   | Simulated Annealing (meta-heuristic)        |
| `genetic_algorithm_solver.py` | Genetic Algorithm (evolutionary search) |
| `Solving_N_Queens_problem.pdf` | Comparative performance report (PDF)  |

---

## 🛠️ Installation

Make sure you have Python 3.x and install the required package:

```bash
pip install psutil
````

> `psutil` is used to measure memory usage of each solver during execution.

---

## 🚀 How to Run

Each solver script can be executed individually to test performance on different board sizes.

### Run DFS (small N only):

```bash
python dfs_exhaustive_search.py
```

### Run Hill Climbing:

```bash
python hill_climbing_search.py
```

### Run Simulated Annealing:

```bash
python simulated_annealing.py
```

### Run Genetic Algorithm:

```bash
python genetic_algorithm_solver.py
```

---

## 📊 Algorithm Comparison Summary

| Algorithm               | Completeness                 | Scalability | Memory Use | Speed     |
| ----------------------- | ---------------------------- | ----------- | ---------- | --------- |
| **DFS**                 | ✅ Complete                   | ❌ Poor      | ✅ Low      | ❌ Slow    |
| **Hill Climbing**       | ⚠️ Incomplete                | ⚠️ Medium   | ✅ Low      | ✅ Fast    |
| **Simulated Annealing** | ⚠️ Incomplete                | ⚠️ Medium   | ✅ Low      | ✅ Fast    |
| **Genetic Algorithm**   | ⚠️ Incomplete (needs tuning) | ✅ Good      | ❌ Higher   | ⚠️ Medium |

---

## 📄 Report & Authors

📘 **Report (PDF)**: [Solving\_N\_Queens\_problem.pdf](./Solving_N_Queens_problem.pdf)
📝 **Overleaf**: [Click here to view in Overleaf](https://www.overleaf.com/read/mvbdfhkhznyx#98dbc2)

### 👤 Authors

* **Fadi Abbara**
  University of Europe for Applied Sciences
  📧 [fadi.abbara@ue-germany.de](mailto:fadi.abbara@ue-germany.de)

* **Raja Hashim Ali**
  AI Research Group, UE Potsdam
  📧 [hashim.ali@ue-germany.de](mailto:hashim.ali@ue-germany.de)

---

## 🔖 Citation

If this work is useful for your research or studies, please cite:


  author = {Fadi Abbara and Raja Hashim Ali},
  title = {Solving the N-Queens Problem with Exhaustive Search, Local Search, and Genetic Algorithms},
  year = {2024},
  institution = {University of Europe for Applied Sciences},
  note = {Course project for Machine Learning for Scientists and Scholars (MLSS)}
}
```

---

## 📝 License

This project is licensed under the **MIT License**.


