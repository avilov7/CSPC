import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# 1. Read kinetics.csv (time, concentration)
data = np.loadtxt("kinetics.csv", delimiter=",", skiprows=1)
time = data[:, 0]
C_measured = data[:, 1]

# Set C0 to the first measured value
C0 = C_measured[0]


# 2. Objective function: total squared error(k)
def total_error(k):
    C_predicted = C0 * np.exp(-k * time)
    return np.sum((C_measured - C_predicted) ** 2)


# 3. Minimise error(k) with SLSQP, bounds=[(0, 5)], x0=0.5
result = minimize(total_error, x0=[0.5], method="SLSQP", bounds=[(0, 5)])
fitted_k = result.x[0]

# Print fitted k
print(f"Fitted rate constant k: {fitted_k:.4f}")

# 4. Plot data and fitted curve
t_dense = np.linspace(time.min(), time.max(), 200)
C_fitted = C0 * np.exp(-fitted_k * t_dense)

plt.figure(figsize=(7, 5))
plt.plot(time, C_measured, "o", label="Measured Data", color="red")
plt.plot(
    t_dense,
    C_fitted,
    "-",
    label=f"Fitted Curve (k = {fitted_k:.4f})",
    color="blue",
)
plt.xlabel("Time (s)")
plt.ylabel("Concentration (C)")
plt.title("First-Order Kinetics Fitting")
plt.legend()
plt.grid(True)

# Save kinetics.png
plt.savefig("kinetics.png", dpi=300)
plt.show()