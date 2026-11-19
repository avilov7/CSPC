import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

heart = pd.read_csv("heart.csv")
chem = pd.read_csv("chemicals_cancer.csv")

# ---------- 4. Is the effect real? thalach: disease vs healthy ----------
print("=== TASK 4: thalach by target ===")
print(heart["target"].value_counts())
sick = heart.loc[heart["target"] == 1, "thalach"]
healthy = heart.loc[heart["target"] == 0, "thalach"]

# Gatekeeper: normality inside each group (the groups are what the test compares)
for name, g in [("disease", sick), ("healthy", healthy)]:
    w, p = stats.shapiro(g)
    print(f"Shapiro {name}: n={len(g)} W={w:.4f} p={p:.4g}")

# Q-Q plots per group
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, (name, g) in zip(axes, [("disease", sick), ("healthy", healthy)]):
    stats.probplot(g, dist="norm", plot=ax)
    ax.set_title(f"Q-Q plot: thalach, {name}")
plt.tight_layout()
plt.savefig("qq_thalach_groups.png", dpi=150)
plt.close()

# Non-parametric test (data failed normality) + parametric one as a cross-check
u, p_u = stats.mannwhitneyu(sick, healthy, alternative="two-sided")
t, p_t = stats.ttest_ind(sick, healthy, equal_var=False)
print(f"Mann-Whitney U={u:.1f} p={p_u:.3g}")
print(f"(cross-check) Welch t={t:.3f} p={p_t:.3g}")
print(f"medians: disease={sick.median():.1f} healthy={healthy.median():.1f}")

# Uncertainty on each mean: standard error and ~95% CI (mean +- 2*SE, as in lecture)
def mean_se(x):
    m = x.mean()
    se = x.std(ddof=1) / np.sqrt(len(x))
    return m, se

res = {}
for name, g in [("disease", sick), ("healthy", healthy)]:
    m, se = mean_se(g)
    res[name] = (m, se)
    print(f"{name}: mean={m:.2f} SE={se:.2f} 95% CI=[{m-2*se:.2f}, {m+2*se:.2f}]")

fig, ax = plt.subplots(figsize=(5, 5))
labels = ["healthy (0)", "disease (1)"]
means = [res["healthy"][0], res["disease"][0]]
errs = [2 * res["healthy"][1], 2 * res["disease"][1]]
ax.bar(labels, means, yerr=errs, capsize=8, color=["tab:blue", "tab:red"], alpha=0.7)
ax.set_ylabel("max heart rate (thalach), mean ± 2·SE (≈95% CI)")
ax.set_title("thalach by heart-disease status")
plt.tight_layout()
plt.savefig("thalach_means_errorbars.png", dpi=150)
plt.close()

# ---------- 5. age vs thalach ----------
print("\n=== TASK 5: age vs thalach ===")
r, p_r = stats.pearsonr(heart["age"], heart["thalach"])
rho, p_rho = stats.spearmanr(heart["age"], heart["thalach"])
print(f"Pearson r={r:.3f} p={p_r:.3g}")
print(f"Spearman rho={rho:.3f} p={p_rho:.3g}")

fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(heart["age"], heart["thalach"], s=15, alpha=0.6)
slope, intercept = np.polyfit(heart["age"], heart["thalach"], 1)
xs = np.linspace(heart["age"].min(), heart["age"].max(), 100)
ax.plot(xs, slope * xs + intercept, color="red", label=f"fit: slope={slope:.2f} bpm/yr")
ax.set_xlabel("age (years)")
ax.set_ylabel("thalach (max heart rate)")
ax.set_title(f"age vs thalach (r={r:.2f})")
ax.legend()
plt.tight_layout()
plt.savefig("age_vs_thalach.png", dpi=150)
plt.close()

# ---------- 6. Naive analysis ----------
print("\n=== TASK 6: naive correlations with malignancy ===")
for c in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(chem[c], chem["malignancy"])
    print(f"{c:8s} r={r:.3f} p={p:.3g}")
