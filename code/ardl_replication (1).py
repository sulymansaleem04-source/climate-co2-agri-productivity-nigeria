"""
Replication of the ARDL(1,2,0,0,0,0) model from:
"Navigating the Impact of Climate Change and Carbon Dioxide Emissions on
Agricultural Productivity in Nigeria (1990-2024)"

Reproduces the EViews estimates using open-source tools.
Requires: pandas, numpy, scipy, statsmodels

Run from the repository root:  python code/ardl_replication.py
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# ---------------------------------------------------------------- data
df = pd.read_csv("data/nigeria_agri_climate_1990_2024.csv").set_index("YEAR")
d = pd.DataFrame({
    "LAGDP": np.log(df.AGDP),    # logged
    "TEMP": df.TEMP,             # level
    "LRAIN": np.log(df.RAIN),    # logged
    "CO2": df.CO2,               # level
    "LAND": df.LAND,             # level
    "LLAB": np.log(df.LAB),      # logged
})

# ------------------------------------------- ARDL(1,2,0,0,0,0), case 2
# Lag orders chosen by AIC (max 2) in EViews: LAGDP(1), TEMP(2), others 0.
X = pd.DataFrame({
    "LAGDP(-1)": d.LAGDP.shift(1),
    "TEMP": d.TEMP,
    "TEMP(-1)": d.TEMP.shift(1),
    "TEMP(-2)": d.TEMP.shift(2),
    "LRAIN": d.LRAIN,
    "CO2": d.CO2,
    "LAND": d.LAND,
    "LLAB": d.LLAB,
})
X = sm.add_constant(X).loc[1992:]          # estimation sample 1992-2024 (n=33)
y = d.LAGDP.loc[1992:]
m = sm.OLS(y, X).fit()

print("=== ARDL(1,2,0,0,0,0): dependent variable LAGDP ===")
print(m.summary().tables[1])
print(f"n = {int(m.nobs)}  R2 = {m.rsquared:.6f}  adj R2 = {m.rsquared_adj:.6f}  F = {m.fvalue:.3f}\n")

# ------------------------------------- error correction term and ECM form
b, V = m.params, m.cov_params()
rho = b["LAGDP(-1)"] - 1                    # error correction term
rho_se = np.sqrt(V.loc["LAGDP(-1)", "LAGDP(-1)"])
print(f"Error correction term (rho) = {rho:.5f}  (se {rho_se:.5f}, t = {rho/rho_se:.3f})\n")

# --------------------- bounds test: F-test that rho and all level terms = 0
# Conditional ECM (the form EViews uses for the bounds test):
#   D(LAGDP) = c + rho*LAGDP(-1) + th_T*TEMP(-1) + th_R*LRAIN + th_C*CO2
#              + th_L*LAND + th_B*LLAB + g0*D(TEMP) + g1*D(TEMP(-1)) + e
# Regressors with zero lags enter as current-period levels.
E = pd.DataFrame({
    "LAGDP(-1)": d.LAGDP.shift(1),
    "TEMP(-1)": d.TEMP.shift(1),
    "LRAIN": d.LRAIN, "CO2": d.CO2, "LAND": d.LAND, "LLAB": d.LLAB,
    "D(TEMP)": d.TEMP.diff(), "D(TEMP(-1))": d.TEMP.diff().shift(1),
})
E = sm.add_constant(E).loc[1992:]
dy = d.LAGDP.diff().loc[1992:]
ecm_u = sm.OLS(dy, E).fit()
# Case 2 (restricted constant): the null also restricts the intercept to zero.
level_terms = ["const", "LAGDP(-1)", "TEMP(-1)", "LRAIN", "CO2", "LAND", "LLAB"]
R = np.zeros((len(level_terms), len(ecm_u.params)))
for i, name in enumerate(level_terms):
    R[i, list(ecm_u.params.index).index(name)] = 1
F = float(ecm_u.f_test(R).fvalue)
print("=== Bounds test (Pesaran, Shin & Smith 2001), case 2, k = 5 ===")
print(f"F-statistic = {F:.4f}   (EViews: 4.3023)")
print("Critical values from the EViews bounds table, n = 35: 5% I(0) 2.804, I(1) 4.013; 1% I(0) 3.900, I(1) 5.419")
print("Conditional ECM level coefficients (these are what EViews labels 'Long-run Regressors'):")
print(ecm_u.params[level_terms[1:]].round(5).to_string(), "\n")

# -------------------------------- long-run multipliers (delta method)
print("=== Long-run multipliers: -theta_j / rho  (delta method SEs) ===")
rows = []
theta = {
    "TEMP": ["TEMP", "TEMP(-1)", "TEMP(-2)"],
    "LRAIN": ["LRAIN"], "CO2": ["CO2"], "LAND": ["LAND"], "LLAB": ["LLAB"],
}
for var, cols in theta.items():
    th = b[cols].sum()
    # g = -theta/rho with rho = phi - 1:  dg/dtheta_i = -1/rho,  dg/dphi = theta/rho**2
    idx = cols + ["LAGDP(-1)"]
    grad = np.array([-1 / rho] * len(cols) + [th / rho**2])
    lr = -th / rho
    se = float(np.sqrt(grad @ V.loc[idx, idx].values @ grad))
    t = lr / se
    p = 2 * (1 - stats.t.cdf(abs(t), df=m.df_resid))
    rows.append({"variable": var, "ecm_form_coef": th, "long_run_multiplier": lr,
                 "std_err": se, "t_stat": t, "p_value": p})
lr_tab = pd.DataFrame(rows).set_index("variable")
print(lr_tab.round(4))

import os
os.makedirs("results/tables", exist_ok=True)
lr_tab.round(6).to_csv("results/tables/long_run_multipliers_python.csv")
m.summary2().tables[1].round(6).to_csv("results/tables/ardl_estimates_python.csv")
