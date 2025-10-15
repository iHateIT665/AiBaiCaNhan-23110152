import random
import time
from utils import is_safe, observe, reset_observed_states, size, generate_safe_config

def get_domains_str(start_row, domains):
    """Helper: Tạo string mô tả domains từ start_row trở đi."""
    desc = []
    for r in range(start_row, size):
        dom_list = sorted(list(domains[r]))
        desc.append(f"row{r}:{dom_list}")
    return ', '.join(desc)

def ForwardChecking8queens(target_solution=None):
    """Forward Checking cho 8-Queens: Bắt đầu từ partial 2 queens random an toàn,
    mỗi hàng có domain {0-7}, gán col từ domain, forward check update domains sau,
    nếu domain rỗng → backtrack. Observe chỉ domains chưa chọn."""
    reset_observed_states()
    random.seed(time.time())
    
    initial_partial = generate_safe_config(2)
    if not initial_partial:
        observe([], index="Initial-Empty")
        return []
    
    # Init queens và domains
    queens = initial_partial[:]
    domains = [set(range(size)) for _ in range(size)]
    
    # Apply initial: Fix domains[0:2], remove conflicts from future rows
    for r in range(2):
        col = queens[r]
        domains[r] = {col}
        for future_row in range(r + 1, size):
            # Remove same col
            domains[future_row].discard(col)
            # Remove diagonals
            diff = future_row - r
            diag1 = col + diff
            diag2 = col - diff
            if 0 <= diag1 < size:
                domains[future_row].discard(diag1)
            if 0 <= diag2 < size:
                domains[future_row].discard(diag2)
    
    observe(initial_partial[:], index=get_domains_str(2, domains))
    
    row_start = 2
    if backtrack_fc(queens, row_start, domains):
        observe(queens[:])
        return queens
    else:
        observe([])
        return []

def backtrack_fc(queens, row, domains):
    """Hàm đệ quy forward checking: Thử gán từ domain[row], forward check, backtrack nếu fail."""
    if row == size:
        return True
    
    domain_row = domains[row].copy()
    if not domain_row:
        observe(queens[:], index=get_domains_str(row, domains))
        return False
    
    for col in sorted(domain_row):  # Sorted để consistent
        if is_safe(queens, row, col):  # Check với past assignments
            # Gán
            queens.append(col)
            old_domain_row = domains[row].copy()
            domains[row] = {col}
            
            # Forward check
            success, saved_domains = forward_check(queens, row, domains)
            if success:
                # Observe domains sau gán và forward check thành công
                observe(queens[:], index=get_domains_str(row + 1, domains))
                
                # Đệ quy
                if backtrack_fc(queens, row + 1, domains):
                    return True
            
            # Undo
            queens.pop()
            domains[row] = old_domain_row
            
            # Restore future domains
            for fr in range(row + 1, size):
                domains[fr] = saved_domains[fr]
            
            # Observe domains sau backtrack
            observe(queens[:], index=get_domains_str(row, domains))
    
    # Hết col → backtrack
    observe(queens[:], index=get_domains_str(row, domains))
    return False

def forward_check(queens, row, domains):
    """Forward check: Update domains future rows, check empty, return success và saved cho undo."""
    col = queens[row]
    saved_domains = [d.copy() for d in domains]
    for future_row in range(row + 1, size):
        # Remove same col
        domains[future_row].discard(col)
        # Remove diagonals
        diff = future_row - row
        diag1 = col + diff
        diag2 = col - diff
        if 0 <= diag1 < size:
            domains[future_row].discard(diag1)
        if 0 <= diag2 < size:
            domains[future_row].discard(diag2)
        
        if not domains[future_row]:
            # Undo all updates in this forward_check
            for fr in range(row + 1, future_row + 1):
                domains[fr] = saved_domains[fr]
            # Observe domains sau fail forward check
            observe(queens[:], index=get_domains_str(row + 1, domains))
            return False, saved_domains
    
    return True, saved_domains