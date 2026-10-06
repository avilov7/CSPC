import numpy as np
from scipy.optimize import minimize, newton


def f(x):
    return (x - 3) ** 2 + 1


def fprime(x):
    return 2 * (x - 3)


print("--- Part 2A: f(x) = (x - 3)^2 + 1 (x0 = 0) ---")


x_2a = 0
learning_rate_2a = 0.1
for _ in range(100):
    x_2a = x_2a - learning_rate_2a * fprime(x_2a)
print(f"Gradient descent: {x_2a:.5f}")


result_newton_2a = newton(fprime, x0=0, fprime=lambda x: 2)
print(f"Newton:           {result_newton_2a:.5f}")


result_slsqp_2a = minimize(f, x0=0, method="SLSQP")
print(f"SLSQP:            {result_slsqp_2a.x[0]:.5f}\n")




def g(x):
    return x**4 - 3 * x**2 + x + 5


def gprime(x):
    return 4 * x**3 - 6 * x + 1


def gdouble_prime(x):
    return 12 * x**2 - 6


def run_part_2b(x0):
    print(f"--- Part 2B: g(x) = x^4 - 3x^2 + x + 5 (x0 = {x0}) ---")


    x = x0
    learning_rate = 0.01  
    for _ in range(1000):
        x = x - learning_rate * gprime(x)
    print(f"Gradient descent: x = {x:.5f}, g(x) = {g(x):.5f}")


    try:
        result_newton = newton(gprime, x0=x0, fprime=gdouble_prime)
        curvature = gdouble_prime(result_newton)

        if curvature > 0:
            nature = "Local Minimum"
        elif curvature < 0:
            nature = "Local Maximum"
        else:
            nature = "Inflexion Point"

        print(
            f"Newton:           x = {result_newton:.5f}, g''(x) = {curvature:.2f} ({nature})"
        )
    except Exception as e:
        print(f"Newton:           Failed to converge ({e})")


    result_slsqp = minimize(g, x0=x0, method="SLSQP")
    print(
        f"SLSQP:            x = {result_slsqp.x[0]:.5f}, g(x) = {result_slsqp.fun:.5f}\n"
    )



run_part_2b(0)
run_part_2b(2)