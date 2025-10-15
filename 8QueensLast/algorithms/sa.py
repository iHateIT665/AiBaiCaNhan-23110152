import random
import math
from utils import observe, reset_observed_states, get_observed_states, initialize_individual, fitness

size = 8

def get_random_neighbor(individual):
    """Tạo một trạng thái lân cận ngẫu nhiên bằng cách hoán đổi hai vị trí."""
    neighbor = individual[:]
    i, j = random.sample(range(size), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def SimulatedAnnealing8queens(target_solution=None):
    """Thuật toán Simulated Annealing cho bài toán 8 quân hậu."""
    reset_observed_states()
    current = initialize_individual()
    print(f"Starting Simulated Annealing with initial state: {current}")
    current_fitness = fitness(current)  # Tính fitness ban đầu
    current_temp = 100.0  # Temp ban đầu để observe
    observe(current[:], fitness=current_fitness, temp=current_temp)
    
    initial_temp = 100.0
    cooling_rate = 0.95
    min_temp = 0.01
    max_iterations = 1000  # Giới hạn số vòng lặp
    
    current_temp = initial_temp
    iteration = 0
    
    while current_temp > min_temp and iteration < max_iterations:
        current_fitness = fitness(current)
        if current_fitness == size:
            print(f"Simulated Annealing found solution after {iteration} iterations: {current}")
            return current
        
        # Chọn một trạng thái lân cận ngẫu nhiên
        neighbor = get_random_neighbor(current)
        neighbor_fitness = fitness(neighbor)
        delta_e = neighbor_fitness - current_fitness
        
        # Chấp nhận trạng thái lân cận
        if delta_e > 0 or random.random() < math.exp(delta_e / current_temp):
            current = neighbor
            current_fitness = neighbor_fitness  # Cập nhật fitness
            observe(current[:], fitness=current_fitness, temp=current_temp)  # Observe với fitness và temp
            print(f"Iteration {iteration + 1}: State = {current}, Fitness = {current_fitness}, Temp = {current_temp:.2f}")
        
        # Giảm nhiệt độ
        current_temp *= cooling_rate
        iteration += 1
    
    final_fitness = fitness(current)  # Fitness cuối
    print(f"Simulated Annealing stopped after {iteration} iterations without solution: {current} (Fitness: {final_fitness})")
    observe(current[:], fitness=final_fitness, temp=current_temp)  # Observe trạng thái cuối
    return None