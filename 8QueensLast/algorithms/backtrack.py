import random
import time
from utils import is_safe, observe, reset_observed_states, size,generate_safe_config



def Backtrack8queens(target_solution=None):
    """Backtracking cho 8-Queens: Bắt đầu từ partial 2 queens random an toàn,
    thử đặt từng hàng tiếp theo, quay lui nếu không thể (conflict hoặc dead-end).
    Observe mỗi state khi đặt/quay lui (tránh duplicate)."""
    reset_observed_states()
    random.seed(time.time())
    
    initial_partial = generate_safe_config(2)
    if not initial_partial:
        observe([], index="Initial-Empty")
        return []
    
    queens = initial_partial[:]
    observe(initial_partial[:], index="Initial state")
    
    row_start = 2
    if backtrack(queens, row_start):
        observe(queens[:], index="(Solution)")
        return queens
    else:
        observe([], index="No solution found")
        return []

def backtrack(queens, row, placed_in_row=False):
    """Hàm đệ quy backtrack: Thử đặt queen ở hàng 'row', quay lui nếu fail.
    Thêm param 'placed_in_row' để track nếu đã đặt ít nhất 1 queen ở row này (tránh duplicate observe)."""
    if row == size:
        return True
    
    # Thử từng cột cho hàng hiện tại
    for col in range(size):
        if is_safe(queens, row, col):
            # Đặt queen
            queens.append(col)
            observe(queens[:])
            placed_in_row = True  # Đã đặt ít nhất 1
            
            # Đệ quy hàng tiếp
            if backtrack(queens, row + 1, placed_in_row=True):
                return True
            
            # Quay lui: Không thể tiếp tục từ đây
            queens.pop()
            observe(queens[:], index="Back track")
    
    # Không cột nào safe → dead-end row, observe chỉ nếu chưa đặt gì (tránh duplicate với pop)
    if row > 0 and not placed_in_row:
        observe(queens[:], index=f"Backtrack")
    
    return False