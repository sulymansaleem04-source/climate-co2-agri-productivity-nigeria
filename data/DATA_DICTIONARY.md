# Data Dictionary

**File:** `nigeria_agri_climate_1990_2024.csv`
**Coverage:** Nigeria, annual, 1990–2024 (35 observations, no missing values)

| Column | Description | Unit | Used in model as | Source |
|---|---|---|---|---|
| `YEAR` | Calendar year | – | time index | – |
| `AGDP` | Agricultural gross domestic product, constant local currency (proxy for agricultural productivity) | Billion naira | `LAGDP` = ln(AGDP) | World Bank WDI; CBN Statistical Bulletin |
| `TEMP` | Temperature change on land | °C | level (`TEMP`) | FAOSTAT; NiMet |
| `RAIN` | Average annual rainfall | mm | `LRAIN` = ln(RAIN) | FAOSTAT; NiMet |
| `CO2` | CO2 emissions excluding LULUCF, per capita | tCO2e per capita | level (`CO2`) | World Bank WDI; World Bank Climate Change Knowledge Portal |
| `LAND` | Agricultural land | % of total land area | level (`LAND`) | World Bank WDI; FAOSTAT |
| `LAB` | Employment in agriculture | % of total employment | `LLAB` = ln(LAB) | World Bank WDI; ILOSTAT |

## Notes

- **TEMP is a temperature-change (anomaly) series, not an absolute temperature.** Values are relative to a baseline, which is why some years are negative (e.g. 1992: -0.067).
- **Transformations.** AGDP, RAIN and LAB are natural-logged in the estimated model. TEMP, CO2 and LAND stay in levels. The CSV holds the raw, untransformed values.
- **Compilation.** Author's compilation (2026) from the sources above. Where sources overlap, official national sources were preferred for economic variables and international databases for climate variables.
-**Interpolation.** No interpolation was applied. All values are as obtained from the sources above, with no missing observations.
- **Integrity check.** The CSV matches Appendix B of the project report value for value.
