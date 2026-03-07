import pygame

TILE_SIZE = 64

def draw_vector_tile(surface, x, y, size, tile, is_filled=False):
    # 1. Background
    pygame.draw.rect(surface, (240, 240, 240), (x, y, size, size))
    pygame.draw.rect(surface, (200, 200, 200), (x, y, size, size), 1)

    # 2. Pipe configuration
    pipe_color = (50, 150, 255) if is_filled else (100, 100, 100)
    thickness = size // 3
    center_x = x + size // 2
    center_y = y + size // 2
    half_thick = thickness // 2

    conns = tile.get_connections() # [Up, Right, Down, Left]

    # 3. Center Piece
    if tile.tile_type == 4: # Endpoint
        radius = int(thickness * 0.8) 
        pygame.draw.circle(surface, pipe_color, (center_x, center_y), radius)
    else: # Normal pipes
        pygame.draw.rect(surface, pipe_color, (center_x - half_thick, center_y - half_thick, thickness, thickness))

    # 4. Draw branches
    if conns[0]: # Up
        pygame.draw.rect(surface, pipe_color, (center_x - half_thick, y, thickness, size // 2))
    if conns[1]: # Right
        pygame.draw.rect(surface, pipe_color, (center_x, center_y - half_thick, size // 2, thickness))
    if conns[2]: # Down
        pygame.draw.rect(surface, pipe_color, (center_x - half_thick, center_y, thickness, size // 2))
    if conns[3]: # Left
        pygame.draw.rect(surface, pipe_color, (x, center_y - half_thick, size // 2, thickness))

def draw_game_state(screen, game_state, water_filled_tiles_set):
    for y in range(game_state.rows):
        for x in range(game_state.cols):
            tile = game_state.grid[y][x]
            pixel_x = x * TILE_SIZE
            pixel_y = y * TILE_SIZE
            has_water = (x, y) in water_filled_tiles_set
            draw_vector_tile(screen, pixel_x, pixel_y, TILE_SIZE, tile, is_filled=has_water)

    # Water source (Red dot at center)
    start_x, start_y = game_state.cols // 2, game_state.rows // 2
    center_p = (start_x * TILE_SIZE + TILE_SIZE // 2, start_y * TILE_SIZE + TILE_SIZE // 2)
    pygame.draw.circle(screen, (255, 0, 0), center_p, TILE_SIZE // 4)
    pygame.draw.circle(screen, (150, 0, 0), center_p, TILE_SIZE // 4, 3)

def draw_button(screen, rect, text, font, color=(200, 200, 200)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    label = font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_step_info(screen, step_idx, total_steps, font, y_offset):
    text_str = "Initial State" if step_idx == 0 else f"Step: {step_idx} / {total_steps - 1}"
    text = font.render(text_str, True, (0, 0, 0))
    screen.blit(text, (20, y_offset))

def draw_highlight(screen, step_idx, rows, cols, tile_size):
    if step_idx < 0: return
    grid_x, grid_y = step_idx % cols, step_idx // cols
    if grid_y < rows:
        pixel_x, pixel_y = grid_x * tile_size, grid_y * tile_size
        s = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        s.fill((255, 255, 0, 120)) 
        screen.blit(s, (pixel_x, pixel_y))
        pygame.draw.rect(screen, (255, 50, 50), (pixel_x, pixel_y, tile_size, tile_size), 3)

def draw_menu(screen, level_names, title_font, button_font, screen_width):
    title = title_font.render("SELECT LEVEL", True, (50, 50, 50))
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))
    
    buttons = []
    for i, name in enumerate(level_names):
        rect = pygame.Rect(100 + (i % 3) * 150, 150 + (i // 3) * 80, 120, 50)
        buttons.append((rect, name))
        draw_button(screen, rect, name, button_font)
    return buttons
    
def draw_algorithm_selector(screen, font, selected_algo):
    """Draw button to select A* or DFS."""
    algorithms = ["A*", "DFS"]
    buttons = []
    
    start_y = 480 # Vị trí bên dưới danh sách level
    for i, algo in enumerate(algorithms):
        rect = pygame.Rect(180 + i * 140, start_y, 100, 40)
        # Nếu đang được chọn thì màu xanh đậm hơn
        color = (100, 255, 100) if algo == selected_algo else (200, 200, 200)
        draw_button(screen, rect, algo, font, color=color)
        buttons.append((rect, algo))
    return buttons