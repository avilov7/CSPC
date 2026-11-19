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







# PW3 — Data, Distributions, Testing, and Causation

Data: `heart.csv` (Cleveland heart disease, UCI Machine Learning Repository / Kaggle, 303 patients) and `chemicals_cancer.csv` (synthetic, 1000 patients, Moodle).
Scripts: `pw3_session1.py` (tasks 1–3), `pw3_session2.py` (tasks 4–7 + bonus). Run with `python pw3_session1.py` / `python pw3_session2.py`.

## Session 1 — Characterising the data

**Shape of each variable** (`distributions.png`)
- `age`: roughly bell-shaped but slightly left-skewed (skew −0.21), with a flat/bimodal-looking top; mean 54.4, median 56.
- `chol`: right-skewed (skew 1.13, excess kurtosis 4.4) with a heavy right tail; one extreme patient at 564 mg/dl.
- `trestbps`: right-skewed (skew 0.70), a few high readings up to 200; mean ≈ median ≈ 130.
- `thalach`: left-skewed (skew −0.53) with a tail of low heart rates; mean 149.6, median 153.

![distributions](distributions.png)

**Normality verdicts** (Q-Q plots `qqplots.png` + Shapiro–Wilk and D'Agostino–Pearson tests; H0 = "data is normal")

| variable | Shapiro p | D'Agostino p | verdict | reasoning |
|---|---|---|---|---|
| age | 0.0061 | 0.0162 | not normal (mild) | Q-Q mostly on the line but tails bend away; both tests reject at 0.05. Closest to normal of the four. |
| chol | <0.0001 | <0.0001 | NOT normal | Upper tail curves sharply above the line, outlier at 564; strong skew and heavy tails. |
| trestbps | <0.0001 | <0.0001 | NOT normal | Upper tail bends above the line; right skew; visible stair-steps because values are rounded. |
| thalach | 0.0001 | 0.0012 | NOT normal | Q-Q is S-shaped, low end falls below the line (left skew). |

![qqplots](qqplots.png)

With n = 303 the tests are sensitive, so even small departures reject; the Q-Q plots show `age` is only mildly non-normal, while `chol` is clearly not normal. Conservative decision: treat all four as non-normal and use non-parametric methods.

## Session 2 — Conclusions

### 4. Do heart-disease patients reach a different maximum heart rate?
- Groups: disease (target = 1, n = 139), healthy (target = 0, n = 164).
- Normality inside each group: Shapiro p = 0.35 (disease), p = 0.0005 (healthy). `thalach` overall failed in Session 1, and the healthy group rejects normality, so I used the non-parametric **Mann–Whitney U** test (two-sided; H0: the two groups have the same distribution).
- Result: U = 5806.5, **p = 1.9e-13** → reject H0. Medians: 142 (disease) vs 161 (healthy). (Cross-check, Welch t-test: t = −7.86, p = 9e-14 — same conclusion.)
- Means with uncertainty (SE = std/√n, 95% CI ≈ mean ± 2·SE), `thalach_means_errorbars.png`:
  - healthy: 158.4 ± 1.5 (95% CI 155.4–161.4)
  - disease: 139.3 ± 1.9 (95% CI 135.4–143.1)
- The error bars are far apart and do not overlap, which agrees with the test: patients with heart disease reach a lower max heart rate, about 19 bpm lower. The p-value says the gap is not chance; the 19 bpm is the effect size.

![errorbars](thalach_means_errorbars.png)

### 5. age vs thalach (`age_vs_thalach.png`)
- Pearson r = −0.394 (p = 1e-12); Spearman ρ = −0.392 (p = 2e-12). Both agree, which matters because the variables are not normal.
![age vs thalach](age_vs_thalach.png)

- Interpretation: moderate negative relationship — older patients tend to have lower maximum heart rates (about −1 bpm per year of age). It is a tendency, not a rule: age explains only ~15% of the variance (r² ≈ 0.16).

### 6. Naive analysis (chemicals)
- benzene vs malignancy: r = 0.385; cadmium vs malignancy: r = 0.880 (both p ≈ 0).
- Taken at face value, **cadmium** looks like the cause.

### 7. Look again — controlling for `pollution_index`
- `pollution_index` is almost the same variable as cadmium (r = 0.982) and is also strongly related to malignancy (r = 0.895), while it is unrelated to benzene (r = 0.054). So it is a candidate confounder for cadmium. `age` is not (|r| < 0.1 with everything).
- Method: hold pollution fixed — split patients into narrow `pollution_index` bands and recompute each chemical's correlation with malignancy inside every band (`chemicals_within_bands.png`).

| band width | mean r benzene | mean r cadmium |
|---|---|---|
| 20 | 0.71 | 0.26 |
| 10 | 0.75 | 0.11 |
| 5 | 0.76 | 0.03 |

  Narrower bands = fairer "like with like", and cadmium's correlation melts away toward zero, while benzene's stays at ≈ 0.75 in every band. (Wide bands leave some pollution variation inside, which is why cadmium does not drop to 0 at width 20.)
- Cross-check, partial correlation (removing the linear effect of pollution): benzene r = 0.755 (p ≈ 1e-185); cadmium r = 0.013 (p = 0.69).
![within bands](chemicals_within_bands.png)

- **Conclusion: benzene is the real cause; cadmium only looked guilty** because it tracks the polluted area. The cadmium–malignancy link vanishes once pollution is held fixed (so it was never causal), whereas the benzene link survives.
- Caveat: this is still observational data. Controlling for one measured confounder supports but does not prove causation; only a randomised experiment would. Also, malignancy is capped at 100 (5.5% of rows), which slightly compresses correlations.

### Bonus — entropy of a categorical column
H = −Σ p log₂ p. `target`: p = (0.541, 0.459), H = 0.995 bits (max 1 bit) → almost perfectly balanced, as hard to guess as a coin flip. `sex`: p = (0.68, 0.32), H = 0.905 bits → somewhat lopsided, guessing "male" is right 68% of the time.nces on which evidence you trusted and why)
