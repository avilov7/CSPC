import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ---------- 1. Load ----------
df = pd.read_csv("heart.csv")
print("Shape:", df.shape)
print(df.head())
print("Duplicate rows:", df.duplicated().sum())  # Kaggle versions often contain duplicates
print("Missing values:\n", df.isna().sum())

cols = ["age", "chol", "trestbps", "thalach"]
X = df[cols]
print(X.describe())

# ---------- 2. Distributions (histogram + density, 4 panels) ----------
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
for ax, c in zip(axes.ravel(), cols):
    ax.hist(X[c], bins=20, density=True, alpha=0.6, edgecolor="black")
    X[c].plot.kde(ax=ax)
    ax.axvline(X[c].mean(), color="red", linestyle="--", label="mean")
    ax.axvline(X[c].median(), color="green", linestyle=":", label="median")
    ax.set_title(c)
    ax.legend()
plt.tight_layout()
plt.savefig("distributions.png", dpi=150)

# ---------- 3. Normality: Q-Q plots + numerical tests ----------
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
for ax, c in zip(axes.ravel(), cols):
    stats.probplot(X[c], dist="norm", plot=ax)
    ax.set_title(f"Q-Q plot: {c}")
plt.tight_layout()
plt.savefig("qqplots.png", dpi=150)

rows = []
for c in cols:
    x = X[c].dropna()
    w, p_sw = stats.shapiro(x)
    k2, p_dp = stats.normaltest(x)  # D'Agostino-Pearson (skew + kurtosis)
    rows.append({
        "variable": c,
        "n": len(x),
        "skew": stats.skew(x),
        "excess_kurtosis": stats.kurtosis(x),
        "shapiro_p": p_sw,
        "dagostino_p": p_dp,
    })
print(pd.DataFrame(rows).round(4).to_string(index=False))

plt.show()
