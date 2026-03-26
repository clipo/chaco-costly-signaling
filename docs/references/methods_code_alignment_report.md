# Methods-Code Alignment Report

**Date:** 2026-03-27
**Manuscript:** `docs/manuscript/Chaco_Signaling_Manuscript.md`
**Code files reviewed:**
- `src/chaco/simulation.py` (core simulation engine)
- `src/chaco/environment.py` (PMDI-based environment)
- `src/chaco/spatial.py` (spatial structure)
- `scripts/analysis/bayesian_model_comparison.py` (Bayesian analyses)
- `scripts/analysis/comprehensive_tree_ring_analysis.py` (tree-ring tests)
- `scripts/analysis/pmdi_period_analysis.py` (period-level PMDI analysis)

---

## Code Infrastructure Summary

The codebase implements a three-layer costly signaling model:

1. **Simulation engine** (`simulation.py`, 647 lines): Agent-based model with quality-dependent investment via the Spence condition, intergroup assessment noise, exponential survival with network buffering, and lambda-sigma feedback. Groups have continuous quality derived from room counts. Annual time step with depreciation, conflict, pilgrimage, and network dynamics.

2. **Environment** (`environment.py`, 391 lines): Loads PMDI data from `data/processed/chaco_pmdi_simulation_input.csv` (1,001 years, 500-1500 CE). Converts PMDI to productivity. Computes drought events and sigma.

3. **Spatial** (`spatial.py`, 264 lines): Defines 5 core great houses (Pueblo Bonito, Chetro Ketl, Pueblo del Arroyo, Pueblo Alto, Kin Kletso) and 30 procedurally generated outliers. Quality derived from room counts via sqrt scaling.

4. **Analysis scripts**: Three scripts performing empirical tests against the 5,419-record Chaco Research Archive tree-ring database and PMDI data. Bayesian analyses use PyMC 5 with ArviZ.

---

## Notation Mapping (Confirmed)

| Manuscript notation | Code variable/parameter | Location |
|---|---|---|
| $q$ (quality) | `group.quality`, derived via `_quality_from_rooms()` | simulation.py L89, L150-164 |
| $q_{\min}$ | `config.q_min` (default 0.1) | simulation.py L50 |
| $x^*(q)$ (Spence investment) | `_spence_investment(q, lam)` return value | simulation.py L230-243 |
| $\lambda$ (signaling return) | `current_lambda`, computed by `_compute_lambda()` | simulation.py L221-228 |
| $\lambda_0$ | `config.lambda_0` (default 0.3) | simulation.py L51 |
| $\lambda_1$ | `config.lambda_1` (default 0.5) | simulation.py L52 |
| $\alpha$ (lambda-sigma exponent) | `config.alpha` (default 1.0) | simulation.py L53 |
| $\sigma$ (env. uncertainty) | `sigma`, computed by `_compute_sigma()` | simulation.py L205-219 |
| $\sigma_0$ (baseline assessment noise) | `config.sigma_0` (default 0.5) | simulation.py L58 |
| $\sigma_{\text{eff}}$ (effective noise) | `_assessment_noise()` return value | simulation.py L245-251 |
| $\kappa$ | `config.kappa` (default 0.001) | simulation.py L59 |
| $M_g, M_h$ (monument stock) | `group.monument_investment` | simulation.py L92 |
| $\delta$ (depreciation rate) | `config.monument_decay_rate` (default 0.02) | simulation.py L54 |
| $S(\sigma, k)$ (survival) | `_survival_probability(sigma, k)` | simulation.py L253-258 |
| $\gamma$ (buffering coefficient) | `config.gamma` (default 0.1) | simulation.py L64 |
| $k$ (exchange partners) | `group.exchange_partners` | simulation.py L96 |
| $c(x, q) = x^2/(2q)$ (cost function) | Inline in `_process_signaling_investment()` L341 | simulation.py L341 |

---

## Methods Discrepancies

### Critical Issues (Checks 1-3)

#### C1. Lambda-sigma specification: manuscript vs. code vs. Data Availability

The manuscript presents the lambda-sigma feedback in three different forms:

- **Section 2.4 (line 146):** $\lambda(\sigma) = \lambda_0 + \lambda_1 \cdot \sigma$ (linear)
- **Appendix A.5 (line 711-713):** General family $\lambda(\sigma) = \lambda_0 + \lambda_1 \cdot \sigma^{\alpha}$ with $\alpha \in (0, 2]$, noting the main text uses the linear case
- **Data Availability (line 457):** $\lambda(\sigma) = \lambda_0 + \lambda_1 \sigma^{\alpha}$
- **Code (simulation.py line 228):** `lambda_0 + lambda_1 * (sigma ** alpha)` with `alpha` defaulting to 1.0

