# CSPC PW1 Lab A

## Results
- **Unit Tests:** All 3 tests passed (`pytest -v`).
- **Performance Comparison (N0 = 200,000):** 
  - Pure-Python loop time: [2.0147 ] s
  - NumPy time: [ 0.0002 ] s
  - Speed-up factor: NumPy is [12245.24]x faster.

## Conclusion
NumPy vectorization significantly speeds up radioactive decay simulation compared to standard Python loops.
## PW1 --- Lab B

- **Data Observation**: The observed data shows an exponential decay pattern over time.
- **Comparison**: The observed data points closely match the analytical decay law curve (N_0 * exp(-lambda * t)).
- **Snakemake Pipeline**: The Snakemake pipeline automates running `plot.py` to recreate `figure.png` whenever the source data or script changes.
pw 2 lab a
# CSPC PW2 — Lab A: Motion Analysis via Numerical Methods

## Experimental Results
- **Mean Acceleration:** -8.58 m/s²
- **Acceleration Standard Deviation (Noise):** 28.72 m/s²
- **Max Difference (Original vs Recovered Position):** 0.7846 m

## Physical Interpretation & Findings
1. **Numerical Differentiation Amplifies Noise:**
   Taking numerical derivatives relies on subtracting nearby position values and dividing by a small time step ($\Delta t$). This process severely amplifies measurement errors at each step, resulting in a highly noisy acceleration signal ($a.std \approx 28.72\text{ m/s}^2$).

2. **Numerical Integration Suppresses Noise:**
   Integrating acceleration back to velocity and position acts as a smoothing operator (summation). Despite the extreme noise in acceleration, double integration recovers the original position trajectory within a maximum deviation of less than $0.78\text{ m}$.

## Visualization
Generated motion curves saved in `motion.png`.
## PW2 --- Lab B: Optimization in Chemistry

### Part 2: Three Routes to a Minimum
* **Part 2A (Convex):** On $f(x) = (x - 3)^2 + 1$, Gradient descent, Newton's method, and SLSQP all converged smoothly to the global minimum at $x = 3.0$.
* **Part 2B (Harder Landscape):** On $g(x) = x^4 - 3x^2 + x + 5$:
  * **Starting at $x_0 = 0$:**
    * Gradient descent ($x \approx -1.301$) and SLSQP ($x \approx -1.301$) found the local minimum.
    * Newton's method converged to $x \approx 0.170$. Evaluating $g''(0.170) \approx -5.65 < 0$ proves Newton landed on a **local maximum**, illustrating that $g'(x) = 0$ alone does not guarantee a minimum.
  * **Starting at $x_0 = 2$:**
    * Gradient descent and Newton's method settled into the local minimum at $x \approx 1.131$ ($g'' \approx 9.35 > 0$).
    * SLSQP traversed the barrier to find the overall global minimum at $x \approx -1.301$.
* **Key Takeaway:** Optimization trajectories and outcomes depend heavily on algorithm selection, step size, and initial conditions ($x_0$).
### Part 3: Chemistry 1 — Reaction Rate Fitting
* **Model:** First-order reaction decay $C(t) = C_0 e^{-kt}$.
* **Method:** Minimised total squared error using SLSQP with $x_0 = 0.5$ and bounds $[0, 5]$.
* **Fitted Rate Constant ($k$):** $\approx 0.25$
* **Result:** The fitted exponential decay curve matches the experimental data points cleanly (saved as `kinetics.png`).
# PW3: Data, Distributions, Testing, and Causation

## Session 1

### Dataset
Heart Disease (Cleveland), UCI Machine Learning Repository / Kaggle.
303 patients. Columns used: age, chol, trestbps, thalach, target.
(Add a note here if you rebuilt heart.csv from the raw UCI file.)

### Distributions
![Distributions](distributions.png)

- **age:** (2-3 sentences in your own words)
- **chol:** 
- **trestbps:** 
- **thalach:** 

### Normality
![Q-Q plots](qqplots.png)

| Variable | Skew | Excess kurtosis | Shapiro p | Verdict |
|---|---|---|---|---|
| age | -0.21 | -0.53 | 0.006 | |
| chol | 1.13 | 4.40 | <0.0001 | |
| trestbps | 0.70 | 0.85 | <0.0001 | |
| thalach | -0.53 | -0.07 | 0.0001 | |

**Reasoning:** (for each variable, one or two sentences on which evidence you trusted and why)
