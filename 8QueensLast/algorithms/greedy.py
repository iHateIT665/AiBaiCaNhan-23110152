from heapq import heappush, heappop
from utils import is_safe, observe, reset_observed_states, h

size = 8
greedy_run_count = 0  # Đếm số lần chạy Greedy

def Greedy8queens(target_solution):
    global greedy_run_count
    greedy_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    # Sử dụng priority queue với h(col, row, target_solution)
    priority_queue = []
    heappush(priority_queue, (0, [], 0))  # (cost, queens, row)
    observe([])  # Lưu state ban đầu

    while priority_queue:
        _, queens, row = heappop(priority_queue)  # Lấy state có h thấp nhất
        observe(queens[:])  # Lưu state hiện tại

        # Nếu khớp target_solution
        if row == size and queens == target_solution:
            print(f"Greedy found target solution: {queens}")
            return queens

        # Mở rộng: chọn tất cả cột hợp lệ
        candidates = []
        for col in range(size):
            if is_safe(queens, row, col):
                cost = h(col, row, target_solution)  # Khoảng cách cột
                candidates.append((cost, col))
        if candidates:
            candidates.sort()  # Sắp xếp theo h thấp nhất
            for cost, col in candidates:  # Thêm tất cả cột hợp lệ
                heappush(priority_queue, (cost, queens + [col], row + 1))

    print(f"Greedy không thể đạt target solution: {target_solution}")
    return None