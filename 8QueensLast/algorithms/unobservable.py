import random
import time
from collections import deque
from utils import is_safe, observe, reset_observed_states, size  # Giả sử size=8 từ utils

def Unobservable8queens(target_solution=None):
    """Conformant search (Unobservable): BFS level-by-level từ empty partial, 
    mở rộng tất cả safe positions, prune nếu không thể mở rộng, 
    dừng khi TẤT CẢ states ở level là solutions (length 8)."""
    reset_observed_states()
    random.seed(time.time())
    
    # Đầu vào: Empty partial (không observation nào)
    initial_empty = []  # Belief ban đầu: { [] }
    
    # Queue chứa lists of partials (mỗi item là một level)
    belief_queue = deque([[initial_empty]])  # Bắt đầu với level 1: [ [] ]
    level = 1  # Bắt đầu từ lần 1
    
    while belief_queue:
        current_level = belief_queue.popleft()  # List các partials ở level hiện tại
        
        # Observe tất cả states ở level này
        for partial in current_level:
            observe(partial[:], index=f"xét lần {level}, {partial}")
        
        # Kiểm tra nếu TẤT CẢ level là solutions (length 8)
        if all(len(partial) == size for partial in current_level):
            # Tất cả đều full → conformant success, lấy bất kỳ
            solution = current_level[0][:]
            observe(solution, index="Solution (Unobs: All conformant)")
            return solution
        
        # Mở rộng next level: tất cả possible safe extensions
        next_level = []
        for partial in current_level:
            row = len(partial)
            if row == size:
                continue  # Đã full, không mở rộng
            
            safe_cols = [col for col in range(size) if is_safe(partial, row, col)]
            if not safe_cols:
                continue  # Prune: không thể mở rộng, bỏ qua
            
            # Thêm tất cả extensions
            for col in safe_cols:
                new_partial = partial + [col]
                next_level.append(new_partial)
        
        # Nếu next_level rỗng, không có conformant solution
        if not next_level:
            return []
        
        # Enqueue next level
        belief_queue.append(next_level)
        level += 1
    
    return []  # No conformant solution