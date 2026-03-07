"""
Search algorithms for solving the Pipes puzzle game.
This module provides highly optimized DFS and A* search algorithms.
"""

import heapq
import time
import tracemalloc
from game_env import PipesGameState, Tile
from data import MY_LEVELS

def extract_rotations(initial_state, goal_state):
    """Trích xuất các bước xoay giữa trạng thái đầu và đích."""
    rotations = []
    for y in range(initial_state.rows):
        for x in range(initial_state.cols):
            initial_rot = initial_state.grid[y][x].rotation
            goal_rot = goal_state.grid[y][x].rotation
            rotation_diff = (goal_rot - initial_rot) % 360
            if rotation_diff != 0:
                rotations.append((x, y, rotation_diff))
    return rotations


def is_state_valid(state):
    """
    PRUNING FUNCTION (Incremental Consistency Check):
    Instead of checking the whole grid, it only validates the most recently assigned tile.
    """
    if state.depth == 0:
        return True
        
    # Tính tọa độ của ô vừa được gán ở bước trước
    last_idx = state.depth - 1
    x = last_idx % state.cols
    y = last_idx // state.cols
    
    conns = state.grid[y][x].get_connections()
    
    # 1. Không được chĩa ống ra ngoài biên giới
    if x == 0 and conns[3]: return False # Biên trái
    if y == 0 and conns[0]: return False # Biên trên
    if x == state.cols - 1 and conns[1]: return False # Biên phải
    if y == state.rows - 1 and conns[2]: return False # Biên dưới
    
    # 2. Phải khớp với ô BÊN TRÊN (nếu có)
    if y > 0:
        top_conns = state.grid[y - 1][x].get_connections()
        if conns[0] != top_conns[2]: return False
        
    # 3. Phải khớp với ô BÊN TRÁI (nếu có)
    if x > 0:
        left_conns = state.grid[y][x - 1].get_connections()
        if conns[3] != left_conns[1]: return False
        
    return True



def solve_dfs(initial_state, return_steps=False, max_nodes=500000):
    """
    Depth-First Search (DFS) Implementation.
    
    Args:
        initial_state: Starting puzzle configuration.
        return_steps (bool): 
            - If False: Returns rotation list for high-speed benchmarking.
            - If True: Returns all explored states for UI animation.
    """
    grid = initial_state.copy_grid()
    for row in grid:
        for tile in row:
            tile.rotation = 0

    start_state = PipesGameState(grid, (0, 0), 0)
    
    # Sử dụng Stack cho DFS
    stack = [start_state]
    visited = set()
    
    # Mảng lưu lại quá trình duyệt để vẽ lên UI
    steps = []
    
    nodes_explored = 0

    while stack:
        # Lấy node trên cùng của Stack (LIFO)
        current_state = stack.pop()
        nodes_explored += 1
        
        if nodes_explored > max_nodes:
            print(f"!!! [Safety Break] Reached limit of {max_nodes} nodes. DFS stopped to save RAM.")
            if return_steps: return steps, None
            return None
        
        # Nếu bật chế độ UI, ghi lại trạng thái hiện tại đang được xét
        if return_steps:
            steps.append(current_state)
            # Giới hạn để tránh tràn RAM nếu DFS chạy quá sâu trên map lớn
            if len(steps) > 10000: break 

        # Định danh trạng thái để tránh lặp (Graph Search)
        state_hash = (current_state.get_hash(), current_state.depth)

        if state_hash not in visited:
            visited.add(state_hash)

            # Kiểm tra Đích (Goal Test)
            if current_state.is_complete():
                if current_state._check_valid_solution():
                    if return_steps:
                        # Trả về lịch sử duyệt và trạng thái đích cho UI
                        return steps, current_state
                    else:
                        # Trả về danh sách lệnh xoay cho Benchmark
                        return extract_rotations(initial_state, current_state)
                continue

            # Sinh các trạng thái con và đẩy vào Stack
            for successor in reversed(current_state.get_successors()):
                stack.append(successor)

    if return_steps:
        return steps, None
    return None


def heuristic(state):
    """
    h*(n): estimate of h(n).
    Admissible heuristic: Số lượng đầu ống hở ít nhất cần phải đóng.
    """
    open_ends = 0
    if state.depth > 0:
        last_idx = state.depth - 1
        x = last_idx % state.cols
        y = last_idx // state.cols
        conns = state.grid[y][x].get_connections()
        if conns[1]: open_ends += 1 
        if conns[2]: open_ends += 1 
        
    return open_ends


