import random
from utils import observe, reset_observed_states, get_observed_states, initialize_individual, fitness, get_neighbors

size = 8

def HillClimbing8queens(target_solution=None):
    """Thuật toán Hill Climbing cho bài toán 8 quân hậu."""
    reset_observed_states()
    current = initialize_individual()
    print(f"Starting Hill Climbing with initial state: {current}")
    initial_fitness = fitness(current)
    # Observe initial state với neighbors của nó (tạo ngay để observe)
    initial_neighbors = get_neighbors(current)
    observe(current[:], fitness=initial_fitness, neighbors=initial_neighbors)  # Observe initial với neighbors
    
    max_iterations = 100  # Giới hạn để tránh vòng lặp vô hạn
    iteration = 0
    
    while iteration < max_iterations:
        current_fitness = fitness(current)
        if current_fitness == size:
            print(f"Hill Climbing found solution after {iteration} iterations: {current}")
            # Observe solution với neighbors cuối (nếu cần, hoặc None)
            solution_neighbors = get_neighbors(current)
            observe(current[:], fitness=current_fitness, neighbors=solution_neighbors)
            return current
        
        neighbors = get_neighbors(current)
        best_neighbor = current
        best_fitness = current_fitness
        
        # Observe current state với list neighbors (nhưng vì đã observe initial, giờ observe cho iteration này)
        observe(current[:], fitness=current_fitness, neighbors=neighbors)  # Observe current + neighbors của nó
        
        # Tìm best từ neighbors
        for neighbor in neighbors:
            neighbor_fitness = fitness(neighbor)
            if neighbor_fitness > best_fitness:
                best_neighbor = neighbor
                best_fitness = neighbor_fitness
        
        # Nếu không có trạng thái lân cận nào tốt hơn, dừng
        if best_fitness <= current_fitness:
            print(f"Hill Climbing stopped at local maximum after {iteration} iterations: {current} (Fitness: {current_fitness})")
            # Observe local max với neighbors
            observe(current[:], fitness=current_fitness, neighbors=neighbors)
            return None
        
        # Chuyển sang trạng thái lân cận tốt nhất
        current = best_neighbor
        print(f"Iteration {iteration + 1}: State = {current}, Fitness = {best_fitness}")
        iteration += 1
    
    final_fitness = fitness(current)
    print(f"Hill Climbing stopped after {max_iterations} iterations without solution: {current} (Fitness: {final_fitness})")
    # Observe final với neighbors
    final_neighbors = get_neighbors(current)
    observe(current[:], fitness=final_fitness, neighbors=final_neighbors)
    return None