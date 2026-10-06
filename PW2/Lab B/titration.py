import matplotlib.pyplot as plt
import numpy as np

# 1. Read titration.csv (volume base in mL, pH)
data = np.loadtxt("titration.csv", delimiter=",", skiprows=1)
volume = data[:, 0]
ph = data[:, 1]

# 2. Compute slope dpH/dV using np.gradient
slope = np.gradient(ph, volume)

# 3. Find volume where the slope is largest (np.argmax)
max_idx = np.argmax(slope)
eq_volume = volume[max_idx]
eq_ph = ph[max_idx]
max_slope = slope[max_idx]

print(f"Equivalence Point Volume: {eq_volume:.2f} mL (pH = {eq_ph:.2f}, Slope = {max_slope:.2f})")

# 4. Make two plots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: pH Curve
ax1.plot(volume, ph, color="blue", linewidth=2, label="pH Curve")
ax1.axvline(x=eq_volume, color="red", linestyle="--", label=f"Equivalence Point ({eq_volume:.1f} mL)")
ax1.scatter([eq_volume], [eq_ph], color="red", zorder=5)
ax1.set_xlabel("Volume of Base (mL)")
ax1.set_ylabel("pH")
ax1.set_title("Titration Curve (pH vs Volume)")
ax1.legend()
ax1.grid(True)

# Plot 2: Slope dpH/dV
ax2.plot(volume, slope, color="green", linewidth=2, label="dpH / dV (Slope)")
ax2.axvline(x=eq_volume, color="red", linestyle="--", label=f"Peak Slope ({eq_volume:.1f} mL)")
ax2.scatter([eq_volume], [max_slope], color="red", zorder=5)
ax2.set_xlabel("Volume of Base (mL)")
ax2.set_ylabel("dpH / dV")
ax2.set_title("Derivative (Slope vs Volume)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()

# Save plot as titration.png
plt.savefig("titration.png", dpi=300)
plt.show()