**Status: Consistent.** The code implements the general form with alpha=1.0 as default, which reduces to the linear specification in Section 2.4. The docstring on simulation.py line 7 correctly notes the general form. No mismatch, but the manuscript should acknowledge that the simulation uses the generalized form and that the default alpha=1.0 recovers the linear case.

#### C2. Sigma computation: manuscript vs. simulation vs. analysis scripts

Three different definitions of sigma exist:

- **Manuscript (Section 2.4):** Sigma is described conceptually as "environmental uncertainty" without specifying the exact computation for the empirical tests.
- **Simulation (`simulation.py` lines 205-219):** `_compute_sigma()` computes the rolling standard deviation of PMDI over a 30-year window, using `np.std()` on the cached PMDI history.
- **Analysis scripts (`comprehensive_tree_ring_analysis.py` lines 103-106):** Rolling variance (`rolling().var()`) and rolling mean computed with 20-year and 30-year windows with `center=True`.
- **Period analysis (`pmdi_period_analysis.py` lines 47-49):** Period-level `pmdi.std()` and `pmdi.var()` for archaeological phases.
- **Environment (`environment.py` lines 261-306):** `calculate_sigma()` uses a complex formula: `(avg_magnitude * avg_duration) / frequency_interval`, not a rolling standard deviation.

**Status: Inconsistent.** The simulation's sigma (rolling SD of PMDI) differs from the environment module's sigma (composite drought metric). The analysis scripts use variance and mean in rolling windows, which is yet a third operationalization. The manuscript does not specify which sigma operationalization applies to which test, creating ambiguity about what "environmental uncertainty" means in each context.

#### C3. Quality assignment circularity

The manuscript acknowledges this issue (Section 6.7, line 432; Data Availability, line 457). Quality q is derived from room counts via `_quality_from_rooms()` (simulation.py lines 150-164), using `q = q_min + c * sqrt(rooms)` calibrated so 350 rooms maps to q = 2.0. Room counts are themselves a component of monument investment. The Bayesian quality-investment test (bayesian_model_comparison.py lines 251-297) regresses log(timbers) on log(rooms), which tests a different relationship (timber specimens vs. rooms) but both are signaling outputs. The manuscript correctly flags this as a circularity issue.

**Status: Acknowledged but unresolved.** No independent quality proxy is implemented in the code.

#### C4. Specimen count discrepancy: 2,899 vs. 2,973

The manuscript reports two different specimen counts:
- **Section 5.5 (line 308):** "2,899 dated timber specimens ... spanning 25 sites ... with outer ring dates between 828 and 1200 CE"
- **Section 6.2 (line 376):** "2,973 specimens, 24 sites"

Verification from the data:
- 5,419 total records in the CSV
- 3,342 records with valid numeric outside_date
- **2,973 records** with year in range 800-1200 (also equals 828-1200), from **24** unique site_clean values
- 2,922 records with year in range 850-1150
- 2,921 records from the 13 mapped sites only (828-1200)

The number 2,973 from 24 sites is reproducible from the code. The number 2,899 from 25 sites cannot be reproduced from any filtering combination attempted. The per-site counts in the manuscript (Pueblo Bonito 556, Chetro Ketl 593, Pueblo del Arroyo 506, Aztec Ruins 920) do not match the code output (639, 621, 443, 939 for 828-1200 range).

**Status: Discrepancy.** The manuscript's 2,899 count and per-site breakdowns appear to derive from a different filtering or earlier version of the data. Neither analysis script produces these exact numbers. The 2,973 count in Section 6.2 matches the code. The inconsistency between the two manuscript sections and between the manuscript and the reproducible code output must be resolved.

#### C5. Bayesian changepoint model uses DiscreteUniform for tau

The changepoint detection (bayesian_model_comparison.py line 209) uses `pm.DiscreteUniform('tau', lower=1020, upper=1140)`, a discrete parameter. PyMC's default NUTS sampler does not handle discrete parameters; PyMC 5 uses compound step methods (Metropolis for discrete, NUTS for continuous). The manuscript does not note this, and the code does not explicitly configure the sampler, relying on PyMC's automatic assignment.

**Status: Not documented.** The use of Metropolis sampling for the discrete changepoint parameter should be noted because it affects mixing and convergence properties differently than NUTS.

