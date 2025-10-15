from collections import deque
from utils import is_safe, observe, reset_observed_states

size = 8
dfs_run_count = 0  # Đếm số lần chạy DFS
global_stack = deque()  # Stack toàn cục để lưu trạng thái

def DFS8queens(start_state=None):
    global dfs_run_count, global_stack
    dfs_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    stack = deque()
    found_previous = False

    # Khởi tạo ngăn xếp
    if dfs_run_count == 1 or not global_stack:
        # Lần đầu hoặc stack rỗng, bắt đầu từ state rỗng
        stack.append([] if not start_state else start_state[:])
        global_stack.clear()
        observe([] if not start_state else start_state[:])
    else:
        # Tiếp tục từ global_stack
        stack.extend(global_stack)
        if start_state and len(start_state) == size:
            observe(start_state[:])  # Lưu start_state nếu là solution
            found_previous = True

    while stack:
        queens = stack.pop()  # Lấy state từ đỉnh ngăn xếp (DFS)
        row = len(queens)
        observe(queens[:])  # Lưu state hiện tại

        # Nếu đủ 8 hàng → là nghiệm
        if row == size:
            if not start_state or (start_state and found_previous):
                print(queens)
                global_stack.clear()  # Xóa stack cũ
                # Thêm lại các state chưa khám phá vào global_stack
                global_stack.extend(stack)
                return queens
            elif start_state and queens == start_state:
                found_previous = True
            continue

        # Mở rộng (thêm các cột theo thứ tự ngược để ưu tiên cột cao trước)
        for col in range(size - 1, -1, -1):
            if is_safe(queens, row, col):
                stack.append(queens + [col])

    # Nếu không tìm thấy nghiệm tiếp theo
    print("Không còn nghiệm kế tiếp.")
    global_stack.clear()
    return None