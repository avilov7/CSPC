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