#### C6. Conflict resolution: code adds mechanisms not in manuscript

The conflict resolution in `_resolve_conflict()` (simulation.py lines 464-505) includes:
- Strength modified by monument investment: `strength = population * (1 + monument_investment / 500)` (line 474)
- Territory transfers for decisive victories (lines 498-505): Winner takes 1/4 of loser's territory cells when strength ratio exceeds 1.5x

The manuscript's Layer 2 description (Section 2.3) describes only the assessment noise function reducing conflict probability. It does not mention monument-modified combat strength or territory transfers. These are simulation-specific mechanisms with no formal derivation in the manuscript.

**Status: Code extends beyond manuscript specification.** The conflict probability mechanism matches the manuscript, but the outcome mechanics (strength weighting, territory transfer) are undocumented additions.

#### C7. Network partner dynamics: code adds decay not in manuscript

The `_update_exchange_networks()` method (simulation.py lines 507-522) includes a partner decay rate of 5% per year (`partner_decay = 0.05 * group.exchange_partners`, line 518). The manuscript discusses network formation (Layer 3, Section 2.4) but does not specify a partner decay rate. The manuscript's depreciation equation (Section 2.5, $M_g(t+1) = (1-\delta) M_g(t) + I_g(t)$) applies only to monument stock, not to exchange partners.

**Status: Undocumented code mechanism.** Partner decay is a plausible dynamic but has no manuscript derivation.

### Warnings (Checks 4-6)

#### W1. Rounding in manuscript correlation values

Manuscript reports (Section 5.5, line 308):
- "r = -0.17, p = 0.004" for 10-year variance vs. construction
- "r = -0.15, p = 0.012" for 20-year variance vs. construction
- "r = +0.38, p < 0.0001" for 20-year mean vs. construction
- "r = +0.43, p < 0.0001" for 30-year mean vs. construction

Code reproduces:
- r = -0.1643, p = 0.0043 (rounds to r = -0.16, not -0.17)
- r = -0.1460, p = 0.0112 (rounds to r = -0.15, correct)
- r = +0.3861, p < 0.0001 (rounds to r = +0.39, not +0.38)
- r = +0.4316, p < 0.0001 (rounds to r = +0.43, correct)

**Status: Minor rounding discrepancies.** The first correlation (-0.1643) rounds to -0.16 by standard rules, not the -0.17 reported. The third correlation (+0.3861) rounds to +0.39, not +0.38. These are single-digit rounding issues and do not affect conclusions, but should be corrected for rigor.

#### W2. Levene's test values confirmed

Manuscript (Section 5.5, line 300): "F = 0.21, p = 0.64"
Code reproduces: F = 0.2143, p = 0.6438

**Status: Match.** Rounded correctly.

#### W3. Bayesian beta and changepoint values

Manuscript claims:
- "Bayesian change-point ... AD 1082" (Section 6.2, line 376)
- "beta = 1.67 (94% HDI: 0.84-2.45, P(beta > 0) = 0.9998)" (Section 5.1, line 254)

Saved results (`bayesian_results.csv`):
- changepoint_mean = 1082.008 (rounds to 1082, correct)
- beta_qi_mean = 1.672 (rounds to 1.67, correct)
- beta_qi_prob_positive = 0.99975 (manuscript says 0.9998, which is a rounding up from 0.99975)

**Status: Match within rounding.** The P(beta>0) = 0.9998 rounds up from 0.99975. This is a minor inflation (0.99975 rounds to 0.9998 or 0.9997 depending on convention). The difference is immaterial to the conclusion.

#### W4. Construction counts confirmed

Manuscript (Section 6.2, line 376): "Chaco Canyon construction dropping from 223 specimens in the 1080s to 63 in the 1090s"

Code output: Chaco 1080s = 223, Chaco 1090s = 63.

**Status: Exact match.**

Manuscript: "Aztec Ruins surges from 15 specimens in the 1090s to 771 in the 1110s"

Code output: Aztec 1090s = 15, Aztec 1110s = 771.

**Status: Exact match.**

#### W5. Post-1160 Chaco timbers

Manuscript (Section 6.2, line 376): "only 2 Chaco timber specimens date to the post-1160 period"
Code output: 2 Chaco specimens with year in 1161-1200 (both Kin Kletso, years 1171 and 1178).

**Status: Exact match.** Note: filtering must exclude dates > 1200 (which includes modern excavation-era dates from 1878-1935) to get this count.

