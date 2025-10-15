import random
from utils import observe, reset_observed_states, get_observed_states,initialize_individual,fitness

size = 8
ga_run_count = 0  # Đếm số lần chạy GA


def crossover(parent1, parent2):
    """Lai ghép: Chọn n vị trí từ parent1, còn lại từ parent2."""
    n = random.randint(1, size - 1)  # Tránh n = 0
    indices = random.sample(range(size), n)
    child = [-1] * size
    used_values = set()
    for i in indices:
        child[i] = parent1[i]
        used_values.add(parent1[i])
    remaining = [x for x in range(size) if x not in indices]
    for pos in remaining:
        for candidate in parent2:
            if candidate not in used_values:
                child[pos] = candidate
                used_values.add(candidate)
                break
        else:
            # Nếu không tìm được giá trị hợp lệ, chọn ngẫu nhiên
            available = [x for x in range(size) if x not in used_values]
            if available:
                child[pos] = random.choice(available)
                used_values.add(child[pos])
            else:
                child[pos] = random.randint(0, size - 1)  # Trường hợp hiếm
    return child

def mutate(individual, mutation_rate=0.1):
    """Đột biến: Hoán đổi ngẫu nhiên hai vị trí nếu ngẫu nhiên < mutation_rate."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(size), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def GA8queens(target_solution=None):
    global ga_run_count
    ga_run_count += 1
    print(f"Starting GA run {ga_run_count}")  # Debug

    reset_observed_states()
    population = [initialize_individual() for _ in range(4)]
    print("Thế hệ đầu là: ",population)
    generation = 0
    max_generations = 100  # Giữ theo yêu cầu

    while generation < max_generations:
        pop_with_fitness = [(ind, fitness(ind)) for ind in population]
        pop_sorted = sorted(pop_with_fitness, key=lambda x: x[1], reverse=True)
        gen_info = [(ind[:], fit) for ind, fit in pop_sorted]
        observe(gen_info)
        print(f"Generation {generation}: Best fitness = {pop_sorted[0][1]}")  # Debug

        if pop_sorted[0][1] == size:
            print(f"GA found solution after {generation} generations: {pop_sorted[0][0]}")
            return pop_sorted[0][0]

        parent1, parent2 = pop_sorted[0][0], pop_sorted[1][0]
        new_population = [parent1[:], parent2[:]]
        print("Thế hệ tiếp là: ")
        while len(new_population) < 4:
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
            print(" ",child)

        population = new_population
        generation += 1

    print("GA không tìm được solution trong giới hạn thế hệ")
    return None