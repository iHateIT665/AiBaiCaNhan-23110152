from heapq import heappush, heappop
from utils import is_safe, observe, reset_observed_states, h, g_attacked_by

size = 8
astar_run_count = 0  # Đếm số lần chạy A*

def AStar8queens(target_solution):
    global astar_run_count
    astar_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    # Sử dụng priority queue với f = g + h
    priority_queue = []
    initial_state = []
    initial_attacked = set()
    initial_f = 0  # f ban đầu = 0
    heappush(priority_queue, (initial_f, 0, initial_state, 0, initial_attacked))  # (f, h, queens, row, attacked)
    observe(initial_state, cost=initial_f)  # Lưu state ban đầu với cost f

    while priority_queue:
        f, h_cost, queens, row, attacked = heappop(priority_queue)  # Lấy state có f thấp nhất
        observe(queens[:], cost=f)  # Lưu state hiện tại với cost f

        # Nếu khớp target_solution
        if row == size and queens == target_solution:
            print(f"A* found target solution: {queens}")
            return queens

        # Mở rộng: chọn tất cả cột hợp lệ
        candidates = []
        for col in range(size):
            if is_safe(queens, row, col):
                h_val = h(col, row, target_solution)  # Khoảng cách cột
                g_val = len(g_attacked_by(row, col) - attacked)  # Số ô mới bị tấn công (delta g)
                new_g = len(attacked | g_attacked_by(row, col))  # g tích lũy = len(new_attacked)
                candidates.append((h_val, g_val, col, new_g))
        if candidates:
            candidates.sort()  # Sắp xếp theo h thấp nhất, g làm tie-breaker
            for h_val, g_delta, col, new_g in candidates:
                new_state = queens + [col]
                new_attacked = attacked | g_attacked_by(row, col)
                f_new = new_g + h_val  # f = g (tổng ô bị tấn công) + h
                heappush(priority_queue, (f_new, h_val, new_state, row + 1, new_attacked))

    print(f"A* không thể đạt target solution: {target_solution}")
    return None