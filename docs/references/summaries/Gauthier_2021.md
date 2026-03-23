# Summary: Gauthier 2021

**Full citation**: Gauthier, N. 2021. Hydroclimate Variability Influenced Social Interaction in the Prehistoric American Southwest. *Frontiers in Earth Science* 8:620856. DOI: 10.3389/feart.2020.620856
**PDF filename**: Gauthier_2021.pdf
**Date summarized**: 2026-03-23
**Pipeline status**: index

---

## Relevance to Argument

This paper provides direct empirical evidence for the model's Layer 3 prediction: that exchange networks form to buffer against spatially correlated environmental shocks. By demonstrating that climate regime differences structure social interaction beyond what distance alone predicts, Gauthier 2021 establishes the environmental logic for why inter-regional cooperation networks are valuable and why signaling to attract exchange partners from different climate zones would provide crisis-buffering benefits.

## Key Claims

| Claim | Page | Type | Strength | Notes |
|-------|------|------|----------|-------|
| Climate regime differences increase social interaction beyond distance effects | p. 1 | empirical | strong | Core finding; EOF model explains 42.5% vs. 37.8% for distance-only |
| Distance-only null model explains 37.8% of ceramic similarity variance | p. 5 | empirical | strong | Baseline for climate contribution |
| Six EOF drought patterns explain 83% of observed variability; robust across centuries | p. 5 | empirical | strong | PCA of 122-year SPEI record |
| Distance deterrence function predicts interaction falloff at >100 hours travel | p. 5 | empirical | strong | Sets outer limit for regular interaction |
| Climate-structured ties most important at/after AD 1300 | p. 6 | empirical | moderate | Only five time steps; suggestive |
| Tropical Pacific and Atlantic EOFs most important for structuring interaction | p. 8 | interpretive | moderate | ENSO-related moisture sources |
| Social adaptations to one climate mode are fragile when that mode changes | p. 8 | interpretive | moderate | Consistent with model collapse predictions |
| Free-riders can damage social network infrastructure | p. 8 | interpretive | weak | Identifies problem signaling theory addresses |
| Jensen-Shannon divergence measures information flow between sites | p. 2-3 | methodological | strong | 15 decorated ware types from SWSN v1.0 |
| Model residuals show triad closure beyond chance levels | p. 8 | empirical | moderate | Consistent with signaling-based partner selection |

## Data Presented

- **Dataset**: SWSN v1.0, aggregated to 10 km grid cells; ~500 sites; 4.3 million ceramics; 5 time periods (1200-1450 CE)
- **Figure 1**: Site locations and ceramic similarity networks across five periods
- **Figure 2**: Time series of six leading PCs from SPEI varimax rotation
- **Figure 3**: Six EOF spatial patterns (correlation maps)
- **Figure 4**: Distance deterrence function (nonlinear falloff; key thresholds at 10 and 100 hours)
- **Figure 5**: Smooth functions of social interaction vs. climatic difference for each EOF and time period
- **Key metric**: R-squared increase from 37.8% (distance-only) to 42.5% (distance + climate)

## Methodological Notes

- Uses SPEI (Standardized Precipitation-Evapotranspiration Index) rather than PDSI, capturing both precipitation and evaporative demand. The 12-month August SPEI captures the water balance over the growing season.
- Employs generalized additive models (GAMs) with penalized cubic regression splines, estimated by restricted maximum likelihood. This is a more flexible approach than traditional gravity models.
- Least-cost distances computed from 90 m SRTM DEM using modified Tobler hiking function (isotropic, with penalty for very steep slopes).
- The 75% ceramic similarity threshold for network construction follows Mills et al. 2013, with continuous similarity scores used for GAM fitting.

## Connections to Other Sources

- **Depends on**: Mills et al. 2013 (SWSN database); Cook et al. 2004 (drought atlas); Abatzoglou et al. 2017 (SPEI data)
- **Corroborates**: Rautman 1993 (social networks as risk management); Freeman et al. 2014 (crop specialization and exchange robustness); Cordell et al. 2007 (drought and relocation)
- **Extends**: Mills et al. 2013 by adding climate as a predictor of network structure
- **Conflicts with**: None directly, but challenges assumptions that distance alone structures interaction

## Verification Notes

- Page numbers refer to Frontiers in Earth Science published pagination (pp. 1-11).
- The paper is open access and the full text was read directly from the PDF.
