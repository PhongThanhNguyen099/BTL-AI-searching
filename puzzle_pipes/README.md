# Pipes Puzzle Solver Documentation

This repository contains an AI-powered solver for the Pipes puzzle game. It includes both a Graphical User Interface (GUI) for visualizing the search process and a Command-Line Interface (CLI) for performance benchmarking.

---

## 1. GUI Application (`main.py`)

The GUI application provides an interactive way to select levels, choose search algorithms, and watch the AI solve the puzzle step-by-step.

### Prerequisites

* Python 3.x
* `pygame` library (`pip install pygame`)

### How to Run

Execute the main script from your terminal:

```bash
python main.py

```

### Usage Instructions

1. **Menu Screen:**
* Click on any of the available level buttons to select a puzzle.
* Click on the **A*** or **DFS** button at the bottom to choose the search algorithm. The selected algorithm will be highlighted in green.


2. **Playing Screen:**
* The selected puzzle will be displayed. The highlighted tile indicates the current focus of the search algorithm.
* **Next / Prev:** Manually step forward or backward through the algorithm's search process.
* **Auto / Stop:** Toggle automatic playback of the search steps.
* **Back to Menu:** Exit the current puzzle and return to the level selection screen.
* Once the puzzle is solved, a "PUZZLE SOLVED!" message will appear.



---

## 2. CLI Benchmark Tool (`search.py`)

The CLI tool allows you to run the search algorithms directly in the terminal. It provides detailed performance metrics, including execution time and peak memory usage, without the overhead of rendering the GUI.

### How to Run

Execute the search script from your terminal:

```bash
python search.py

```

### Usage Instructions

1. **Level Selection:**
* The terminal will display a numbered list of available levels (e.g., `1. level1`, `2. level2`).
* Input the number corresponding to the level you want to solve and press Enter.


2. **Algorithm Selection:**
* The terminal will prompt you to select an algorithm:
* Input `1` for **A* Search** (Optimal path using heuristics).
* Input `2` for **DFS** (Depth-First Search).


* Press Enter to confirm your choice.


3. **Results:**
* The script will execute the chosen algorithm and print the required rotation steps to solve the puzzle.
* It will output a **Performance Metrics** summary, displaying:
* `Execution Time`: The time taken to find the solution (in seconds).
* `Peak Memory`: The maximum RAM allocated during the search (in MB).





### Important Note on DFS

The `solve_dfs` function includes a safety mechanism (`max_nodes=500000`). If the Depth-First Search explores more than 500,000 nodes without finding a solution, it will automatically terminate to prevent your system from running out of memory. This usually indicates that the search space is too large for unguided DFS, and A* should be used instead.