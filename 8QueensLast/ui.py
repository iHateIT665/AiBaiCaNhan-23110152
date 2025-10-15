import pygame

# ========== CẤU HÌNH CƠ BẢN ==========
pygame.init()
cell_size = 50
board_size = 8 * cell_size
width = board_size * 2 + 160
height = board_size + 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("8 Queens Visualization")

# ========== MÀU SẮC ==========
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
BLUE = (100, 100, 255)
RED = (200, 50, 50)
BORDER_COLOR = (150, 150, 150)

# ========== FONT ==========
font = pygame.font.SysFont('arial', 24)

# ========== TẠO NÚT GIAO DIỆN ==========
def create_buttons(algorithms):
    buttons = []
    num_buttons_per_row = 6
    button_width = 90
    button_height = 40
    x_start = 50
    y_start = board_size + 80
    spacing_x = 100
    spacing_y = 50

    for i, algo in enumerate(algorithms):
        row = i // num_buttons_per_row
        col = i % num_buttons_per_row
        rect = pygame.Rect(
            x_start + col * spacing_x,
            y_start + row * spacing_y,
            button_width,
            button_height,
        )
        buttons.append((rect, algo))

    stop_row = (len(algorithms) + num_buttons_per_row - 1) // num_buttons_per_row
    stop_col = (num_buttons_per_row - 1) // 2
    stop_button = pygame.Rect(
        x_start + stop_col * spacing_x,
        y_start + stop_row * spacing_y,
        button_width,
        button_height
    )
    buttons.append((stop_button, "Stop"))

    # Thêm nút Reset bên cạnh Stop
    reset_button = pygame.Rect(
        x_start + (stop_col + 1) * spacing_x,
        y_start + stop_row * spacing_y,
        button_width,
        button_height
    )
    buttons.append((reset_button, "Reset"))
    return buttons

# Danh sách thuật toán (thêm "Unobservable")
algorithms = [
    "BFS", "DFS", "DLS(L:7)", "IDS", "UCS", "Greedy",
    "A*", "GA", "Beam", "Hill", "SA", "AND-OR",
    "Belief", "Backtrack", "Forward", "Unob","AC-3"  # Thêm "Unobservable"
]
buttons = create_buttons(algorithms)

# ========== VẼ CÁC NÚT ==========
def draw_buttons():
    for rect, label in buttons:
        pygame.draw.rect(screen, BLACK, rect, 2)  # Vẽ viền đen
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

# ========== VẼ BÀN CỜ TRÁI ==========
def draw_board_left(queens=None):
    x, y = 50, 60  # Vị trí như cũ
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(x + col * cell_size, y + row * cell_size, cell_size, cell_size)
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, rect)
            if queens and row < len(queens) and queens[row] == col:
                pygame.draw.circle(screen, RED, rect.center, cell_size // 3)

# ========== VẼ BÀN CỜ PHẢI ==========
def draw_board_right(queens=None):
    x, y = board_size + 100, 60  # Vị trí như cũ
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(x + col * cell_size, y + row * cell_size, cell_size, cell_size)
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, rect)
            if queens and row < len(queens) and queens[row] == col:
                pygame.draw.circle(screen, RED, rect.center, cell_size // 3)

# ========== HIỂN THỊ THÔNG TIN ==========
def draw_info(current_algo, run_count, simulation_active=False, simulation_index=0,
              simulation_states=None, simulation_delay=30):
    """Hiển thị thông tin trạng thái thuật toán hiện tại (tại vị trí (50, 0))."""
    if current_algo:
        if simulation_active and simulation_states:
            if simulation_index < len(simulation_states) - 1:
                text = f"Algorithm: {current_algo} | Solution: {run_count} | Step: {simulation_index + 1}/{len(simulation_states)} | Delay: {simulation_delay}ms"
            else:
                text = f"Algorithm: {current_algo} | Solution: {run_count} | Completed | Delay: {simulation_delay}ms"
        else:
            text = f"Algorithm: {current_algo} | Solution: {run_count}"
    else:
        text = "No algorithm selected"

    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (50, 0))