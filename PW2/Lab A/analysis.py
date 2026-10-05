import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1: Read freefall.csv into arrays t and y
t, y = np.loadtxt('freefall.csv', delimiter=',', skiprows=1, unpack=True)

# TODO 2: Compute velocity and acceleration
v = np.gradient(y, t)
a = np.gradient(v, t)

print("Mean acceleration:", np.mean(a))

# Part 3: Noise analysis
print(f"Acceleration standard deviation (std): {a.std():.2f} m/s^2")

# TODO 3 (Part 4): Integrate back to recover velocity and position
v_rec = cumulative_trapezoid(a, t, initial=0) + v[0]
y_rec = cumulative_trapezoid(v_rec, t, initial=0) + y[0]

max_diff = np.max(np.abs(y - y_rec))
print(f"Max difference between original and recovered position: {max_diff:.4f} m")

# TODO 4 (Part 5): Plot 3 stacked panels and save motion.png
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

# Panel 1: Position
ax1.plot(t, y, label='Original Position', color='blue')
ax1.plot(t, y_rec, label='Recovered Position', color='orange', linestyle='--')
ax1.set_ylabel('Position (m)')
ax1.set_title('PW2 Lab A: Motion from Tracking Data')
ax1.legend()
ax1.grid(True)

# Panel 2: Velocity
ax2.plot(t, v, label='Velocity', color='green')
ax2.set_ylabel('Velocity (m/s)')
ax2.legend()
ax2.grid(True)

# Panel 3: Acceleration
ax3.plot(t, a, label='Acceleration', color='red', alpha=0.6)
ax3.axhline(-9.81, color='black', linestyle='--', label='True -9.81 m/s²')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Acceleration (m/s²)')
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.savefig('motion.png')
print("Successfully saved motion.png!")