import time
import decay

N0 = 200000
rate = 0.4

# Pure-Python simulate_loop süresini ölç
start_loop = time.perf_counter()
decay.simulate_loop(N0, rate)
end_loop = time.perf_counter()
time_loop = end_loop - start_loop

# NumPy simulate süresini ölç
start_numpy = time.perf_counter()
decay.simulate(N0, rate)
end_numpy = time.perf_counter()
time_numpy = end_numpy - start_numpy

speedup = time_loop / time_numpy

print(f"Python loop time: {time_loop:.4f} seconds")
print(f"NumPy vector time: {time_numpy:.4f} seconds")
print(f"NumPy is {speedup:.2f}x faster than pure Python loop.")