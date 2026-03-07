import copy
from collections import deque

class Tile:
    # [Up, Right, Down, Left]
    CONFIG = {
            0: [False, True, False, True],   # 0: Thẳng (Straight) - Gốc là ━
            1: [True, True, False, False],   # 1: Góc chữ L (Corner) - Gốc là ┗
            2: [True, True, True, False],    # 2: Chữ T (T-shape) - Gốc là ┣
            3: [True, True, True, True],     # 3: Chữ thập (Cross) - Gốc là ╋
            4: [True, False, False, False],  # 4: Đầu mút (Endpoint) - Gốc là ╹
        }
    
    SYMBOLS = {
            0: {0: '━', 90: '┃', 180: '━', 270: '┃'},
            1: {0: '┗', 90: '┏', 180: '┓', 270: '┛'},
            2: {0: '┣', 90: '┳', 180: '┫', 270: '┻'},
            3: {0: '╋', 90: '╋', 180: '╋', 270: '╋'}, 
            4: {0: '╹', 90: '╺', 180: '╻', 270: '╸'},
        }
    
    def __init__(self, tile_type, rotation=0):
        self.tile_type = tile_type
        self.rotation = rotation
    
    def get_connections(self):
        """
        Return [Up, Right, Down, Left] after rotation
        """
        base_config = self.CONFIG[self.tile_type]
        rotations = self.rotation // 90
        
        # Dịch vòng tròn mảng kết nối
        result = [base_config[(i - rotations) % 4] for i in range(4)]
        return result
    
    def copy(self):
        return Tile(self.tile_type, self.rotation)
        
    def __repr__(self):
        return f"Tile({self.tile_type}, {self.rotation})"


