import pygame
import random
import math
import copy
import time
import tracemalloc
import sys

# Initial Variable
INIT_TEMP = 5.0
COOLING_RATE = 0.9999
MIN_TEMP = 1e-5

# Pygame resolution
WIDTH = 600
HEIGHT = 750
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
MARGIN_X = (WIDTH - GRID_SIZE) // 2
MARGIN_Y = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 150, 0)
BG_COLOR = (245, 245, 245)

def get_blocks_info(init_board):
    blocks_mutable_cells = [[] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            if init_board[r][c] == 0:
                block_idx = (r // 3) * 3 + (c // 3)
                blocks_mutable_cells[block_idx].append((r, c))
    return blocks_mutable_cells

def create_init_state(init_board, blocks_mutable_cells):
    board = copy.deepcopy(init_board)
    for block_idx in range(9):
        start_r = (block_idx // 3) * 3
        start_c = (block_idx % 3) * 3
        existing_nums = set()
        for i in range(3):
            for j in range(3):
                val = board[start_r + i][start_c + j]
                if val != 0:
                    existing_nums.add(val)
        
        missing_nums = list(set(range(1, 10)) - existing_nums)
        random.shuffle(missing_nums)

        for idx, (r, c) in enumerate(blocks_mutable_cells[block_idx]):
            board[r][c] = missing_nums[idx]
    
    return board

def calculate_energy(board):
    energy = 0
    for i in range(9):
        row_duplicates = 9 - len(set(board[i]))
        col_duplicates = 9 - len(set(board[r][i] for r in range(9)))
        energy += row_duplicates + col_duplicates
    return energy

def get_neighbor(board, blocks_mutable_cells):
    new_board = copy.deepcopy(board)
    valid_blocks = [i for i, cells in enumerate(blocks_mutable_cells) if len(cells) >= 2]
    if not valid_blocks:
        return new_board

    block_idx = random.choice(valid_blocks)
    cell1, cell2 = random.sample(blocks_mutable_cells[block_idx], 2)

    r1, c1 = cell1
    r2, c2 = cell2
    new_board[r1][c1], new_board[r2][c2] = new_board[r2][c2], new_board[r1][c1]
    return new_board

def solve_simulated_annealing(init_board, ui_update_callback):
    blocks_mutable_cells = get_blocks_info(init_board)
    current_state = create_init_state(init_board, blocks_mutable_cells)
    current_energy = calculate_energy(current_state)

    T = INIT_TEMP
    iterations = 0

    while T > MIN_TEMP and current_energy > 0:
        neighbor_state = get_neighbor(current_state, blocks_mutable_cells)
        neighbor_energy = calculate_energy(neighbor_state)
        delta_e = neighbor_energy - current_energy

        if delta_e < 0 or random.random() < math.exp(-delta_e / T):
            current_state = neighbor_state
            current_energy = neighbor_energy

        T *= COOLING_RATE
        iterations += 1

        if iterations % 5000 == 0:
            ui_update_callback(current_state, iterations, current_energy, T)

    return current_state, iterations, current_energy

def draw_grid(screen):
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, 
                         (MARGIN_X + i * CELL_SIZE, MARGIN_Y), 
                         (MARGIN_X + i * CELL_SIZE, MARGIN_Y + GRID_SIZE), line_width)
        pygame.draw.line(screen, BLACK, 
                         (MARGIN_X, MARGIN_Y + i * CELL_SIZE), 
                         (MARGIN_X + GRID_SIZE, MARGIN_Y + i * CELL_SIZE), line_width)

def draw_numbers(screen, font, current_board, initial_board):
    for r in range(9):
        for c in range(9):
            val = current_board[r][c]
            if val != 0:
                color = BLACK if initial_board[r][c] != 0 else BLUE
                text_surface = font.render(str(val), True, color)
                
                text_rect = text_surface.get_rect(center=(
                    MARGIN_X + c * CELL_SIZE + CELL_SIZE // 2,
                    MARGIN_Y + r * CELL_SIZE + CELL_SIZE // 2
                ))
                screen.blit(text_surface, text_rect)

def draw_dashboard(screen, font_small, iterations, energy, temp, runtime=None, memory=None):
    pygame.draw.rect(screen, BG_COLOR, (0, MARGIN_Y + GRID_SIZE + 10, WIDTH, HEIGHT - GRID_SIZE))
    
    y_offset = MARGIN_Y + GRID_SIZE + 20
    text_iter = font_small.render(f"Iterations: {iterations}", True, BLACK)
    text_energy = font_small.render(f"Energy (Errors): {energy}", True, BLACK)
    text_temp = font_small.render(f"Temperature: {temp:.5f}", True, BLACK)
    
    screen.blit(text_iter, (MARGIN_X, y_offset))
    screen.blit(text_energy, (MARGIN_X, y_offset + 30))
    screen.blit(text_temp, (MARGIN_X, y_offset + 60))
    
    if runtime is not None and memory is not None:
        color = GREEN if energy == 0 else BLUE
        status = "SOLVED!" if energy == 0 else "STOPPED"
        text_status = font_small.render(status, True, color)
        text_time = font_small.render(f"Runtime: {runtime:.4f} s", True, BLACK)
        text_mem = font_small.render(f"Peak Mem: {memory:.4f} MB", True, BLACK)
        
        screen.blit(text_status, (WIDTH - MARGIN_X - 150, y_offset))
        screen.blit(text_time, (WIDTH - MARGIN_X - 150, y_offset + 30))
        screen.blit(text_mem, (WIDTH - MARGIN_X - 150, y_offset + 60))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver - Simulated Annealing AI")
    
    font_large = pygame.font.SysFont('arial', 40, bold=True)
    font_small = pygame.font.SysFont('arial', 20)
    
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

    # Callback for update ui
    def update_ui(current_board, iterations, energy, temp):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_numbers(screen, font_large, current_board, example_board)
        draw_dashboard(screen, font_small, iterations, energy, temp)
        pygame.display.flip()

    # START ALGORITHM
    # Init state
    update_ui(example_board, 0, calculate_energy(create_init_state(example_board, get_blocks_info(example_board))), INIT_TEMP)
    
    time.sleep(1) 

    tracemalloc.start()
    start_time = time.time()

    # Callback for Simulated Annealing
    final_board, total_iterations, final_energy = solve_simulated_annealing(example_board, update_ui)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = end_time - start_time
    peak_mem_mb = peak / 10**6

    #Final Result
    screen.fill(BG_COLOR)
    draw_grid(screen)
    draw_numbers(screen, font_large, final_board, example_board)
    draw_dashboard(screen, font_small, total_iterations, final_energy, 0, runtime, peak_mem_mb)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()