#### W6. Spearman rho for quality-investment

Manuscript (Figure 15 legend, line 633): "Spearman rho = 0.87 (p < 0.001)"
Code output: rho = 0.8717, p = 0.000103

**Status: Match.** Rounded correctly. Note that the 13 sites used include Aztec Ruins, which is excluded from other Chaco-specific analyses but included in the quality-investment test.

---

## Results Discrepancies

| Manuscript claim | Code result | Status |
|---|---|---|
| Spearman rho = 0.87 | rho = 0.8717 | Match |
| 10-yr PMDI var r = -0.17 | r = -0.1643 | Minor: rounds to -0.16 |
| 20-yr PMDI var r = -0.15 | r = -0.1460 | Match |
| 20-yr PMDI mean r = +0.38 | r = +0.3861 | Minor: rounds to +0.39 |
| 30-yr PMDI mean r = +0.43 | r = +0.4316 | Match |
| Changepoint AD 1082 | 1082.008 | Match |
| beta = 1.67 | 1.672 | Match |
| P(beta>0) = 0.9998 | 0.99975 | Minor: rounds to 0.9998 or 0.9997 |
| Levene's F = 0.21, p = 0.64 | F = 0.2143, p = 0.6438 | Match |
| 1080s Chaco = 223 | 223 | Match |
| 1090s Chaco = 63 | 63 | Match |
| 1090s Aztec = 15 | 15 | Match |
| 1110s Aztec = 771 | 771 | Match |
| 2 Chaco timbers post-1160 | 2 | Match |
| 2,899 specimens, 25 sites | 2,973 specimens, 24 sites | **Discrepancy** |
| PB=556, CK=593, PdA=506, AR=920 | PB=639, CK=621, PdA=443, AR=939 | **Discrepancy** |

---

## Unverifiable Claims

1. **"n = 301 years" (Section 5.5, line 308).** The manuscript attaches n=301 to the rolling-window correlation results. The merged DataFrame has 301 rows (years 850-1150), but rolling-window computations drop edge values, so the effective n for each correlation is less than 301. For the 10-year centered window with min_periods=5, the effective n is indeed 301 (all rows have at least 5 values). For 20-year and 30-year windows, the effective n is also 301 due to min_periods = w//2. So this is correct, though potentially misleading since it implies 301 independent observations when temporal autocorrelation reduces effective sample size.

2. **Bayesian model comparison LOO weights (Figure 16a legend, line 635).** The manuscript says "All models are effectively equivalent at decadal resolution (elpd differences < 1)." The saved results show the signaling (PMDI var) model had LOO weight of 1.0, which contradicts "effectively equivalent." This discrepancy suggests the saved CSV may reflect a different run than the one described in the figure caption. The LOO comparison results are printed at runtime and not fully saved; only the best model and its weight are recorded.

3. **HDI bounds for beta (94% HDI: 0.84-2.45).** The code uses ArviZ default HDI (94%), and the summary function is called (line 290), but the HDI values are printed to stdout, not saved. The values in the manuscript cannot be verified from saved outputs. They are plausible given beta_mean = 1.67 and the distribution shape but require re-running the Bayesian analysis to confirm.

4. **Changepoint rate estimates (16.0 timbers/yr before, 7.4 after).** These values are printed by the changepoint analysis (lines 237-240) but not saved to the CSV. They cannot be verified from saved outputs.

---

## Diagnostic Reporting Gaps (Check 5)

### Bayesian convergence diagnostics

1. **Rhat and ESS are not reported in the manuscript.** The ArviZ `summary()` function (called on lines 175-179, 290) computes Rhat and ESS by default, but the code extracts only `['mean', 'sd', 'hdi_3%', 'hdi_97%']` columns. Rhat and ESS values are computed but discarded before printing. The manuscript does not mention convergence diagnostics for any of the four Bayesian models.

2. **Number of chains, tune, and draw iterations.**
   - LOO models (lines 132-157): 2,000 draws, 1,000 tune, 1 chain (cores=1), seed=42
   - Changepoint model (line 222): 4,000 draws, 2,000 tune, 1 chain, seed=42
   - Quality-investment model (line 280): 2,000 draws, 1,000 tune, 1 chain, seed=42

   The manuscript does not document these settings. Using a single chain prevents Rhat computation across chains; within-chain Rhat may be computed by ArviZ but is less diagnostic. Single-chain sampling is methodologically concerning for publication-quality Bayesian analysis; multiple chains are standard practice for verifying convergence.

