import random
from utils import observe, reset_observed_states, get_observed_states, initialize_individual, fitness, get_neighbors,observe_beam_states,clear_file,write_states_to_file
# Giả sử utils.py đã có, nhưng tôi sẽ paste lại đầy đủ ở dưới để tự chạy

size = 8
beam_width = 3  # Beam width nhỏ để demo
max_iterations = 5  # Số iterations demo
neighbors_per_state = 10  # Số neighbors tạo từ mỗi state (như code gốc)

def BeamSearch8queens(target_solution=None, run_count=1):
    """Thuật toán Beam Search cho bài toán 8 quân hậu, với observe và ghi file beam + top 3 neighbors."""
    reset_observed_states()
    clear_file()  # Clear file trước khi ghi
    
    # Bắt đầu từ 1 state ban đầu
    beam = [initialize_individual()]
    print(f"Starting Beam Search with initial beam (1 state): {beam[0]}")
    
    # Observe initial beam (step 0)
    iteration = 0
    observe_beam_states(beam, iteration, "Initial")
    write_states_to_file(get_observed_states(), run_count, "BeamSearch")  # Ghi initial vào file
    
    while iteration < max_iterations:
        # Kiểm tra nếu có giải pháp trong beam hiện tại
        for state in beam:
            if fitness(state) == size:
                print(f"Beam Search found solution after {iteration} iterations: {state}")
                # Observe solution
                observe(state[:], fitness=fitness(state), neighbors=None, index="Solution")
                write_states_to_file(get_observed_states(), run_count, "BeamSearch")
                return state
        
        # Tạo tất cả new neighbors từ beam hiện tại
        all_new_neighbors = []
        for state in beam:
            neighbors = get_neighbors(state)
            all_new_neighbors.extend([(neighbor, fitness(neighbor)) for neighbor in neighbors])
        
        # Pool = current beam + all_new_neighbors
        pool = [(state, fitness(state)) for state in beam] + all_new_neighbors
        
        # Sắp xếp pool theo fitness giảm dần
        pool.sort(key=lambda x: x[1], reverse=True)
        
        # Chọn beam_width trạng thái tốt nhất từ pool làm beam mới
        beam = [candidate for candidate, _ in pool[:beam_width]]
        
        # Observe selected beam với top 3 neighbors (sắp xếp theo fitness)
        iteration += 1
        observe_beam_states(beam, iteration, "Beam")
        write_states_to_file(get_observed_states(), run_count, "BeamSearch")  # Ghi beam mới vào file
        
        print(f"Iteration {iteration}: Pool size={len(pool)}, Best fitness = {fitness(beam[0])}")
    
    # Observe beam cuối
    observe_beam_states(beam, max_iterations, "Final")
    write_states_to_file(get_observed_states(), run_count, "BeamSearch")
    
    print(f"Beam Search stopped after {max_iterations} iterations without solution. Best fitness: {fitness(beam[0])}")
    return None

