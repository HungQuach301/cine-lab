# Cluster C — Official US data (Census Bureau) — "Why US Cities Stopped Building the Corner Apartment Block"

Accessed: 2026-10-12 (all files fetched by curl that day). Raw files in `raw/`, scripts in `scripts/`, full computed output in `results.json`.
Reproduce:
```
P=/opt/cine/bin/python; S=<scratchpad>; C=$S/src/C
$P -m pip install --target $S/pylib xlrd openpyxl      # parsers only, outside any env
$P -I -W ignore $C/scripts/analyze.py $S/pylib $C/raw $C/results.json
$P -I $C/scripts/summarize.py $C/results.json
```
"Our calculation" = computed by `scripts/analyze.py` from the published values; formula given each time. Census values are rounded as published (NRC: thousands to 0.1; SOC Characteristics: whole thousands).

## Source codes

| Code | Source | URL | Vintage |
|---|---|---|---|
| C-NRC-CO | U.S. Census Bureau & HUD, Survey of Construction (SOC), *New Privately-Owned Housing Units Completed*, sheet `Annual` | https://www.census.gov/construction/nrc/xls/comps_cust.xlsx | file last-modified 24 Sep 2026; data through Aug 2026; tied to NRC release CB26-147, 17 Sep 2026 |
| C-NRC-ST | same, *Units Started*, sheet `Annual` | https://www.census.gov/construction/nrc/xls/starts_cust.xlsx | same |
| C-NRC-BP | Census Building Permits Survey (BPS), *Units Authorized by Building Permits in Permit-Issuing Places*, sheet `Annual` | https://www.census.gov/construction/nrc/xls/permits_cust.xlsx | same |
| C-NRC-REL | Monthly New Residential Construction, August 2026, Release CB26-147 (17 Sep 2026; next release 20 Oct 2026) | https://www.census.gov/construction/nrc/pdf/newresconst.pdf | |
| C-BPS-ST | BPS annual state file 2025 (row `US`) | https://www2.census.gov/econ/bps/State/st2025a.txt | last-modified 14 May 2026 |
| C-CHARS-MFU | SOC, Characteristics of New Housing, *Number of Multifamily Units Completed by Number of Units Per Building*, sheet `MFUUnitsperBldgAll`, United States block | https://www.census.gov/construction/chars/xls/mfu_unitsperbldg_cust.xls | last-modified 1 Jul 2026 (data through 2025) |
| C-CHARS-MFB | same, *Number of Multifamily Buildings Completed by Number of Units Per Building* | https://www.census.gov/construction/chars/xls/mfb_unitsperbldg_cust.xls | same |
| C-CHARS-FLR | same, *MF Buildings Completed by Number of Floors* (`MFBFloorsAll`) and *MF Units Completed by Number of Floors in Building* (`MFUnitsFloorsAll`) | https://www.census.gov/construction/chars/xls/mfb_floors_cust.xls ; .../mfu_floors_cust.xls | same |
| C-ACS-24 | ACS 2024 1-year, table-based Summary File, tables B25024 (Units in Structure, all housing units) and B25127 (Tenure by Year Structure Built by Units in Structure, occupied units); geo `0100000US` | https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/1YRData/acsdt1y2024-b25024.dat ; ...-b25127.dat ; labels: .../documentation/ACS20241YR_Table_Shells.txt | files dated 11 Sep 2025 |

Notes on access: api.census.gov returned HTTP 302 → `missing_key.html` (key required), so the ACS Summary File (same estimates) was used instead. The legacy URL `nrc/xls/co_cust.xls` still resolves but is stale (last-modified 16 Feb 2024, ends at 2023 with an unrevised 2023 = 1,452.5k); the current `.xlsx` files linked from https://www.census.gov/construction/nrc/data/series.html were used. SHA-256 of each raw file: see bottom.