3. **Discrete parameter sampling.** The changepoint model uses `pm.DiscreteUniform('tau')`, which PyMC 5 handles via Metropolis sampling while using NUTS for continuous parameters. This compound sampler is not documented in the manuscript. Metropolis sampling for discrete parameters can have poor mixing properties that NUTS diagnostics do not detect.

4. **LOO-CV warnings.** ArviZ's `loo()` function may produce Pareto k diagnostics indicating unreliable LOO estimates for observations with high leverage. With only 31 data points (decades 850-1150 in 10-year bins), individual decades can have high influence. The code does not check or report Pareto k values.

---

## Code Without Documentation

The following simulation mechanisms appear in the code but have no corresponding manuscript description:

1. **Quality from rooms (`_quality_from_rooms`, simulation.py L150-164):** `q = q_min + c * sqrt(rooms)` with c calibrated so 350 rooms yields q = 2.0. The manuscript describes quality conceptually but does not specify this particular functional form or calibration.

2. **Resource production (simulation.py L296-298):** `resources = territory_cells * productivity * 100`. The productivity-to-resources conversion is not described in the manuscript.

3. **Resource constraint on investment (simulation.py L345):** `actual_cost = min(resource_cost_scaled, resources * 0.5)`. Investment is capped at 50% of available resources. This constraint is not in the manuscript's formal model.

4. **Birth rate quality dependence (simulation.py L391-396):** Birth rate modifier ranges 1.1 to 0.7 based on normalized quality, implementing K-selection. Not in manuscript.

5. **Elite exotic goods mortality (simulation.py L355-363):** Elite agents die during exotic acquisition at rate `elite_population * acquisition_cost * exotic_investment_rate`. Not in manuscript.

6. **Pilgrimage dynamics (simulation.py L524-545):** Seasonal labor influx proportional to monument stock, with pilgrims contributing to monument investment. The manuscript mentions pilgrimage models but does not formalize this mechanism.

7. **Initial monument stock (simulation.py L177, L191):** Core houses start with `rooms * 5.0` monument stock; outliers start with `rooms * 2.0`. Not in manuscript.

8. **Partner initialization (simulation.py L180, L198):** Initial partners scale with quality: core `max(1.0, q * 3.0)`, outlier `max(0.5, q * 1.5)`. Not in manuscript.

9. **Elite population cap (simulation.py L423):** Elites capped at 10% of total population. Not in manuscript.

---

## Equation-Code Correspondence (Check 6)

### Equation 1: Cost function $c(x, q) = x^2 / (2q)$

**Manuscript (Section 2.2, line 98):** $c(x_i, q_i) = \frac{x_i^2}{2q_i}$

**Code (simulation.py line 341):** `resource_cost = (optimal_x ** 2) / (2.0 * group.quality) if group.quality > 0 else 0`

**Status: Exact match.** Guard clause for q=0 is a reasonable numerical safety measure not needed in the formal model.

### Equation 2: Spence equilibrium $x^*(q) = \sqrt{\lambda(q^2 - q_{\min}^2)}$

**Manuscript (Section 2.2, line 104):** $x^*(q) = \sqrt{\lambda \cdot (q^2 - q_{\min}^2)}$

**Code (simulation.py lines 237-243):**
```python
val = lam * (q ** 2 - q_min ** 2)
if val <= 0:
    return 0.0
return math.sqrt(val)
```

**Status: Exact match.** Guard clause for val <= 0 handles numerical edge cases.

### Equation 3: Assessment noise $\sigma_{\text{eff}} = \sigma_0 / \sqrt{1 + \kappa(M_g + M_h)}$

**Manuscript (Section 2.3, line 124):** $\sigma_{\text{eff}} = \frac{\sigma_0}{\sqrt{1 + \kappa(M_g + M_h)}}$

**Code (simulation.py lines 249-251):** `sigma_0 / math.sqrt(1.0 + kappa * (m_g + m_h))`

**Status: Exact match.**

### Equation 4: Survival function $S(\sigma, k) = \exp(-\sigma / (1 + \gamma k))$

**Manuscript (Section 2.4, line 138):** $S(\sigma, k) = \exp\left(-\frac{\sigma}{1 + \gamma k}\right)$

**Code (simulation.py lines 256-258):**
```python
denominator = 1.0 + self.config.gamma * k
return math.exp(-sigma / denominator)
```

**Status: Exact match.**

### Equation 5: Lambda-sigma feedback $\lambda(\sigma) = \lambda_0 + \lambda_1 \cdot \sigma^{\alpha}$

