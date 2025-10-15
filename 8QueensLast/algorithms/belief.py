import random
import time
from collections import deque
from utils import is_safe, observe, reset_observed_states, size,generate_safe_config



def Belief8queens(target_solution=None):
    """Belief state search (PO): BFS level-by-level từ partial 2 queens random, 
    mở rộng tất cả safe positions, prune nếu không thể mở rộng, 
    dừng khi TÌM THẤY ÍT NHẤT 1 SOLUTION (length 8)."""
    reset_observed_states()
    random.seed(time.time())
    
    initial_partial = generate_safe_config(2)  # Partial random an toàn với 2 queens (observation ban đầu)
    if not initial_partial:
        observe([], neighbors=[], index="Initial-Empty")
        return []
    
    # Queue chứa lists of partials (mỗi item là một level)
    belief_queue = deque([[initial_partial]])  # Bắt đầu với level 1: [initial]
    level = 1  # Bắt đầu từ lần 1
    
    while belief_queue:
        current_level = belief_queue.popleft()  # List các partials ở level hiện tại
        
        # Observe tất cả states ở level này
        for partial in current_level:
            observe(partial[:], index=f"xét lần {level}, {partial}")
        
        # Kiểm tra nếu có ÍT NHẤT 1 solution (length 8) trong level này
        solutions_in_level = [p for p in current_level if len(p) == size]
        if solutions_in_level:
            solution = solutions_in_level[0][:]  # Lấy solution đầu tiên
            observe(solution, index="Solution (PO: First found)")
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
        
        # Nếu next_level rỗng, không có solution
        if not next_level:
            return []
        
        # Enqueue next level
        belief_queue.append(next_level)
        level += 1
    
    return []  # No solution