print("chem corr matrix:\n", chem.corr().round(3))

# ---------- 7. Look again: control for pollution_index ----------
print("\n=== TASK 7: controlling for pollution_index ===")
def band_table(width):
    out = []
    for lo in np.arange(0, 100, width):
        sub = chem[(chem["pollution_index"] >= lo) & (chem["pollution_index"] < lo + width)]
        if len(sub) < 25:  # too few points for a stable r
            continue
        rb, _ = stats.pearsonr(sub["benzene"], sub["malignancy"])
        rc, _ = stats.pearsonr(sub["cadmium"], sub["malignancy"])
        out.append({"band": f"{lo:g}-{lo+width:g}", "n": len(sub), "r_benzene": rb, "r_cadmium": rc})
    return pd.DataFrame(out)

# Narrower bands = fairer "like with like" (less leftover variation in pollution)
for width in (20, 10, 5):
    t = band_table(width)
    print(f"band width {width}: mean r benzene={t.r_benzene.mean():.2f}, mean r cadmium={t.r_cadmium.mean():.2f}")
rows_df = band_table(10)
print(rows_df.round(3).to_string(index=False))

# The lecture's simple version: one narrow band
narrow = chem[(chem["pollution_index"] > 40) & (chem["pollution_index"] < 60)]
for c in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(narrow[c], narrow["malignancy"])
    print(f"narrow band 40-60 (n={len(narrow)}): {c:8s} r={r:.3f} p={p:.3g}")

# Cross-check: partial correlation (remove the linear effect of pollution_index)
def residual(y, z):
    s, i = np.polyfit(z, y, 1)
    return y - (s * z + i)

pz = chem["pollution_index"]
for c in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(residual(chem[c], pz), residual(chem["malignancy"], pz))
    print(f"partial corr ({c} , malignancy | pollution): r={r:.3f} p={p:.3g}")
r_pc, _ = stats.pearsonr(chem["pollution_index"], chem["cadmium"])
r_pb, _ = stats.pearsonr(chem["pollution_index"], chem["benzene"])
print(f"pollution~cadmium r={r_pc:.3f}, pollution~benzene r={r_pb:.3f}")

# Is age a confounder too? (it is mentioned in the task)
for c in ["benzene", "cadmium", "pollution_index"]:
    r, p = stats.pearsonr(chem["age"], chem[c])
    print(f"age vs {c}: r={r:.3f}")

# Plot: overall vs within-band
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, c in zip(axes, ["benzene", "cadmium"]):
    sc = ax.scatter(chem[c], chem["malignancy"], c=chem["pollution_index"], s=10, cmap="viridis")
    ax.set_xlabel(c)
    ax.set_ylabel("malignancy")
    ax.set_title(f"{c} vs malignancy (colour = pollution_index)")
fig.colorbar(sc, ax=axes, label="pollution_index")
plt.savefig("chemicals_confounder.png", dpi=150, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
df_b = rows_df
x = np.arange(len(df_b))
ax.bar(x - 0.2, df_b["r_benzene"], 0.4, label="benzene")
ax.bar(x + 0.2, df_b["r_cadmium"], 0.4, label="cadmium")
ax.set_xticks(x)
ax.set_xticklabels(df_b["band"])
ax.set_xlabel("pollution_index band (width 10)")
plt.setp(ax.get_xticklabels(), rotation=45)
ax.set_ylabel("r with malignancy (within band)")
ax.axhline(0, color="k", lw=0.8)
ax.legend()
plt.tight_layout()
plt.savefig("chemicals_within_bands.png", dpi=150)
plt.close()

# ---------- Bonus: entropy of categorical columns ----------
print("\n=== BONUS: entropy ===")
for col in ["target", "sex"]:
    p = heart[col].value_counts(normalize=True)
    H = -(p * np.log2(p)).sum()
    print(f"{col}: proportions={p.round(3).to_dict()} entropy={H:.4f} bits (max {np.log2(len(p)):.0f} bit)")