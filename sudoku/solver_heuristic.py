import time
import tracemalloc
from utils import is_valid, print_board

def get_mrv_cell(board):
    min_options = 10
    best_cell = None
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                # Count valid options for this cell
                options = 0
                for num in range(1, 10):
                    if is_valid(board, r, c, num):
                        options += 1
                
                if options < min_options:
                    min_options = options
                    best_cell = (r, c)
                    
                if min_options == 1: # Optimization: only 1 choice left
                    return best_cell
    return best_cell

def solve_mrv(board):
    cell = get_mrv_cell(board)
    if not cell:
        return True
    
    row, col = cell
    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i

            if solve_mrv(board):
                return True

            board[row][col] = 0 # Backtrack
    return False

if __name__ == "__main__":
    # Use same board for comparison
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

    if solve_mrv(example_board):
        print("Sudoku solved via MRV Heuristic:")
        print_board(example_board)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nRuntime: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory: {peak / 10**6:.4f} MB")
