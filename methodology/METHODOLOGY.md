# Methodology

**Study:** Navigating the Impact of Climate Change and Carbon Dioxide Emissions on Agricultural Productivity in Nigeria (1990–2024)
**Approach:** ARDL bounds testing (Pesaran, Shin and Smith, 2001)
**Software:** EViews

## 1. Theoretical framework

The study is anchored on the Production Function Theory (Cobb and Douglas, 1928), in which output depends on inputs such as land and labour. Climate variables are added as environmental inputs that shift agricultural output. The model is adapted from Oghenekevwe and Adesoye (2024), with agricultural land and agricultural labour added as control variables.

## 2. Model specification

Functional form:

```
AGDP = f(TEMP, RAIN, CO2, LAND, LAB)
```

Estimated log-linear form:

```
LnAGDP(t) = β0 + β1·TEMP(t) + β2·LnRAIN(t) + β3·CO2(t) + β4·LAND(t) + β5·LnLAB(t) + μ(t)
```

AGDP, RAIN and LAB are logged. TEMP, CO2 and LAND stay in levels. Coefficients on logged variables are read as elasticities, and the TEMP coefficient as a semi-elasticity. Variable definitions and sources are in [`data/DATA_DICTIONARY.md`](../data/DATA_DICTIONARY.md).

## 3. A priori expectations

| Variable | Expected sign | Reasoning |
|---|---|---|
| TEMP | negative | Heat stress, faster crop cycles and higher evapotranspiration reduce output |
| RAIN | positive | Over 90% of Nigerian agriculture is rainfed |
| CO2 | negative (long run) | Emissions drive climate change that harms output over time, outweighing any short-run fertilisation effect |
| LAND | positive | Expanding cultivated area raises output |
| LAB | positive | Agriculture is labour-intensive with limited mechanisation |

## 4. Estimation procedure

**Pre-estimation**
1. Trend analysis of each series, 1990–2024.
2. Descriptive statistics (mean, median, dispersion, skewness, kurtosis).
3. Pearson correlation matrix.
4. Phillips-Perron unit root test at level and first difference, to establish each variable's order of integration. The variables were of mixed order, with none integrated of order two, so ARDL is appropriate.
5. Lag length selection using AIC, SIC and HQ information criteria.

**Estimation**
6. ARDL bounds test for cointegration: a computed F-statistic above the upper critical bound indicates a long-run relationship.
7. Long-run coefficients from the ARDL model.
8. Error correction model for short-run dynamics and the speed of adjustment.

**Post-estimation diagnostics (5% significance level)**

| Test | Null hypothesis | Purpose |
|---|---|---|
| Breusch-Godfrey LM | No serial correlation | Residual independence |
| Breusch-Pagan-Godfrey | Homoscedastic residuals | Constant variance |
| Jarque-Bera | Normally distributed residuals | Normality |
| Ramsey RESET | Correct functional form | Specification |
| Variance inflation factors | – | Multicollinearity |
| CUSUM and CUSUM of squares | Stable parameters | Stability over the sample |

## 5. Headline results

**Specification and cointegration**

| Item | Result |
|---|---|
| Selected model | ARDL(1,2,0,0,0,0) by AIC, maximum 2 lags, constant (Case 2), 33 observations (1992–2024) |
| Bounds test F-statistic | 4.302, above the 5% upper bound of 4.013, so a long-run relationship exists |
| Error correction term | -0.0734 (about 7% of a deviation corrected per year) |

**Coefficients from the bounds-test (conditional error-correction) regression**

TEMP and LAND are in levels, so their coefficients are semi-elasticities (a one-unit change in the regressor changes AGDP by roughly 100 × coefficient per cent). LRAIN and LLAB are logged, so their coefficients are elasticities.

| Variable | Coefficient | p-value | Sign as expected |
|---|---|---|---|
| TEMP | -0.2219 | 0.039 | Yes |
| LRAIN | -0.1487 | 0.530 | No |
| CO2 | -0.4423 | 0.087 | Yes |
| LAND | 0.0353 | 0.018 | Yes |
| LLAB | 0.1851 | 0.419 | Yes |

**Long-run multipliers.** Each coefficient divided by the negative of the error correction term, with delta-method standard errors (computed in `code/ardl_replication.py`):

| Variable | Long-run multiplier | p-value |
|---|---|---|
| TEMP | -3.02 | 0.418 |
| LRAIN | -2.02 | 0.554 |
| CO2 | -6.02 | 0.283 |
| LAND | 0.48 | 0.349 |
| LLAB | 2.52 | 0.646 |

The long-run multipliers are imprecisely estimated with only 33 observations, and none is individually significant at 5%. The significance of TEMP and LAND in the table above refers to the bounds-test regression coefficients.

Full tables and diagnostics are in `results/`.

## References

- Cobb, C. W. and Douglas, P. H. (1928). A theory of production. *American Economic Review*, 18(1), 139–165.
- Oghenekevwe, O. P. and Adesoye, O. S. (2024). Effect of climate change on agricultural productivity in Nigeria (1991–2022). *The Es Economics and Entrepreneurship*, 3(02), 209–218. https://doi.org/10.58812/esee.v3i02.264
- Pesaran, M. H., Shin, Y. and Smith, R. J. (2001). Bounds testing approaches to the analysis of level relationships. *Journal of Applied Econometrics*, 16(3), 289–326.
