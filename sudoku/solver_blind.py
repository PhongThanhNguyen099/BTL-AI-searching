import time
import tracemalloc
from utils import is_valid, find_empty, print_board

def solve_dfs(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i

            if solve_dfs(board):
                return True

            board[row][col] = 0 # Backtrack

    return False

# Example usage and performance tracking
if __name__ == "__main__":
    example_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    tracemalloc.start()
    start_time = time.time()
    
    if solve_dfs(example_board):
        print("Sudoku solved via DFS:")
        print_board(example_board)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nRuntime: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory: {peak / 10**6:.4f} MB")