**Manuscript (Section 2.4, line 146):** $\lambda(\sigma) = \lambda_0 + \lambda_1 \cdot \sigma$ (linear)
**Manuscript (Appendix A.5, line 711):** General family $\lambda_0 + \lambda_1 \cdot \sigma^{\alpha}$

**Code (simulation.py line 228):** `lambda_0 + lambda_1 * (sigma ** alpha)` with `alpha` default 1.0

**Status: Exact match.** Code implements the general form; default alpha=1.0 recovers the linear case in Section 2.4.

### Equation 6: Depreciation $M_g(t+1) = (1 - \delta) M_g(t) + I_g(t)$

**Manuscript (Section 2.5, line 162):** $M_g(t+1) = (1 - \delta) \cdot M_g(t) + I_g(t)$

**Code (simulation.py lines 318-319):** `group.monument_investment *= (1 - self.config.monument_decay_rate)` applied after new investment is added (line 352).

**Status: Match with ordering note.** The code applies depreciation after adding new investment within the same time step (step 9 in the annual cycle, line 318-319, after investment in step 4). This means the sequence is: $M_g(t+1) = (1 - \delta) \cdot (M_g(t) + I_g(t))$, which differs slightly from the manuscript equation where new investment is not depreciated in the period it is added: $M_g(t+1) = (1 - \delta) M_g(t) + I_g(t)$. The difference is a factor of $(1-\delta)$ applied to $I_g(t)$; with $\delta = 0.02$, this means new investment loses 2% immediately, a minor but systematic deviation from the formal specification.

### Conflict probability derivation

**Manuscript (Section 2.3, line 126):** Conflict probability decreases as assessment noise decreases (qualitative description).

**Code (simulation.py lines 456-459):**
```python
noise_ratio = noise / self.config.sigma_0  # 0 to 1
conflict_prob = self.config.base_conflict_rate * noise_ratio
```

**Status: Consistent with manuscript's qualitative description.** The specific linear scaling of conflict probability with noise ratio is a code-level implementation detail not formally derived in the manuscript.

---

## Summary Statistics

| Category | Count |
|---|---|
| **Critical issues** | 7 |
| C1. Lambda-sigma form consistency | Consistent (after checking defaults) |
| C2. Sigma computation inconsistency across modules | Inconsistent (3 different definitions) |
| C3. Quality circularity | Acknowledged, unresolved |
| C4. Specimen count discrepancy (2,899 vs. 2,973) | **Needs correction** |
| C5. Discrete parameter sampling undocumented | Needs documentation |
| C6. Conflict outcome mechanics beyond manuscript | Needs documentation or removal |
| C7. Network partner decay undocumented | Needs documentation |
| **Warnings** | 6 |
| W1. Rounding discrepancies in two correlations | Minor correction needed |
| W2. Levene's test values | Confirmed |
| W3. Bayesian beta/changepoint | Confirmed |
| W4. Construction counts | Confirmed |
| W5. Post-1160 timbers | Confirmed |
| W6. Spearman rho | Confirmed |
| **Diagnostic gaps** | 4 |
| Rhat/ESS not reported | Needs addition |
| Chain/tune/draw not documented | Needs addition |
| Single chain for all models | Methodological concern |
| LOO Pareto k not checked | Needs addition |
| **Equation-code matches** | 6/6 exact (1 with ordering caveat) |
| **Code without documentation** | 9 mechanisms |
| **Results discrepancies** | 2 minor rounding, 1 specimen count |
| **Unverifiable claims** | 4 (values printed to stdout, not saved) |

### Priority actions

1. **Resolve the 2,899 vs. 2,973 specimen count and per-site breakdowns.** Determine which filtering produces each number, correct the manuscript to use one consistent count, and verify per-site figures.
2. **Add Bayesian convergence diagnostics** (Rhat, ESS, chain count) to the manuscript or supplementary materials. Consider re-running with multiple chains.
3. **Correct the two rounding errors** in PMDI correlations (r = -0.16, not -0.17; r = +0.39, not +0.38).
4. **Document the depreciation timing** difference (code depreciates new investment immediately; manuscript equation does not).
5. **Document or justify the 9 code mechanisms** that extend beyond the manuscript's formal model (conflict outcomes, partner decay, resource constraints, etc.), or note them as simulation-specific implementation details.
6. **Reconcile the LOO model comparison** narrative ("effectively equivalent") with the saved result (signaling model weight = 1.0).
