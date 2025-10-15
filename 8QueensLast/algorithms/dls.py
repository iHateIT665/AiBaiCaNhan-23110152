from collections import deque
from utils import is_safe, observe, reset_observed_states

size = 8
dls_run_count = 0  # Đếm số lần chạy DLS
global_stack = deque()  # Stack toàn cục để lưu trạng thái

def DLS8queens(start_state=None, limit=7):
    global dls_run_count, global_stack
    dls_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    stack = deque()
    found_previous = False

    # Khởi tạo ngăn xếp
    if dls_run_count == 1 or not global_stack:
        # Lần đầu hoặc stack rỗng, bắt đầu từ state rỗng
        stack.append([] if not start_state else start_state[:])
        global_stack.clear()
        observe([] if not start_state else start_state[:])
    else:
        # Tiếp tục từ global_stack
        stack.extend(global_stack)
        if start_state and len(start_state) == limit:
            observe(start_state[:])  # Lưu start_state nếu là solution
            found_previous = True

    while stack:
        queens = stack.pop()  # Lấy state từ đỉnh ngăn xếp (DLS)
        row = len(queens)
        observe(queens[:])  # Lưu state hiện tại

        # Nếu đạt độ dài limit → là nghiệm
        if row == limit:
            if not start_state or (start_state and found_previous):
                print(queens)
                global_stack.clear()  # Xóa stack cũ
                # Thêm lại các state chưa khám phá vào global_stack
                global_stack.extend(stack)
                return queens
            elif start_state and queens == start_state:
                found_previous = True
            continue

        # Mở rộng nếu chưa vượt quá limit
        if row < limit:
            for col in range(size - 1, -1, -1):  # Thêm cột ngược để ưu tiên cột cao
                if is_safe(queens, row, col):
                    stack.append(queens + [col])

    # Nếu không tìm thấy nghiệm tiếp theo
    print(f"Không còn nghiệm kế tiếp với limit={limit}.")
    global_stack.clear()
    return None