from heapq import heappush, heappop
from utils import is_safe, observe, reset_observed_states, g_attacked_by

size = 8
ucs_run_count = 0  # Đếm số lần chạy UCS
global_queue = []  # Queue toàn cục để lưu trạng thái

def UCS8queens(start_state=None):
    global ucs_run_count, global_queue
    ucs_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    # Sử dụng priority queue với (total_cost, queens, row, attacked)
    priority_queue = []
    found_previous = False

    # Khởi tạo
    if ucs_run_count == 1 or not global_queue:
        initial_state = [] if not start_state else start_state[:]
        initial_cost = 0
        heappush(priority_queue, (initial_cost, initial_state, 0, set()))  # (cost, queens, row, attacked)
        global_queue.clear()
        observe(initial_state, cost=initial_cost)  # Observe initial với cost
    else:
        initial_cost = 0
        priority_queue.extend([(initial_cost, state, len(state), set()) for state in global_queue])
        if start_state and len(start_state) == size:
            observe(start_state[:], cost=initial_cost)  # Observe start_state với cost
            found_previous = True

    while priority_queue:
        total_cost, queens, row, attacked = heappop(priority_queue)
        observe(queens[:], cost=total_cost)  # Observe state với cost

        # Nếu đủ 8 hàng → nghiệm
        if row == size:
            if not start_state or (start_state and found_previous):
                print(f"UCS found solution: {queens}")
                global_queue = [state for _, state, _, _ in priority_queue]  # Lưu state chưa khám phá
                return queens
            elif start_state and queens == start_state:
                found_previous = True
            continue

        # Mở rộng
        for col in range(size):
            if is_safe(queens, row, col):
                new_attacked = g_attacked_by(row, col)
                new_fee = len(new_attacked - attacked)  # Chi phí là số ô mới bị tấn công
                new_state = queens + [col]
                heappush(priority_queue, (total_cost + new_fee, new_state, row + 1, attacked | new_attacked))

    print("UCS không tìm thấy nghiệm kế tiếp.")
    global_queue.clear()
    return None