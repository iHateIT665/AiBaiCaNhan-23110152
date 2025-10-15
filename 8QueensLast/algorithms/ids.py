from utils import is_safe, observe, reset_observed_states
from algorithms.dls import DLS8queens, global_stack  # Import DLS và global_stack

size = 8
ids_run_count = 0  # Đếm số lần chạy IDS

def IDS8queens(start_state=None):
    global ids_run_count, global_stack
    ids_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    # Nếu start_state là solution đầy đủ, lưu nó và tiếp tục tìm solution kế tiếp
    if start_state and len(start_state) == size:
        observe(start_state[:])

    # IDS: tăng limit từ 0 đến size (8)
    for limit in range(size + 1):
        # Gọi DLS với limit hiện tại
        solution = DLS8queens(start_state, limit=limit)
        if solution and len(solution) == size:  # Chỉ trả về nếu là solution đầy đủ
            print(f"IDS found solution at limit {limit}: {solution}")
            # Không xóa global_stack vì DLS đã xử lý
            return solution

    # Nếu không tìm thấy solution
    print("Không còn nghiệm kế tiếp với IDS.")
    global_stack.clear()
    return None