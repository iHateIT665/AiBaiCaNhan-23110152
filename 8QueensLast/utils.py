import random
size = 8
observed_states = []  # Init global ở đây để an toàn

def initialize_individual():
    """Tạo một cá thể ngẫu nhiên với 8 quân hậu, mỗi quân trên một hàng."""
    return random.sample(range(size), size)

def is_safe(queens, row, col):
    for r, c in enumerate(queens):
        if c == col or abs(r - row) == abs(c - col):
            return False
    return True

def observe(state, fitness=None, temp=None, cost=None, neighbors=None, index=None):
    """Lưu trạng thái, fitness và nhiệt độ (nếu có) vào observed_states. Neighbors là list các neighbor của state."""
    global observed_states
    observed_states.append((state[:], fitness, temp, cost, neighbors, index))  # Tuple đầy đủ 6 phần tử

def reset_observed_states():
    global observed_states
    observed_states = []

def get_observed_states():
    return observed_states

def clear_file():
    with open('ixt.txt', 'w', encoding='utf-8') as f:
        f.write('')

def write_states_to_file(states, run_count, algo_name):
    with open('ixt.txt', 'a', encoding='utf-8') as f:
        f.write(f"Thuật toán {algo_name} lần {run_count}\n")
        if algo_name == "GA":
            for gen, full_state in enumerate(states):
                state = full_state[0] if isinstance(full_state, tuple) else full_state
                f.write(f"Generation {gen}:\n")
                for ind, fit in state:
                    f.write(f"{ind} (Fitness: {fit})\n")
                f.write("\n")
        else:
            step_num = 0
            for state_tuple in states:
                # Unpack optional (nếu thiếu, dùng None)
                if len(state_tuple) >= 6:
                    state, fitness_val, temp, cost, neighbors, index = state_tuple
                else:
                    state = state_tuple[0] if state_tuple else None
                    fitness_val = temp = cost = neighbors = index = None
                if state is None:
                    continue
                step_num += 1
                line = f"Step {step_num}: {state}"
                if fitness_val is not None:
                    line += f" (Fitness: {fitness_val})"
                if temp is not None:
                    line += f" (Temp: {temp:.2f})"
                if cost is not None:
                    line += f" (Cost: {cost})"
                if neighbors is not None:
                    all_neighbors_str = [str(nb) for nb in neighbors]
                    line += f" (Neighbors: len={len(neighbors)}, all={all_neighbors_str})"
                if index is not None:
                    line += f" (Index: {index})"
                f.write(f"{line}\n")
        f.write('\n')

def h(col, cur_row, solution):
    """Heuristic: Khoảng cách cột tại hàng cur_row so với solution."""
    return abs(solution[cur_row] - col)

def g_attacked_by(row, col):
    """Tính tập hợp ô bị tấn công bởi quân hậu tại (row, col)."""
    attacked = set()
    attacked.add((row, col))
    for j in range(size):
        attacked.add((row, j))
    for i in range(size):
        attacked.add((i, col))
    for d in range(-size, size):
        if 0 <= row + d < size and 0 <= col + d < size:
            attacked.add((row + d, col + d))
        if 0 <= row + d < size and 0 <= col - d < size:
            attacked.add((row + d, col - d))
    return attacked

def fitness(individual):
    """Tính số quân hậu hợp lệ (không bị tấn công lẫn nhau)."""
    conflicts = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if individual[i] == individual[j] or abs(i - j) == abs(individual[i] - individual[j]):
                conflicts += 1
    return size - conflicts

def get_neighbors(individual):
    """Tạo 10 trạng thái lân cận ngẫu nhiên bằng cách hoán đổi hai vị trí."""
    all_pairs = [(i, j) for i in range(size) for j in range(i + 1, size)]
    selected_pairs = random.sample(all_pairs, min(10, len(all_pairs)))
    neighbors = []
    for i, j in selected_pairs:
        neighbor = individual[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbors.append(neighbor)
    return neighbors

# Hàm phụ cho Beam nếu cần (không mix vào SA)
def observe_beam_states(beam, iteration, prefix):
    """Observe từng state trong beam với top 3 neighbors (sắp xếp theo fitness giảm dần)."""
    for beam_idx, state in enumerate(beam, start=1):
        all_neighbors = get_neighbors(state)
        # Sắp xếp neighbors theo fitness giảm dần và lấy top 3
        sorted_neighbors = sorted(all_neighbors, key=fitness, reverse=True)[:3]
        observe(state[:], fitness=fitness(state), neighbors=sorted_neighbors, index=f"{prefix}[{iteration}][{beam_idx}]")
def generate_safe_config(num_queens):
    """Tạo partial an toàn với num_queens hậu (backtrack với random shuffle col)."""
    cols = list(range(size))
    random.shuffle(cols)
    
    def backtrack(row, queens):
        if row == num_queens:
            return queens[:]
        for col in cols:
            if is_safe(queens, row, col):
                queens.append(col)
                result = backtrack(row + 1, queens)
                if result:
                    return result
                queens.pop()
        return None
    config = backtrack(0, [])
    if config is None:
        return [i for i in range(num_queens)]
    return config