class PipesGameState:
    # Cập nhật lại DIRECTIONS cho khớp với [Up, Right, Down, Left]
    # Trong ma trận, y đi xuống là dương, x đi phải là dương.
    DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)] 
    # Hướng đối diện (Up <-> Down, Right <-> Left)
    OPPOSITE_DIRECTIONS = [2, 3, 0, 1]
    
    def __init__(self, grid, current_pos=(0, 0), depth=0):
        self.grid = grid
        self.current_pos = current_pos
        self.depth = depth
        self.rows = len(grid)
        self.cols = len(grid)
    
    def copy_grid(self):
        return [[tile.copy() for tile in row] for row in self.grid]

    def is_complete(self):
        # Trạng thái hoàn thành việc gán (chưa chắc đã win game) 
        # là khi độ sâu bằng tổng số ô.
        return self.depth == (self.rows * self.cols)
        
    def get_successors(self):
        """
        Generates successor states from the current state.
        Each successor state represents a valid rotation (action) at the current tile.
        """
        successors = []
        
        # LÝ THUYẾT: Nếu đã gán hết tất cả các ô trên bàn cờ (đạt độ sâu tối đa),
        # trạng thái này là trạng thái lá (leaf node), không sinh thêm con nữa.
        if self.is_complete():
            return successors
        
        # 1. TÍNH TOÁN TỌA ĐỘ TIẾP THEO (Chuyển trạng thái)
        # Quét ma trận theo thứ tự từ Trái sang Phải, từ Trên xuống Dưới.
        x, y = self.current_pos
        # Nếu x chạm lề phải (cols - 1), x tiếp theo quay về 0. Ngược lại x tiến lên 1.
        next_x = 0 if x == self.cols - 1 else x + 1
        # Nếu x chạm lề phải, y nhảy xuống hàng tiếp theo (y + 1). Ngược lại y giữ nguyên.
        next_y = y + 1 if x == self.cols - 1 else y
        next_pos = (next_x, next_y)
        
        # 2. XÁC ĐỊNH Ô ĐANG XÉT
        tile = self.grid[y][x]
        
        # 3. TỐI ƯU HÓA HỆ SỐ RẼ NHÁNH (Symmetry Breaking / Pruning)
        # Mặc định, mỗi ô có 4 cách xoay (Branching factor b = 4).
        valid_rotations = [0, 90, 180, 270]
        
        # Tối ưu 1: Ống thẳng (Straight pipe)
        # Xoay 180 độ hình dáng y hệt 0 độ, xoay 270 độ y hệt 90 độ.
        # Cắt giảm 1 nửa số nhánh, tránh sinh ra các trạng thái trùng lặp.
        if tile.tile_type == 0:    
            valid_rotations = [0, 90]
            
        # Tối ưu 2: Ống chữ thập (Cross) hoặc Ô rỗng (Empty)
        # Hình dáng đối xứng tâm tuyệt đối, xoay hướng nào cũng ra cùng 1 kết quả.
        # Giảm số nhánh từ 4 xuống còn 1.
        elif tile.tile_type == 3 or tile.tile_type == 5: 
            valid_rotations = [0]
            
        # 4. SINH TRẠNG THÁI CON
        # Áp dụng từng góc xoay hợp lệ để tạo ra các trạng thái thế giới mới.
        for rotation in valid_rotations:
            # Bắt buộc phải copy lưới hiện tại để không làm ảnh hưởng đến trạng thái cha
            new_grid = self.copy_grid()
            
            # Thực hiện hành động: Xoay ống
            new_grid[y][x].rotation = rotation  
            
            # Đóng gói thành một node mới: truyền vào lưới mới, tọa độ ô tiếp theo, và tăng độ sâu (depth) thêm 1.
            successors.append(PipesGameState(new_grid, next_pos, self.depth + 1))
            
        return successors
        
    def get_water_flow(self):
        """
        Dùng cho UI: Tìm tất cả các ô có nước chảy tới từ điểm chính giữa.
        Trả về: Một set chứa các tuple tọa độ (x, y) của các ô có nước.
        """
        water_filled = set()
        
        # 1. Tự động xác định nguồn nước ở trung tâm ma trận
        start_x = self.cols // 2
        start_y = self.rows // 2
        
        start_tile = self.grid[start_y][start_x]
        
        # 2. Nếu ô trung tâm không có ống, không có nước chảy ra
        if not any(start_tile.get_connections()):
            return water_filled  
            
        water_filled.add((start_x, start_y))
        queue = deque([(start_x, start_y)])
        
        while queue:
            x, y = queue.popleft()
            current_connections = self.grid[y][x].get_connections()
            
            for i in range(4):
                if current_connections[i]:
                    dx, dy = self.DIRECTIONS[i]
                    nx, ny = x + dx, y + dy
                    
                    if 0 <= nx < self.cols and 0 <= ny < self.rows:
                        if (nx, ny) not in water_filled:
                            neighbor_connections = self.grid[ny][nx].get_connections()
                            opp_dir = self.OPPOSITE_DIRECTIONS[i]
                            
                            if neighbor_connections[opp_dir]:
                                water_filled.add((nx, ny))
                                queue.append((nx, ny))
                                
        return water_filled

    def get_hash(self):
        return tuple(tuple((tile.tile_type, tile.rotation) for tile in row) for row in self.grid)
        
    def is_goal(self):
        if not self.is_complete():
            return False
        return self._check_valid_solution()
        
        
    def _check_valid_solution(self):
        
        visited = [[False] * self.cols for _ in range(self.rows)]
        total_pipes = 0
        
        # 1. Cố định start_pos ở giữa (dùng phép chia lấy nguyên // 2)
        start_x = self.cols // 2
        start_y = self.rows // 2
        start_pos = (start_x, start_y)
        
        # 2. Vẫn cần đếm tổng số ống trên bàn
        for y in range(self.rows):       
            for x in range(self.cols):  
                if any(self.grid[y][x].get_connections()):
                    total_pipes += 1
                    
        # Nếu trên bàn không có ống nào thì bỏ qua
        if total_pipes == 0:
            return False

        # BẢO VỆ: Nếu ô trung tâm (nguồn nước) lại là một ô trống (không có ống) 
        # thì chắc chắn nước không thể chảy đi đâu -> Báo False luôn!
        if not any(self.grid[start_y][start_x].get_connections()):
            return False

        # --- BẮT ĐẦU THUẬT TOÁN LOANG (BFS) ---
        queue = deque([start_pos])
        visited[start_y][start_x] = True  
        visited_count = 1
        
        parent = {start_pos: None}
        
        while queue:
            x, y = queue.popleft()
            connections = self.grid[y][x].get_connections()
            
            for i in range(4):
                if connections[i]:
                    dx, dy = self.DIRECTIONS[i]
                    nx, ny = x + dx, y + dy
                    
                    # CHECK 1: Nước chảy ra ngoài biên
                    if nx < 0 or nx >= self.cols or ny < 0 or ny >= self.rows:
                        return False 
                        
                    neighbor_connections = self.grid[ny][nx].get_connections()
                    opp_dir = self.OPPOSITE_DIRECTIONS[i]
                    
                    # CHECK 2: Hở ống
                    if not neighbor_connections[opp_dir]:
                        return False 
                        
                    # CHECK 3: Vòng lặp kín
                    if visited[ny][nx]:
                        if parent[(x, y)] != (nx, ny):
                            return False
                    else:
                        # Hợp lệ -> Đánh dấu và lan tiếp
                        visited[ny][nx] = True
                        parent[(nx, ny)] = (x, y)
                        visited_count += 1
                        queue.append((nx, ny))
                        
        # CHECK 4: Tính liên thông toàn bộ ống
        return visited_count == total_pipes
        