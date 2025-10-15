from collections import deque
from utils import is_safe, observe, reset_observed_states

size = 8
bfs_run_count = 0  # Đếm số lần chạy BFS
global_queue = deque()  # Queue toàn cục để lưu trạng thái

def BFS8queens(start_state=None):
    global bfs_run_count, global_queue
    bfs_run_count += 1

    # Reset observed_states trước khi chạy
    reset_observed_states()

    queue = deque()
    found_previous = False

    # Khởi tạo hàng đợi
    if bfs_run_count == 1 or not global_queue:
        # Lần đầu hoặc queue rỗng, bắt đầu từ state rỗng
        queue.append([] if not start_state else start_state[:])
        global_queue.clear()
        observe([] if not start_state else start_state[:])
    else:
        # Tiếp tục từ global_queue
        queue.extend(global_queue)
        if start_state and len(start_state) == size:
            observe(start_state[:])  # Lưu start_state nếu là solution
            found_previous = True

    while queue:
        queens = queue.popleft()
        row = len(queens)
        observe(queens[:])  # Lưu state hiện tại

        # Nếu đủ 8 hàng → là nghiệm
        if row == size:
            if not start_state or (start_state and found_previous):
                print(queens)
                global_queue.clear()  # Xóa queue cũ
                # Thêm lại các state chưa khám phá vào global_queue
                global_queue.extend(queue)
                return queens
            elif start_state and queens == start_state:
                found_previous = True
            continue

        # Mở rộng
        for col in range(size):
            if is_safe(queens, row, col):
                queue.append(queens + [col])

    # Nếu không tìm thấy nghiệm tiếp theo
    print("Không còn nghiệm kế tiếp.")
    global_queue.clear()
    return None