Definitions (Census, https://www.census.gov/construction/bps/definitions.html): one-unit = single-family incl. townhouses/row houses separated by ground-to-roof walls; multifamily structures are classified by number of units in the structure. Excludes manufactured homes, group quarters, and units created inside existing buildings (conversions, ADUs inside a house). Pre-1999 single-family estimates include a 3.3% upward adjustment (old .xls footnote) — does not affect 2–4 or 5+ columns.

## 1. NRC completions / starts / permits by units in structure (thousands of units, annual, United States)

Columns in sheet `Annual`: A=Year, B=Total, C=1 unit, D=2 to 4 units, E=5 units or more. Header row 5–6; units "Thousands of units. Detail may not add to total because of rounding." (cell A2).

### Completions (C-NRC-CO), series 1968–2025
| Year | xlsx row | Total | 1 unit | 2–4 | 5+ | 2–4 share* | 5+ share* |
|---|---|---|---|---|---|---|---|
| 1970 | 9 | 1,418.4 | 801.8 | 85.1 | 531.5 | 6.00% | 37.47% |
| 1971 | 10 | 1,706.1 | 1,014.0 | 106.1 | 586.1 | 6.22% | 34.35% |
| 1972 | 11 | 2,003.9 | 1,160.2 | 119.2 | 724.7 | 5.95% | 36.16% |
| 1973 | 12 | 2,100.5 | 1,197.2 | 123.5 | 779.8 | 5.88% | 37.12% |
| 1974 | 13 | 1,728.5 | 940.3 | 95.3 | 692.9 | 5.51% | 40.09% |
| **1979** | 18 | 1,870.8 | 1,301.0 | **124.9 (peak)** | 444.9 | 6.68% | 23.78% |
| 1985 | 24 | 1,703.3 | 1,072.5 | 97.2 | 533.6 | 5.71% | 31.33% |
| 1990 | 29 | 1,308.0 | 966.0 | 44.8 | 297.3 | 3.43% | 22.73% |
| 2000 | 39 | 1,573.7 | 1,241.8 | 27.3 | 304.7 | 1.73% | 19.36% |
| 2006 | 45 | 1,979.4 | 1,654.5 | 40.8 | 284.2 | 2.06% | 14.36% |
| 2010 | 49 | 651.7 | 496.3 | 8.9 | 146.5 | 1.37% | 22.48% |
| **2021** | 60 | 1,341.0 | 969.7 | **7.7 (series low)** | 363.7 | 0.57% | 27.12% |
| 2023 | 62 | 1,448.8 | 998.9 | 11.7 | 438.3 | 0.81% | 30.25% |
| **2024** | 63 | 1,626.9 | 1,018.6 | **16.6** | 591.7 | 1.02% | 36.37% |
| **2025** | 64 | 1,488.5 | 1,004.8 | **16.0** | 467.7 | 1.07% | 31.42% |

*Our calculation: share = column D (or E) / column B, same row.
- Peak 2–4 completions: **1979, 124.9 thousand** (cell `Annual!D18`). Close second 1973 = 123.5k (D12); 1980 = 118.8k is listed in results.json.
- 2025 vs peak (our calculation): 16.0 / 124.9 = **12.8%** (≈ an 87% decline).
- Early-1970s pooled share (our calculation): Σ D(1970–74) / Σ B(1970–74) = 529.2 / 8,957.4 = **5.91%**; 2025 = 16.0 / 1,488.5 = **1.07%**. Average 2–4 completions 1970–74 = 105.8k/yr.
- 5+ completions: peak **1973, 779.8k** (`Annual!E12`); pooled 1970–74 share 37.01%; 2025 = 467.7k = 31.42%.
- 2026 year-to-date (sheet `Not Seasonally Adjusted`, Jan–Aug sum, our calculation): 2–4 = 9.8k (vs 10.7k Jan–Aug 2025); total 865.3k. The SA sheet shows 2–4 as "(S)" (no stable seasonality), so no SAAR exists for 2–4.

### Starts (C-NRC-ST), 2–4 series begins 1964 (1959–63 = NA)
- Peak 2–4 starts: **1972, 141.2k** (`Annual!D20`); 1972 total 2,356.6k, 5+ 906.2k (5+ peak, E20).
- 2024: total 1,367.1, 1u 1,012.9, **2–4 18.0**, 5+ 336.2 (row 72). 2025: total 1,355.8, 1u 939.7, **2–4 19.2**, 5+ 396.9 (row 73).
- Series low for 2–4: 2011, 10.9k (D59).
- Shares (our calculation, D/B): 1970–74 pooled 5.78%; 2024 1.32%; 2025 **1.42%**. 2025 = 13.6% of the 1972 peak.
- 2026 Jan–Aug NSA: 2–4 = 9.6k (vs 13.2k Jan–Aug 2025).

### Building permits (C-NRC-BP), series 1959–2025
- Peak 2–4 permits: **1972, 148.6k** (`Annual!D20`). Low: 2009, 20.7k (D57).
- 2024: total 1,478.0, 2–4 **54.5** (row 72); 2025: total 1,431.6, 1u 911.9, 2–4 **55.7**, 5+ 464.0 (row 73).
- Shares (our calculation): 1970–74 pooled 6.57%; 2025 **3.89%**. 2025 = 37.5% of the 1972 peak.

### BPS 2025 annual, US row (C-BPS-ST, `st2025a.txt`, line beginning `202599,US`)
| Structure | Buildings | Units | Value ($000) |
|---|---|---|---|
| 1 unit | 911,903 | 911,903 | 292,551,243 |
| 2 units | 18,375 | 36,748 | 6,204,050 |
| 3–4 units | 5,268 | 18,993 | 3,124,860 |
| 5+ units | 16,414 | 463,972 | 77,170,364 |
2–4 units = 36,748 + 18,993 = **55,741** (matches 55.7k above); 2–4 share = 55,741 / 1,431,616 = **3.89%** (our calculation). These are "imputed" estimates for all permit-issuing places; the file also has "reported" columns (not used).

**Caution — permits vs starts/completions for 2–4:** permits (55.7k in 2025) are ~3× starts (19.2k) and completions (16.0k). Starts/completions come from the SOC sample and the SOC-based Characteristics table independently gives 2-unit 7k + 3–4-unit 9k = 16k completed in 2025, consistent with NRC completions. Census documentation consulted (definitions pages) does not explain the gap; do not mix the series in one comparison. For "how many were built", use completions; for "how many were authorized", use permits, and say which.

## 2. Existing stock — ACS 2024 1-year (C-ACS-24)

### B25024 Units in Structure, all housing units, United States (estimate ± 90% MOE)
| Line | Category | Units | Share* |
|---|---|---|---|
| E001 | Total | 146,740,964 ± 8,590 | 100% |
| E002+E003 | 1 unit (detached 89,646,723 + attached 9,316,139) | 98,962,862 | 67.44% |
| E004 | 2 | 4,724,007 ± 44,178 | 3.22% |
| E005 | 3 or 4 | 6,335,116 ± 48,425 | 4.32% |
| | **2–4 (E004+E005)** | **11,059,123** | **7.54%** |
| E006 | 5 to 9 | 6,505,738 ± 54,722 | 4.43% |
| E007 | 10 to 19 | 6,278,389 ± 59,165 | 4.28% |
| | **5–19 (E006+E007)** | **12,784,127** | **8.71%** |
| | 2–19 (E004..E007) | 23,843,250 | 16.25% |
| E008+E009 | 20+ (5,625,736 + 10,169,614) | 15,795,350 | 10.76% |
| E010 / E011 | Mobile home / Boat, RV, van | 7,939,191 / 200,311 | |
*Our calculation: category / E001.

### B25127 Tenure × Year Built × Units in Structure (OCCUPIED units only), United States
Our calculation: owner line + renter line for each year-built band (owner lines 003–044, renter lines 046–087; "2 to 4" = band subtotal line +2, "5 to 19" = +3). Check: sum of the 12 band subtotals = 132,737,146 = B25127_E001.

| Year built | 2–4 units (occ.) | % of all occupied 2–4 stock | 5–19 units (occ.) | % of 5–19 stock | 2–4 as % of all units built in band |
|---|---|---|---|---|---|
| 1939 or earlier | 2,248,479 | **23.21%** | 998,325 | 8.91% | 15.26% |
| 1940–1959 | 1,282,274 | 13.23% | 843,926 | 7.53% | 7.24% |
| 1960–1979 | 2,351,246 | 24.27% | 2,984,841 | 26.63% | 7.63% |
| 1980–1999 | 2,164,566 | 22.34% | 3,356,781 | 29.94% | 6.65% |
| 2000–2019 | 1,491,624 | 15.39% | 2,723,202 | 24.29% | 4.73% |
| 2020 or later | 151,086 | **1.56%** | 303,263 | 2.71% | 2.79% |
| Total | 9,689,275 | 100% | 11,210,338 | 100% | |

- 2–4 stock built before 1960: 36.44%; built 2000 or later: **16.95%** (our calculation).
- 81.92% of occupied 2–4 units are renter-occupied (our calculation).
- Caveat: ACS year built is respondent-reported; older bands are less precise. B25127 covers occupied units only (132.7M), so totals differ from B25024 (146.7M incl. vacant). MOEs for B25127 are in the raw file (not propagated).

## 3. Characteristics of New Housing — multifamily completions by units per building (C-CHARS-MFU, United States block; thousands of units)
Sheet `MFUUnitsperBldgAll`; cols B=Total, C=2 units, D=3–4, E=5–9, F=10–19, G=20–29, H=30–49, I=50+. **Footnote: "Data prior to 1999 include 3 to 4 units" in the 2-unit column** (so 1972–1998 col C = 2–4).

| Year | xls row | MF total | 2u | 3–4u | 5–9u | 10–19u | 2–4* | 5–19* | 5–19 % of MF* | 5–19 % of all completions** |
|---|---|---|---|---|---|---|---|---|---|---|
| 1972 | 9 | 828 | 118 (2–4) | NA | 143 | 213 | 118 | 356 | 43.0% | 17.8% |
| 1973 | 10 | 840 | 121 (2–4) | NA | 167 | 210 | 121 | **377 (peak)** | 44.9% | 18.0% |
| 1985 | 22 | 631 | 97 (2–4) | NA | 137 | 198 | 97 | 335 | 53.1% | 19.7% |
| 1999 | 36 | 334 | 13 | 23 | 56 | 91 | 36 | 147 | 44.0% | 9.2% |
| 2010 | 47 | 155 | 4 | 5 | 10 | 19 | 9 | 29 | 18.7% | 4.5% |
| 2020 | 57 | 375 | 5 | 5 | 17 | 33 | 10 | 50 | 13.3% | 3.9% |
| 2024 | 61 | 608 | 6 | 11 | 14 | 29 | 17 | 43 | 7.1% | 2.6% |
| 2025 | 62 | 484 | 7 | 9 | 11 | 37 | **16** | **48** | 9.9% | 3.2% |
*Our calculation: 2–4 = C+D; 5–19 = E+F; % of MF = (E+F)/B. **Denominator = NRC completions total (C-NRC-CO col B) for the same year. 2025 RSE: 2u 20%, 3–4u 47%, 5–9u 20%, 10–19u 23% (row 64) — the small-building estimates are imprecise.
- 50+ unit buildings: 169k (20%) in 1972 vs 278k (57%) of MF units in 2025 (published percent columns).
- Buildings (C-CHARS-MFB, `MFBUnitsperBldgAll`, thousands of buildings): 1978 total 73, of which 2–4-unit 44 (60%); 2025 total 17, of which 2-unit 3 + 3–4-unit 2 (published shares 20% + 12%).

### Stories (C-CHARS-FLR)
No median number of stories is published by units-per-building. Published: MF **buildings** completed by floors (`MFBFloorsAll`, US row 40) 2025: total 17k; 1–2 floors 5k (32%), 3 floors 8k (46%), 4+ floors 4k (22%). MF **units** by floors (`MFUnitsFloorsAll`, row 40) 2025: 484k; 1–2 floors 34k (7%), 3 floors 157k (32%), 4+ floors 293k (61%). Series with a separate 3-floor category starts 2013 ("Data prior to 2013 include 3 floors").

## 4. Building permits 2–4, latest year
2025 (latest annual): **55,741 units in 2–4-unit structures** (36,748 in 2-unit + 18,993 in 3–4-unit buildings; 23,643 buildings) = 3.89% of 1,431,616 permitted units. 2024: 54.5k. Peak 148.6k in 1972.

## Metrics within ±5% of a round-number or comparison worth flagging
- 2–4 completions 2024 (16.6k) vs 2025 (16.0k): essentially flat; 1973 (123.5k) vs 1979 (124.9k) peak differ by 1.1% — saying "peaked in the 1970s" is safer than naming one year.
- 5–9 (4.43%) vs 10–19 (4.28%) shares of stock are within ±5% of each other.

## Raw file SHA-256
```
2e4d8a460131be19ca06e87bb478e12ccb4dd44892369245049ee0e463454ad4  ACS20241YR_Table_Shells.txt
00680fe89713a9545184db0b3caa0347341d3ada6096d9f8be3bef0407fb6eb9  acsdt1y2024-b25024.dat
361e315b6d60ef5810d6724551b747e1776e733333738f30b3f89317fc48dc55  acsdt1y2024-b25127.dat
62ce743e1714eacecbf8592d43a3128b101eb4aa366c419a3f59d54f9fb83986  comps_cust.xlsx
742f9d7abff0e69c5e63ec335bcbdc9e81d6b7e3b1d2b7da55ec7902d7bd4a35  comps_quarterly_cust.xlsx
4ab3087555793b661fc7cdef0418b32db52e4eacb0f8ba895018d496066a3cae  mfb_floors_cust.xls
041a9f29d3eacb6502a8600bdee65985c51d0f7d968489eb2f540a536f67de42  mfb_unitsperbldg_cust.xls
dd98391c553729f567e50b043c093ca27c841e978b66ff7003a7ab94cdafc9b3  mfu_floors_cust.xls
050d012bf79398c42b40897f07d0a085e72a1c6ddb2b48b5c2251c91310f30b4  mfu_unitsperbldg_cust.xls
4c739f2c441a7f4c7dfa6d8af8a8cde8e28bdf726510bbfb1ade140a9dc2e326  newresconst.pdf
ae0c0ef2e325f48cd6dc9c4657691edfcc5d4cf96cc1c5013d3aeb099dfb4e95  permits_cust.xlsx
eab29258ada8389b9f469c566eb6eb074cf128aa94c471e89f818a20a4d83afb  st2025a.txt
02c1926ba520e5ab4f7eadf93a10293fe8c9b95f4343ee9285856321fc2b6da4  starts_cust.xlsx
```
