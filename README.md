# CSPC PW1 Lab A
# CSPC PW1 Lab A Report

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
