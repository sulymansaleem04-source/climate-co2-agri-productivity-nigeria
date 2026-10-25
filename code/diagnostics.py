"""
Post-estimation diagnostics for the ARDL(1,2,0,0,0,0) model.
Reproduces the EViews tests: Breusch-Godfrey, Breusch-Pagan-Godfrey,
Jarque-Bera, Ramsey RESET and variance inflation factors.

Run from the repository root:  python code/diagnostics.py
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

df = pd.read_csv("data/nigeria_agri_climate_1990_2024.csv").set_index("YEAR")
d = pd.DataFrame({"LAGDP": np.log(df.AGDP), "TEMP": df.TEMP, "LRAIN": np.log(df.RAIN),
                  "CO2": df.CO2, "LAND": df.LAND, "LLAB": np.log(df.LAB)})
X = sm.add_constant(pd.DataFrame({
    "LAGDP(-1)": d.LAGDP.shift(1), "TEMP": d.TEMP, "TEMP(-1)": d.TEMP.shift(1),
    "TEMP(-2)": d.TEMP.shift(2), "LRAIN": d.LRAIN, "CO2": d.CO2,
    "LAND": d.LAND, "LLAB": d.LLAB})).loc[1992:]
y = d.LAGDP.loc[1992:]
m = sm.OLS(y, X).fit()
e = m.resid
n, k = int(m.nobs), X.shape[1]
rows = []

# Breusch-Godfrey LM test, 2 lags, pre-sample residuals set to zero (as in EViews)
L = pd.concat([e.shift(i).fillna(0) for i in (1, 2)], axis=1)
L.columns = ["RESID(-1)", "RESID(-2)"]
aux = sm.OLS(e, pd.concat([X, L], axis=1)).fit()
lm = n * aux.rsquared
F_bg = aux.compare_f_test(sm.OLS(e, X).fit())
rows += [("Breusch-Godfrey (2 lags)", "F-statistic", F_bg[0], F_bg[1]),
         ("Breusch-Godfrey (2 lags)", "Obs*R-squared", lm, 1 - stats.chi2.cdf(lm, 2))]

# Breusch-Pagan-Godfrey: regress squared residuals on the regressors (excluding constant)
aux = sm.OLS(e**2, X).fit()
lm = n * aux.rsquared
ess = ((aux.fittedvalues - (e**2).mean())**2).sum()
sigma2 = m.ssr / (n - k)   # EViews uses the degrees-of-freedom corrected variance
scaled = ess / (2 * sigma2**2)
rows += [("Breusch-Pagan-Godfrey", "F-statistic", aux.fvalue, aux.f_pvalue),
         ("Breusch-Pagan-Godfrey", "Obs*R-squared", lm, 1 - stats.chi2.cdf(lm, k - 1)),
         ("Breusch-Pagan-Godfrey", "Scaled explained SS", scaled, 1 - stats.chi2.cdf(scaled, k - 1))]

# Jarque-Bera on residuals
S, K = stats.skew(e), stats.kurtosis(e, fisher=False)
jb = n / 6 * (S**2 + (K - 3)**2 / 4)
rows.append(("Jarque-Bera (residuals)", "JB statistic", jb, 1 - stats.chi2.cdf(jb, 2)))

# Ramsey RESET: add powers 2 and 3 of the fitted values
Z = X.copy()
Z["FITTED^2"], Z["FITTED^3"] = m.fittedvalues**2, m.fittedvalues**3
u = sm.OLS(y, Z).fit()
F_r = u.compare_f_test(m)
lr = 2 * (u.llf - m.llf)
rows += [("Ramsey RESET (powers 2-3)", "F-statistic", F_r[0], F_r[1]),
         ("Ramsey RESET (powers 2-3)", "Likelihood ratio", lr, 1 - stats.chi2.cdf(lr, 2))]

out = pd.DataFrame(rows, columns=["test", "statistic", "value", "p_value"])
print(out.round(4).to_string(index=False))

# Variance inflation factors (centred), regressors excluding the constant
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
Xv = X.drop(columns="const")
v = pd.Series({c: vif(sm.add_constant(Xv).values, i + 1) for i, c in enumerate(Xv.columns)}, name="centred_VIF")
print("\nCentred VIFs:\n", v.round(3).to_string())

import os
os.makedirs("results/tables", exist_ok=True)
out.round(6).to_csv("results/tables/diagnostic_tests_python.csv", index=False)
v.round(4).to_csv("results/tables/vif_python.csv")
