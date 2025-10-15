import random
import time
from collections import deque
from utils import is_safe, observe, reset_observed_states, size, generate_safe_config

def get_domains_str(start_row, domains):
    """Helper: Tạo string mô tả domains từ start_row trở đi."""
    desc = []
    for r in range(start_row, size):
        dom_list = sorted(list(domains[r]))
        desc.append(f"row{r}:{dom_list}")
    return ', '.join(desc)

def revise(domain_i, domain_j, i, j, domains):
    """Revise function: Loại bỏ giá trị từ domain_i không có support trong domain_j cho ràng buộc giữa i và j.
    Observe chi tiết loại gì và domains thay đổi."""
    revised = False
    to_remove = []
    for val_i in sorted(list(domain_i)):
        supported = False
        for val_j in domain_j:
            # Ràng buộc: val_i != val_j and abs(val_i - val_j) != abs(i - j)
            if val_i != val_j and abs(val_i - val_j) != abs(i - j):
                supported = True
                break
        if not supported:
            to_remove.append(val_i)
    
    for val in to_remove:
        domain_i.remove(val)
        observe([], index=f"loại {val} khỏi domain row{i} vì không có support trong domain row{j}")
        revised = True
    
    # Ghi domain của 2 cái trong arc sau revise
    dom_i_str = sorted(list(domain_i))
    dom_j_str = sorted(list(domain_j))
    observe([], index=f"domain row{i}: {dom_i_str}, row{j}: {dom_j_str}")
    
    return revised

def AC3(domains):
    """AC-3: Enforce arc consistency trên tất cả directed arcs (i≠j), với trace chi tiết."""
    # Tạo queue với tất cả directed arcs (i,j) i≠j
    queue = deque()
    for i in range(size):
        for j in range(size):
            if i != j:
                queue.append((i, j))
    
    observe([], index="Khởi tạo agenda với tất cả directed arcs (i,j) i≠j")
    
    queue_set = set(queue)  # Để kiểm tra nhanh "in queue"
    
    while queue:
        i, j = queue.popleft()
        queue_set.remove((i, j))
        observe([], index=f"Xét arc ({i},{j}) từ agenda")
        
        revised = revise(domains[i], domains[j], i, j, domains)
        
        if revised:
            # Nếu revise, thêm lại tất cả incoming arcs vào i (k,i) với k≠i
            for k in range(size):
                if k != i:
                    incoming = (k, i)
                    if incoming not in queue_set:
                        queue.append(incoming)
                        queue_set.add(incoming)
                        observe([], index=f"Thêm arc ({k},{i}) vào agenda do revise ({i},{j}) thay đổi domain{i}")
    
    # Kiểm tra kết quả
    if all(len(domains[r]) > 0 for r in range(size)):
        observe([], index="AC-3 lọc thành công: tất cả domains không rỗng, tiến hành gọi backtrack để tìm lời giải dựa vào các domain")
        return True
    else:
        observe([], index="AC-3 lọc thất bại: có domain rỗng")
        return False

def backtrack_ac(queens, row, domains):
    """Backtrack đơn giản sau AC-3: Chọn từ domain consistent."""
    if row == size:
        return True
    
    domain_row = list(domains[row])
    if not domain_row:
        return False
    
    for col in sorted(domain_row):
        if is_safe(queens, row, col):
            queens.append(col)
            domains[row] = {col}
            observe(queens[:], index=get_domains_str(row + 1, domains))
            
            if backtrack_ac(queens, row + 1, domains):
                return True
            
            queens.pop()
    
    observe(queens[:], index=get_domains_str(row, domains))
    return False

def AC38queens(target_solution=None):
    """AC-3 cho 8-Queens: Initial 2 queens, prune initial, chạy AC-3 với trace,
    nếu thành công thì backtrack."""
    reset_observed_states()
    random.seed(time.time())
    
    initial_partial = generate_safe_config(2)
    if not initial_partial:
        observe([], index="Initial-Empty")
        return []
    
    # Init queens và domains
    queens = initial_partial[:]
    domains = [set(range(size)) for _ in range(size)]
    
    # Prune initial từ 0 và 1
    for r in range(2):
        col = queens[r]
        domains[r] = {col}
        for future_row in range(r + 1, size):
            domains[future_row].discard(col)
            diff = future_row - r
            diag1 = col + diff
            diag2 = col - diff
            if 0 <= diag1 < size:
                domains[future_row].discard(diag1)
            if 0 <= diag2 < size:
                domains[future_row].discard(diag2)
    
    observe(initial_partial[:], index=f"Initial sau khi xét các hàng còn lại với 0,1: {get_domains_str(2, domains)}")
    
    # Chạy AC-3
    success = AC3(domains)
    if not success:
        return []
    
    # Nếu thành công, gọi backtrack
    row_start = 2
    if backtrack_ac(queens, row_start, domains):
        observe(queens[:], index="Solution từ backtrack sau AC-3")
        return queens
    else:
        observe([], index="Backtrack thất bại sau AC-3")
        return []