def a_star(initial_state, return_steps=False):
    """
    Args:
        initial_state: The starting configuration of the puzzle.
        return_steps (bool): 
            - If False (Default): Returns a list of rotation commands (optimized for high-speed Benchmarking).
            - If True: Returns a list of all explored states (required for UI Visualization/Animation).
            
    Returns:
        If return_steps is False: A list of tuples (x, y, rotation) representing the solution.
        If return_steps is True: A tuple (list_of_all_steps, goal_state).
    """
    grid = initial_state.copy_grid()
    for row in grid:
        for tile in row:
            tile.rotation = 0

    start_state = PipesGameState(grid, (0, 0), 0)
    
    # Key của g_score phải bao gồm cả cấu trúc lưới VÀ độ sâu (depth)
    start_key = (start_state.get_hash(), start_state.depth)
    g_score = {start_key: 0}
    
    counter = 0
    start_f = heuristic(start_state)
    open_set = [(start_f, counter, start_state)]
    
    steps = [] # Mảng dùng để lưu lại các frame cho UI

    while open_set:
        current_f, _, current_state = heapq.heappop(open_set)
        
        # Nếu bật chế độ cho UI thì lưu trạng thái lại
        if return_steps:
            steps.append(current_state)

        if current_state.is_complete():
            if current_state._check_valid_solution():
                if return_steps:
                    for i, state in enumerate(steps):
                        if state._check_valid_solution():
                            return steps[:i + 1], current_state
                    return steps, current_state
                else:
                    # Trả về mảng lệnh xoay rút gọn cho Benchmark
                    return extract_rotations(initial_state, current_state)
            continue

        for successor in current_state.get_successors():
            if not is_state_valid(successor):
                continue
            
            succ_key = (successor.get_hash(), successor.depth)
            curr_key = (current_state.get_hash(), current_state.depth)
            tentative_g_score = g_score[curr_key] + 1
            
            # Cập nhật nếu tìm thấy đường đi rẻ hơn (hoặc node mới)
            if succ_key not in g_score or tentative_g_score < g_score[succ_key]:
                g_score[succ_key] = tentative_g_score
                
                h_val = heuristic(successor)
                f_val = tentative_g_score + h_val
                
                counter += 1
                heapq.heappush(open_set, (f_val, counter, successor))

    # Xử lý khi không tìm thấy đường
    if return_steps:
        return steps, None
    return None


def print_solution(rotations):
    """
    Prints the solution path in a readable format.
    """
    if rotations is None:
        print("No solution found!")
        return

    if len(rotations) == 0:
        print("The puzzle is already solved!")
        return

    print(f"Solution found with {len(rotations)} rotation steps:")
    for i, (x, y, rotation) in enumerate(rotations):
        num_rotations = rotation // 90
        # Dùng số nhiều (s) nếu xoay nhiều hơn 1 lần để câu văn chuẩn hơn
        times_str = "time" if num_rotations == 1 else "times"
        print(f"  {i + 1}. Tile ({x}, {y}): rotate {rotation}° ({num_rotations} {times_str})")

# ==========================================
# 3. BENCHMARKING (RUNTIME & MEMORY USAGE)
# ==========================================
def run_benchmark(algorithm_func, initial_state, algo_name):
    """
    Executes an algorithm and measures its performance (Runtime and Peak Memory).
    """
    print(f"\n--- Running {algo_name} ---")
    
    # Start tracking memory allocation
    tracemalloc.start()
    
    # Record start time
    start_time = time.time()
    
    # Execute the search algorithm
    solution = algorithm_func(initial_state)
    
    # Record end time and memory usage
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Output the results
    print_solution(solution)
    print("-" * 30)
    print(f"Performance Metrics for {algo_name}:")
    print(f"  > Execution Time: {end_time - start_time:.5f} seconds")
    print(f"  > Peak Memory:    {peak_mem / 10**6:.5f} MB")
    print("-" * 30)


if __name__ == "__main__":
    # 1. Define available levels (Ensure MY_LEVELS is imported)
    try:
        from data import MY_LEVELS
    except ImportError:
        print("Error: data.py not found! Please check your data file.")
        sys.exit()

    print("===========================================")
    print("      PIPES PUZZLE - CLI BENCHMARK         ")
    print("===========================================")

    # 2. Level Selection
    level_names = list(MY_LEVELS.keys())
    print("\nAvailable Levels:")
    for i, name in enumerate(level_names):
        print(f"{i + 1}. {name}")
    
    try:
        level_choice = int(input(f"\nSelect Level (1-{len(level_names)}): ")) - 1
        if not (0 <= level_choice < len(level_names)):
            raise ValueError
        selected_level_name = level_names[level_choice]
        grid = MY_LEVELS[selected_level_name]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting...")
        sys.exit()

    # 3. Algorithm Selection
    print("\nSelect Search Algorithm:")
    print("1. A* (Finds optimal path using heuristics)")
    print("2. DFS (Depth-First Search)")
    
    algo_choice = input("Your choice (1 or 2): ")
    
    state = PipesGameState(grid)
    
    # 4. Execution
    if algo_choice == "1":
        run_benchmark(a_star, state, f"A* on {selected_level_name}")
    elif algo_choice == "2":
        run_benchmark(solve_dfs, state, f"DFS on {selected_level_name}")
    else:
        print("Invalid algorithm selection.")