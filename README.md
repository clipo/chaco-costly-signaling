# Formalizing Costly Signaling at Chaco Canyon

A three-layer formal signaling model applied to Chaco Canyon (850-1150 CE), with agent-based simulation, Bayesian analysis, and annual-resolution tree-ring tests.

**Authors:** Carl P. Lipo and Robert J. DiNapoli, Binghamton University

## Overview

This project develops and tests a formal costly signaling framework for monumental architecture and exotic goods acquisition at Chaco Canyon. The model operates at three nested scales:

- **Layer 1 (Spence equilibrium):** Individual signaling through condition-dependent investment. Higher-capacity lineages invest more in monument construction because the marginal cost is lower for them, producing an honest signal of productive capacity.
- **Layer 2 (Intergroup assessment):** Monument stock reduces conflict probability through mutual deterrence. Groups with large, visible great houses can assess each other's capacity, reducing costly conflicts.
- **Layer 3 (Cooperation networks):** Signaling builds exchange networks that buffer against environmental uncertainty. The lambda-sigma feedback links environmental conditions to signaling returns.

The model derives eight testable predictions, evaluated against independent archaeological, paleoclimatic, and bioarchaeological evidence. The annual-resolution tree-ring analysis (2,973 specimens, 24 sites) provides quantitative tests including Bayesian model comparison.

## Key Results

- **P5 (lambda-sigma feedback) is falsified:** PMDI variance correlates negatively with construction (r = -0.167); mean PMDI correlates positively (r = +0.43). Construction tracks moisture, not variance.
- **Bayesian changepoint at AD 1082** confirms pre-drought signal degradation (P(before 1130 megadrought) = 1.0), with construction rate dropping from 16.0 to 7.4 timbers/year.
- **Quality-investment gradient confirmed:** Bayesian beta = 1.67 (94% HDI: 0.84-2.45, P(beta > 0) = 0.9998), superlinear scaling across 13 sites.
- **Collapse-sequence evidence** (pre-drought decline, post-collapse non-recovery, Aztec competitive displacement) is consistent with signaling logic but also accommodated by depletion-augmented surplus models.
- The model's primary contribution is **formalization itself**: transforming verbal CST insights into a framework with falsifiable predictions. That P5 was specific enough to fail demonstrates the value of formalization over narrative approaches.

## Project Structure

```
chaco-signaling/
├── src/chaco/                  # Python package
│   ├── simulation.py           # Three-layer ABM (Spence, assessment, networks)
│   ├── environment.py          # PMDI paleoclimate data and sigma computation
│   ├── spatial.py              # Great house spatial structure
│   └── analysis.py             # Summary statistics and comparison tools
├── data/
│   ├── raw/
│   │   ├── construction_dates/ # Chaco Research Archive tree-ring database (5,419 records)
│   │   └── pdsi_reconstructions/ # LBDA v2 PMDI data (Gille et al. 2017)
│   └── processed/              # Derived datasets, correlation results, Bayesian outputs
├── docs/
│   ├── manuscript/             # Manuscript (.md and .docx)
│   ├── references/             # INDEX, claims files, summaries, audit reports
│   ├── evidence/               # Evidence compilations by topic
│   └── peer_review_report.md   # Simulated peer review (4 rounds)
├── scripts/
│   ├── analysis/               # Bayesian model comparison, tree-ring correlation,
│   │                           #   comprehensive analysis, PMDI period analysis
│   ├── data_processing/        # PMDI dataset creation and processing
│   ├── figure_generation/      # Legacy figure scripts
│   └── run_formal_simulation.py # Main simulation runner (20 replicates)
├── figures/
│   └── final/                  # 16 publication-ready figures (300 dpi PNG)
└── CLAUDE.md                   # Project conventions and archaeological parameters
```

## Simulation

The simulation implements the manuscript's equations directly:

```python
# Layer 1: Spence equilibrium
x_star = sqrt(lambda * (q**2 - q_min**2))

# Layer 2: Assessment noise
sigma_eff = sigma_0 / sqrt(1 + kappa * (M_g + M_h))

# Layer 3: Survival function + lambda-sigma feedback
S = exp(-sigma / (1 + gamma * k))
lambda_sigma = lambda_0 + lambda_1 * sigma**alpha
```

Groups have continuous quality derived from room counts. Environmental uncertainty (sigma) is computed from rolling PMDI standard deviation. The simulation runs from AD 800-1200 using real PMDI data from the Living Blended Drought Atlas.

## Data Sources

| Source | Description | Reference |
|--------|------------|-----------|
| Chaco Research Archive | 5,419 tree-ring dated specimens, 60+ sites | chacoarchive.org |
| Living Blended Drought Atlas v2 | Annual PMDI, 500-2017 CE | Gille et al. 2017 |
| Guiterman et al. 2015 | Timber provenance (170 sourced specimens) | PNAS 112(44) |
| Mills et al. 2013, 2018 | Ceramic similarity networks (4.3M sherds) | PNAS 110(15); Antiquity 92(364) |
| Kennett et al. 2017 | Pueblo Bonito archaeogenomics | Nature Communications 8:14115 |
| Polyak et al. 2022 | Fort Stanton Cave speleothem (3,400 yr) | Scientific Reports 12:2684 |

## Figures

| # | Content |
|---|---------|
| 1 | PMDI time series with construction overlay |
| 2 | Three-layer model schematic |
| 3 | Spence equilibrium sensitivity (lambda 0.2-1.2) |
| 4 | Great house visibility distributions |
| 5 | Network-construction co-evolution |
| 6 | Environmental uncertainty decomposition (4 panels) |
| 7 | Prediction evaluation summary with discriminability tags |
| 8 | Simulation dynamics (20 replicates, 90% CI) |
| 9 | Regional map |
| 10 | Construction chronology |
| 11 | Model comparison table |
| 12 | PMDI variance-construction by period |
| 13 | Simulation quality-investment scatter |
| 14 | Annual-resolution PMDI-construction correlation (2,973 specimens) |
| 15 | Comprehensive tree-ring analysis (5 panels) |
| 16 | Bayesian analysis (LOO, changepoint, quality-investment) |

## Requirements

- Python 3.10+
- PyMC 5, ArviZ, NumPy, SciPy, Pandas, Matplotlib

## Key References

1. Guiterman, C.H., et al. 2015. Eleventh-century shift in timber procurement areas for the great houses of Chaco Canyon. *PNAS* 112(44):13438-13443.
2. Kantner, J., & Vaughn, K.J. 2012. Costly signaling in the archaeological record. In *The Oxford Handbook of the Archaeology of Ritual and Religion*, pp. 67-86.
3. Safi, K.N. 2015. Costly signaling and the role of Chacoan great houses in the southern Cibola region. PhD dissertation, Washington State University.
4. Quinn, C.P. 2019. The antiquity of costly signaling. *Journal of Archaeological Method and Theory* 26:1-30.
5. Perreault, C. 2019. *The Quality of the Archaeological Record*. University of Chicago Press.
6. Lakatos, I. 1970. Falsification and the methodology of scientific research programmes. In *Criticism and the Growth of Knowledge*, pp. 91-196.

## License

[To be determined]
