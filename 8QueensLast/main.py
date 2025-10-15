import pygame
import sys
from ui import draw_buttons, draw_board_left, draw_board_right, draw_info, screen, buttons
from utils import clear_file, reset_observed_states, write_states_to_file, get_observed_states
from algorithms.bfs import BFS8queens, global_queue
from algorithms.dfs import DFS8queens, global_stack
from algorithms.dls import DLS8queens
from algorithms.ucs import UCS8queens
from algorithms.greedy import Greedy8queens
from algorithms.astar import AStar8queens
from algorithms.ga import GA8queens
from algorithms.hill import HillClimbing8queens
from algorithms.beam import BeamSearch8queens
from algorithms.sa import SimulatedAnnealing8queens
from algorithms.andor import ANDOR8queens  # Thêm import cho AND-OR
from algorithms.belief import Belief8queens  # Thêm dòng này
from algorithms.unobservable import Unobservable8queens 
from algorithms.backtrack import Backtrack8queens 
from algorithms.forward import ForwardChecking8queens
from algorithms.ac3 import AC38queens

pygame.init()
clear_file()

target_solutions = [
    [0, 4, 7, 5, 2, 6, 1, 3],
    [1, 5, 7, 2, 0, 3, 6, 4],
    [2, 0, 6, 4, 7, 1, 3, 5]
]
target_solution_index = 0

current_algo = None
simulation_active = False
simulation_states = []
path_states = []
simulation_index = 0
simulation_index_right = 0
simulation_delay = 30
last_update_time = 0
last_update_time_right = 0
last_solution = None
run_count = 0
last_button_click_time = 0
click_cooldown = 500

def run_algorithm(algo_name, algo_func, target_solution=None):
    global current_algo, simulation_active, simulation_states, path_states
    global simulation_index, simulation_index_right, last_update_time, last_update_time_right
    global last_solution, run_count, target_solution_index

    print(f"Starting algorithm: {algo_name}")
    current_algo = algo_name
    reset_observed_states()
    run_count += 1
    solution = algo_func(target_solution if target_solution else last_solution)
    if algo_name == "GA":
        simulation_states = []
        write_states_to_file(get_observed_states(), run_count, algo_name)
    else:
        simulation_states = get_observed_states()
        write_states_to_file(simulation_states, run_count, algo_name)
    if solution:
        print(f"Solution found: {solution}")
        if algo_name in ["Greedy", "A*"]:
            target_solution_index += 1
        else:
            last_solution = solution
            path_states = [solution[:i] for i in range(len(solution) + 1)]
    else:
        print("No solution found")
        path_states = []
        simulation_states = get_observed_states()
    simulation_index = 0
    simulation_index_right = 0
    simulation_active = True
    last_update_time = pygame.time.get_ticks()
    last_update_time_right = last_update_time

def main():
    global current_algo, simulation_active, simulation_states, path_states
    global simulation_index, simulation_index_right, last_update_time, last_update_time_right
    global last_solution, run_count, simulation_delay, target_solution_index, last_button_click_time

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        screen.fill((200, 200, 200))

        draw_info(current_algo, run_count, simulation_active, simulation_index, simulation_states, simulation_delay)

        if simulation_active and simulation_states:
            if len(simulation_states) > 1 and simulation_index < len(simulation_states) - 1 and current_time - last_update_time > simulation_delay:
                simulation_index += 1
                last_update_time = current_time
                print(f"Updating left to state {simulation_index}/{len(simulation_states)}")
            if current_algo == "GA":
                draw_board_left()
            else:
                # Sửa: Lấy chỉ phần state [0] từ tuple (state, fitness, temp, cost)
                current_state = simulation_states[simulation_index][0] if simulation_states else None
                draw_board_left(current_state)
        else:
            draw_board_left()
            if current_algo == "GA" and current_time - last_update_time > simulation_delay:
                simulation_active = False

        if current_algo in ["Greedy", "A*"] and target_solutions:
            draw_board_right(target_solutions[target_solution_index % len(target_solutions)])
        elif simulation_active and path_states:
            if len(path_states) > 1 and simulation_index_right < len(path_states) - 1 and current_time - last_update_time_right > simulation_delay:
                simulation_index_right += 1
                last_update_time_right = current_time
                print(f"Updating right to path state {simulation_index_right}/{len(path_states)}")
            draw_board_right(path_states[simulation_index_right] if path_states else None)
        else:
            draw_board_right()

        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_time - last_button_click_time < click_cooldown:
                    continue
                mouse_pos = event.pos
                for rect, label in buttons:
                    if rect.collidepoint(mouse_pos):
                        print(f"Button clicked: {label}")
                        last_button_click_time = current_time
                        if label == "Stop":
                            current_algo = None
                            simulation_active = False
                            simulation_states = []
                            path_states = []
                            simulation_index = 0
                            simulation_index_right = 0
                            last_update_time = 0
                            last_update_time_right = 0
                        elif label == "Reset":
                            current_algo = None
                            simulation_active = False
                            simulation_states = []
                            path_states = []
                            simulation_index = 0
                            simulation_index_right = 0
                            simulation_delay = 100
                            last_update_time = 0
                            last_update_time_right = 0
                            last_solution = None
                            run_count = 0
                            target_solution_index = 0
                            clear_file()
                            from algorithms.bfs import global_queue
                            from algorithms.dfs import global_stack
                            from algorithms.dls import global_stack as dls_global_stack
                            from algorithms.ucs import global_queue as ucs_global_queue
                            global_queue.clear()
                            global_stack.clear()
                            dls_global_stack.clear()
                            ucs_global_queue.clear()
                            reset_observed_states()
                            print("Reset completed - back to initial state")
                        elif label == "BFS":
                            run_algorithm("BFS", BFS8queens)
                        elif label == "DFS":
                            run_algorithm("DFS", DFS8queens)
                        elif label == "DLS(L:7)":
                            run_algorithm("DLS(L:7)", lambda x: DLS8queens(x, limit=7))
                        elif label == "UCS":
                            run_algorithm("UCS", UCS8queens)
                        elif label == "Greedy":
                            run_algorithm("Greedy", Greedy8queens, target_solutions[target_solution_index % len(target_solutions)])
                        elif label == "A*":
                            run_algorithm("A*", AStar8queens, target_solutions[target_solution_index % len(target_solutions)])
                        elif label == "GA":
                            run_algorithm("GA", GA8queens)
                        elif label == "Hill":
                            run_algorithm("Hill", HillClimbing8queens)
                        elif label == "Beam":
                            run_algorithm("Beam", BeamSearch8queens)
                        elif label == "SA":
                            run_algorithm("SA", SimulatedAnnealing8queens)
                        elif label == "AND-OR":  # Thêm xử lý cho AND-OR
                            run_algorithm("AND-OR", ANDOR8queens)
                        elif label == "Belief":
                            run_algorithm("Belief", Belief8queens, target_solutions[target_solution_index % len(target_solutions)])
                        elif label == "Unob":
                            run_algorithm("Unobservable", Unobservable8queens)
                        elif label == "Backtrack":
                            run_algorithm("Backtrack", Backtrack8queens)
                        elif label == "Forward":
                            run_algorithm("Forward", ForwardChecking8queens)
                        elif label == "AC-3":
                            run_algorithm("AC-3", AC38queens)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    simulation_delay = max(50, simulation_delay - 100)
                    print(f"Delay updated: {simulation_delay}ms")
                if event.key == pygame.K_DOWN:
                    simulation_delay = min(5000, simulation_delay + 100)
                    print(f"Delay updated: {simulation_delay}ms")

        pygame.display.flip()

if __name__ == "__main__":
    main()