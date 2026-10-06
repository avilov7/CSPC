import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize, newton

# K = 16 gives x ≈ 0.66, HI ≈ 1.33 mol as specified in the lab sheet
K = 16.0


# 1. Imbalance function: (2x)^2 / (1-x)^2 - K = 0
def k_imbalance(x):
    # Clip x slightly away from 1.0 to avoid division by zero
    x = np.clip(x, 0.0, 0.9999)
    return ((2 * x) ** 2) / ((1 - x) ** 2) - K


# Derivative for Newton's method
def k_imbalance_prime(x):
    x = np.clip(x, 0.0, 0.9999)
    return (8 * x) / ((1 - x) ** 3)


# 2. Method 1: Root-finding with Newton's method
x_newton = newton(k_imbalance, x0=0.5, fprime=k_imbalance_prime)


# 3. Method 2: Minimizing squared imbalance with SLSQP
def objective_slsqp(x):
    return k_imbalance(x[0]) ** 2


result_slsqp = minimize(
    objective_slsqp, x0=[0.5], method="SLSQP", bounds=[(0, 0.99)]
)
x_slsqp = result_slsqp.x[0]

# Print results
print(f"Equilibrium extent (Newton): x = {x_newton:.4f}")
print(f"Equilibrium extent (SLSQP):  x = {x_slsqp:.4f}")

# Calculate amounts at equilibrium
nH2_eq = 1 - x_slsqp
nI2_eq = 1 - x_slsqp
nHI_eq = 2 * x_slsqp

print("\nEquilibrium Amounts:")
print(f"H2 : {nH2_eq:.3f} mol")
print(f"I2 : {nI2_eq:.3f} mol")
print(f"HI : {nHI_eq:.3f} mol")

# 4. Plot component amounts vs extent x
x_vals = np.linspace(0, 0.95, 200)
nH2 = 1 - x_vals
nI2 = 1 - x_vals
nHI = 2 * x_vals

plt.figure(figsize=(7, 5))
plt.plot(x_vals, nH2, label="H2 (Reactant)", color="blue")
plt.plot(x_vals, nI2, "--", label="I2 (Reactant)", color="cyan")
plt.plot(x_vals, nHI, label="HI (Product)", color="red")

# Mark equilibrium point
plt.axvline(
    x=x_slsqp,
    color="black",
    linestyle=":",
    label=f"Equilibrium (x ≈ {x_slsqp:.2f})",
)
plt.scatter([x_slsqp] * 3, [nH2_eq, nI2_eq, nHI_eq], color="black", zorder=5)

plt.xlabel("Reaction Extent (x)")
plt.ylabel("Amount (mol)")
plt.title("Chemical Equilibrium: H2 + I2 ⇌ 2HI")
plt.legend()
plt.grid(True)

# Save plot
plt.savefig("equilibrium.png", dpi=300)
plt.show()