from decay import simulate, simulate_loop
import time

NO, lam = 200000, 0.4

# time of simulate()
sim_start_time = time.perf_counter()
result = simulate(NO, lam)
sim_stop_time = time.perf_counter()

sim_time = sim_stop_time - sim_start_time

#time of simulate_loop()
sim_loop_start_time = time.perf_counter()
result = simulate_loop(NO, lam)
sim_loop_stop_time = time.perf_counter()

sim_loop_time = sim_loop_stop_time - sim_loop_start_time

difference = sim_loop_time / sim_time

print(f"Time for simulate_loop(): {sim_loop_time}")
print(f"Time for simulate(): {sim_time}")
print(f"simulate() is faster than simalate_loop() by {difference} times")