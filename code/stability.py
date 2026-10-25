"""
Parameter stability: CUSUM and CUSUM of squares for the ARDL(1,2,0,0,0,0) model.
Uses recursive residuals (Brown, Durbin and Evans, 1975).

Run from the repository root:  python code/stability.py
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import recursive_olsresiduals
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/nigeria_agri_climate_1990_2024.csv").set_index("YEAR")
d = pd.DataFrame({"LAGDP": np.log(df.AGDP), "TEMP": df.TEMP, "LRAIN": np.log(df.RAIN),
                  "CO2": df.CO2, "LAND": df.LAND, "LLAB": np.log(df.LAB)})
X = sm.add_constant(pd.DataFrame({
    "LAGDP(-1)": d.LAGDP.shift(1), "TEMP": d.TEMP, "TEMP(-1)": d.TEMP.shift(1),
    "TEMP(-2)": d.TEMP.shift(2), "LRAIN": d.LRAIN, "CO2": d.CO2,
    "LAND": d.LAND, "LLAB": d.LLAB})).loc[1992:]
y = d.LAGDP.loc[1992:]
m = sm.OLS(y, X).fit()
T, k = int(m.nobs), X.shape[1]

# ------------------------------------------------------------------ CUSUM
rr = recursive_olsresiduals(m, skip=k, alpha=0.95)
n_rec = T - k
w = np.asarray(rr[0])[-n_rec:]                 # recursive residuals
cusum = np.asarray(rr[5])[-n_rec:]
ci = np.asarray(rr[6])[:, -n_rec:]
years = X.index[-n_rec:]
inside_cusum = bool(np.all((cusum >= ci[0]) & (cusum <= ci[1])))

# ------------------------------------------------------- CUSUM of squares
s = np.cumsum(w**2) / np.sum(w**2)
n = len(w)
t = np.arange(1, n + 1)
mid = (t) / n
# Approximate 5% bounds: +/- c0 around the mean line, c0 from the Kolmogorov-Smirnov
# approximation with effective sample size (T-k)/2 - 1 (Durbin, 1969).
c0 = 1.358 / np.sqrt((T - k) / 2 - 1)
lo, hi = mid - c0, mid + c0
inside_sq = bool(np.all((s >= lo) & (s <= hi)))
out_years = [int(yr) for yr, v, a, b in zip(years, s, lo, hi) if v < a or v > b]

print(f"Recursive residuals: {n} (years {years[0]}-{years[-1]})")
print(f"CUSUM within 5% bounds throughout: {inside_cusum}")
print(f"CUSUM of squares within approx. 5% bounds throughout: {inside_sq}")
if out_years:
    print("CUSUM of squares outside the bounds in:", out_years)

# ------------------------------------------------------------------ plot
fig, axs = plt.subplots(1, 2, figsize=(11, 4))
axs[0].plot(years, cusum, color="#1f5f8b", label="CUSUM")
axs[0].plot(years, ci[0], "r--", lw=1, label="5% bounds"); axs[0].plot(years, ci[1], "r--", lw=1)
axs[0].axhline(0, color="grey", lw=.6); axs[0].set_title("CUSUM", loc="left")
axs[1].plot(years, s, color="#1f5f8b", label="CUSUM of squares")
axs[1].plot(years, lo, "r--", lw=1, label="Approx. 5% bounds"); axs[1].plot(years, hi, "r--", lw=1)
axs[1].set_title("CUSUM of squares", loc="left")
for a in axs:
    a.legend(frameon=False, fontsize=8); a.grid(alpha=.25)
    for sp in ("top", "right"): a.spines[sp].set_visible(False)
fig.tight_layout()
import os; os.makedirs("results/figures", exist_ok=True)
fig.savefig("results/figures/stability_cusum.png", dpi=200)
