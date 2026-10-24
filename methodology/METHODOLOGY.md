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

| Result | Value |
|---|---|
| Long-run relationship (bounds test) | Confirmed |
| Error correction term | -0.0734 (about 7% of a deviation corrected per year) |
| TEMP, long run | Negative, significant: a 1% rise lowers AGDP by about 0.22% |
| LAND, long run | Positive, significant: a 1% rise raises AGDP by about 0.04% |
| RAIN and CO2, long run | Negative, not significant |
| LAB, long run | Positive, not significant |

Full tables and diagnostics are in `results/`.

## References

- Cobb, C. W. and Douglas, P. H. (1928). A theory of production. *American Economic Review*, 18(1), 139–165.
- Oghenekevwe, O. P. and Adesoye, O. S. (2024). Effect of climate change on agricultural productivity in Nigeria (1991–2022). *The Es Economics and Entrepreneurship*, 3(02), 209–218. https://doi.org/10.58812/esee.v3i02.264
- Pesaran, M. H., Shin, Y. and Smith, R. J. (2001). Bounds testing approaches to the analysis of level relationships. *Journal of Applied Econometrics*, 16(3), 289–326.
