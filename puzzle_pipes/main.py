import pygame
import sys
from game_env import PipesGameState
from ui import (draw_game_state, draw_button, draw_step_info, 
                draw_highlight, draw_menu, draw_algorithm_selector, TILE_SIZE)
from search import a_star, solve_dfs

try:
    from data import MY_LEVELS
except ImportError:
    print("Error: data.py not found!")
    sys.exit()

MIN_SCREEN_WIDTH, MENU_HEIGHT, PANEL_HEIGHT, FPS = 600, 650, 120, 60
STATE_MENU, STATE_PLAYING = "MENU", "PLAYING"

def main():
    pygame.init()
    # Khởi tạo với MENU_HEIGHT
    screen = pygame.display.set_mode((MIN_SCREEN_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption("Pipes Puzzle Solver")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial", 22, bold=True)
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    win_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    search_type = "A*"
    current_state = STATE_MENU
    steps, step_index = [], 0
    board_w, board_h, offset_x = 0, 0, 0

    auto_run = False
    auto_speed = 300 
    last_auto_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill((240, 240, 240))
        events = pygame.event.get()
        current_time = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.QUIT: 
                running = False

        if current_state == STATE_MENU:
            level_buttons = draw_menu(screen, list(MY_LEVELS.keys()), title_font, font, MIN_SCREEN_WIDTH)
            
            # Vẽ nhãn thuật toán
            algo_label = font.render("Select Algorithm:", True, (50, 50, 50))
            screen.blit(algo_label, (MIN_SCREEN_WIDTH//2 - algo_label.get_width()//2, 440))
            algo_buttons = draw_algorithm_selector(screen, font, search_type)
            
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 1. Chọn thuật toán
                    for rect, algo in algo_buttons:
                        if rect.collidepoint(event.pos):
                            search_type = algo
                    
                    # 2. Chọn Level
                    for rect, name in level_buttons:
                        if rect.collidepoint(event.pos):
                            grid = MY_LEVELS[name]
                            initial_state = PipesGameState(grid)
                            board_w = initial_state.cols * TILE_SIZE
                            board_h = initial_state.rows * TILE_SIZE
                            
                            new_w = max(board_w, MIN_SCREEN_WIDTH)
                            new_h = board_h + PANEL_HEIGHT
                            screen = pygame.display.set_mode((new_w, new_h))
                            offset_x = (new_w - board_w) // 2
                            
                            print(f"Solving {name} using {search_type}...")
                            if search_type == "A*":
                                steps, _ = a_star(initial_state, return_steps=True)
                            else:
                                steps, _ = solve_dfs(initial_state, return_steps=True)
                                
                            step_index = 0
                            auto_run = False
                            current_state = STATE_PLAYING

        elif current_state == STATE_PLAYING:
            if not steps:
                current_state = STATE_MENU
                screen = pygame.display.set_mode((MIN_SCREEN_WIDTH, MENU_HEIGHT))
                continue
                
            curr_grid_state = steps[step_index]
            water_set = curr_grid_state.get_water_flow()
            game_won = curr_grid_state._check_valid_solution()

            if auto_run and not game_won:
                if current_time - last_auto_time > auto_speed:
                    if step_index < len(steps) - 1:
                        step_index += 1
                        last_auto_time = current_time
                    else:
                        auto_run = False

            # 1. Render Board
            board_surf = pygame.Surface((board_w, board_h))
            board_surf.fill((255, 255, 255))
            draw_game_state(board_surf, curr_grid_state, water_set)
            # Highlight ô mà thuật toán đang xử lý
            draw_highlight(board_surf, curr_grid_state.depth - 1, curr_grid_state.rows, curr_grid_state.cols, TILE_SIZE)
            screen.blit(board_surf, (offset_x, 0))

            # 2. Render Panel
            panel_y = board_h
            pygame.draw.rect(screen, (220, 220, 220), (0, panel_y, screen.get_width(), PANEL_HEIGHT))
            
            algo_info = font.render(f"Mode: {search_type}", True, (100, 100, 100))
            screen.blit(algo_info, (screen.get_width() - 150, panel_y + 15))
            
            prev_btn = pygame.Rect(screen.get_width()//2 - 240, panel_y + 55, 80, 40)
            next_btn = pygame.Rect(screen.get_width()//2 - 150, panel_y + 55, 80, 40)
            auto_btn = pygame.Rect(screen.get_width()//2 - 60, panel_y + 55, 80, 40)
            back_btn = pygame.Rect(screen.get_width()//2 + 50, panel_y + 55, 140, 40)

            draw_button(screen, prev_btn, "Prev", font)
            draw_button(screen, next_btn, "Next", font)
            draw_button(screen, auto_btn, "Stop" if auto_run else "Auto", font, color=(200, 255, 200) if auto_run else (200, 200, 200))
            draw_button(screen, back_btn, "Back to Menu", font, color=(150, 150, 255))
            draw_step_info(screen, step_index, len(steps), font, panel_y + 15)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if prev_btn.collidepoint(event.pos):
                        step_index = max(0, step_index - 1)
                        auto_run = False
                    elif next_btn.collidepoint(event.pos):
                        step_index = min(len(steps) - 1, step_index + 1)
                        auto_run = False
                    elif auto_btn.collidepoint(event.pos):
                        auto_run = not auto_run
                        last_auto_time = current_time
                    elif back_btn.collidepoint(event.pos):
                        current_state = STATE_MENU
                        screen = pygame.display.set_mode((MIN_SCREEN_WIDTH, MENU_HEIGHT))

            if game_won:
                auto_run = False
                txt = win_font.render("PUZZLE SOLVED!", True, (0, 180, 0))
                txt_rect = txt.get_rect(center=(screen.get_width()//2, board_h//2))
                bg_rect = txt_rect.inflate(40, 30)
                pygame.draw.rect(screen, (100, 100, 100), bg_rect.move(5, 5)) # Shadow
                pygame.draw.rect(screen, (255, 255, 255), bg_rect)
                pygame.draw.rect(screen, (0, 180, 0), bg_rect, 4)
                screen.blit(txt, txt_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()