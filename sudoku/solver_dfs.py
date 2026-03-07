import pygame
import time
import tracemalloc
import copy
import sys
from testcase import *   


WIDTH = 600
HEIGHT = 750
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
MARGIN_X = (WIDTH - GRID_SIZE) // 2
MARGIN_Y = 20

UI_UPDATE_FREQ = 2 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
BG_COLOR = (245, 245, 245)


def find_empty(board):
    """Tìm ô trống đầu tiên (từ trái qua phải, trên xuống dưới)."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid(board, row, col, num):
    """Kiểm tra xem đặt số 'num' vào vị trí (row, col) có hợp lệ không."""
    # Kiểm tra hàng
    for i in range(9):
        if board[row][i] == num and col != i:
            return False
    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num and row != i:
            return False
    # Kiểm tra khối 3x3
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != (row, col):
                return False
    return True

def solve_dfs(board, initial_board, ui_update_callback, stats):
    """
    Thuật toán Backtracking bằng Đệ quy.
    stats là một dictionary lưu lại số bước duyệt và số lần quay lui.
    """
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i
            stats['iterations'] += 1

            if stats['iterations'] % UI_UPDATE_FREQ == 0:
                ui_update_callback(board, stats)

            if solve_dfs(board, initial_board, ui_update_callback, stats):
                return True

            board[row][col] = 0 
            stats['iterations'] += 1
            stats['backtracks'] += 1
            
            if stats['iterations'] % UI_UPDATE_FREQ == 0:
                ui_update_callback(board, stats)

    return False


def draw_grid(screen):
    """Vẽ lưới Sudoku."""
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (MARGIN_X + i * CELL_SIZE, MARGIN_Y), 
                         (MARGIN_X + i * CELL_SIZE, MARGIN_Y + GRID_SIZE), line_width)
        pygame.draw.line(screen, BLACK, (MARGIN_X, MARGIN_Y + i * CELL_SIZE), 
                         (MARGIN_X + GRID_SIZE, MARGIN_Y + i * CELL_SIZE), line_width)

def draw_numbers(screen, font, current_board, initial_board):
    """Vẽ các con số lên bảng."""
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

def draw_dashboard(screen, font_small, stats, runtime=None, memory=None):
    """Vẽ bảng thông số ở phía dưới lưới Sudoku."""
    pygame.draw.rect(screen, BG_COLOR, (0, MARGIN_Y + GRID_SIZE + 10, WIDTH, HEIGHT - GRID_SIZE))
    
    y_offset = MARGIN_Y + GRID_SIZE + 20
    text_iter = font_small.render(f"Iterations (Steps): {stats['iterations']}", True, BLACK)
    text_backtracks = font_small.render(f"Backtracks: {stats['backtracks']}", True, BLACK)
    
    screen.blit(text_iter, (MARGIN_X, y_offset))
    screen.blit(text_backtracks, (MARGIN_X, y_offset + 30))
    
    if runtime is not None and memory is not None:
        text_status = font_small.render("SOLVED!", True, GREEN)
        text_time = font_small.render(f"Runtime: {runtime:.4f} s", True, BLACK)
        text_mem = font_small.render(f"Peak Mem: {memory:.4f} MB", True, BLACK)
        
        screen.blit(text_status, (WIDTH - MARGIN_X - 150, y_offset))
        screen.blit(text_time, (WIDTH - MARGIN_X - 150, y_offset + 30))
        screen.blit(text_mem, (WIDTH - MARGIN_X - 150, y_offset + 60))
    else:
        text_status = font_small.render("SOLVING...", True, RED)
        screen.blit(text_status, (WIDTH - MARGIN_X - 150, y_offset))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver - Backtracking / DFS")
    
    font_large = pygame.font.SysFont('arial', 40, bold=True)
    font_small = pygame.font.SysFont('arial', 20)
    
    example_board = HARD

    working_board = copy.deepcopy(example_board)
    stats = {'iterations': 0, 'backtracks': 0}

    def update_ui(current_board, current_stats):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_numbers(screen, font_large, current_board, example_board)
        draw_dashboard(screen, font_small, current_stats)
        pygame.display.flip()

    update_ui(working_board, stats)
    time.sleep(1)

    tracemalloc.start()
    start_time = time.time()

    solve_dfs(working_board, example_board, update_ui, stats)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = end_time - start_time
    peak_mem_mb = peak / 10**6

    screen.fill(BG_COLOR)
    draw_grid(screen)
    draw_numbers(screen, font_large, working_board, example_board)
    draw_dashboard(screen, font_small, stats, runtime, peak_mem_mb)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
