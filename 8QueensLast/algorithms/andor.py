from utils import is_safe, observe, reset_observed_states, get_observed_states, g_attacked_by, size, fitness
import random

class ANDORState:
    def __init__(self, queens=[], row=0, type_node='OR', parent=None):
        self.queens = queens
        self.row = row
        self.type = type_node
        self.children = []
        self.parent = parent
        self.value = float('inf') if type_node == 'OR' else 0
        self.index = f"{type_node}[{row}]"

def heuristic_h(queens, row):
    return size - row

def expand_and_or(root):
    if root.row == size:  # Lá
        conflicts = size - fitness(root.queens)  # Tính conflicts nếu cần, nhưng bỏ observe
        root.value = 0 if conflicts == 0 else float('inf')
        observe(root.queens[:], neighbors=[], index=root.index)  # Bỏ fitness/cost
        return root.value == 0
    
    if root.type == 'OR':
        candidates = []
        for col in range(size):
            if is_safe(root.queens, root.row, col):
                child = ANDORState(root.queens + [col], root.row + 1, 'AND', root)
                root.children.append(child)
                candidates.append(str(col))
        # Observe OR với full neighbors, bỏ fitness/cost
        observe(root.queens[:], neighbors=candidates, index=root.index)
        # Mở rộng con
        successes = [expand_and_or(child) for child in root.children]
        root.value = min([0 if s else float('inf') for s in successes]) if root.children else float('inf')
        return root.value == 0
    else:  # AND
        checks = []
        all_ok = True
        for prev_row in range(root.row - 1):
            conflict = abs(root.queens[root.row - 1] - root.queens[prev_row]) == abs((root.row - 1) - prev_row)
            check_str = f"Check vs row{prev_row}: {'OK' if not conflict else 'Conflict'}"
            checks.append(check_str)
            if conflict:
                all_ok = False
        # Observe AND với full checks, bỏ fitness/cost
        observe(root.queens[:], neighbors=checks, index=root.index)
        root.value = 0 if all_ok else float('inf')
        if all_ok and root.row < size:
            next_or = ANDORState(root.queens, root.row, 'OR', root)
            root.children.append(next_or)
            return expand_and_or(next_or)
        return all_ok

def ANDOR8queens(target_solution=None):
    reset_observed_states()
    root = ANDORState([], 0, 'OR')
    print("Starting AND-OR search.")
    solution_found = expand_and_or(root)
    if solution_found:
        print(f"Solution: {root.queens}")
        return root.queens
    return None