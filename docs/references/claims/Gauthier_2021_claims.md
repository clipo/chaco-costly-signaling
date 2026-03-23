# Claims Extraction: Gauthier 2021

**Full citation**: Gauthier, N. 2021. Hydroclimate Variability Influenced Social Interaction in the Prehistoric American Southwest. *Frontiers in Earth Science* 8:620856. DOI: 10.3389/feart.2020.620856
**PDF filename**: Gauthier_2021.pdf
**PDF version**: published (Frontiers open access)
**Date extracted**: 2026-03-23
**Extractor**: Claude Code

---

## Claims

### Claim 1

**Statement**: Social interaction, measured by ceramic similarity, decayed nonlinearly with distance, but ties between sites in differing oceanic and continental climate regimes were often stronger than expected by distance alone.
**Page**: p. 1 (abstract)
**Type**: empirical
**Evidence cited by author**: Analysis of 4.3 million ceramic artifacts from nearly 500 archaeological sites in the SWSN database (Mills et al. 2013a)
**Depends on**: Jensen-Shannon divergence measure of ceramic similarity; least-cost distance network
**Notes**: Core finding. Sites sharing the same drought regime interact more than distance alone predicts.

**Evidence strength**: Strong
**Assessment**: The finding is well-supported by a large dataset and rigorous spatial interaction modeling. Directly relevant to the model's Layer 3: if climate regime shapes network ties, then signaling to attract exchange partners from different climate zones would provide crisis-buffering benefits.

---

### Claim 2

**Statement**: A distance-only null model explained 37.8% of the variance in ceramic similarity data, while a model adding climatic dissimilarity (EOF loadings) explained 42.5%, a moderate but statistically significant improvement.
**Page**: pp. 5-6
**Type**: empirical
**Evidence cited by author**: Generalized additive model (GAM) comparison; AIC, BIC, and R-squared metrics
**Depends on**: Spatial interaction model with penalized cubic regression splines; maximum likelihood estimation
**Notes**: The 4.7 percentage point improvement (37.8% to 42.5%) is modest in absolute terms but consistent across model selection criteria. The improvement is most pronounced at and after AD 1300.

**Evidence strength**: Strong
**Assessment**: The statistical methodology is sound (GAM with penalized splines, REML estimation). The modest improvement is honestly reported and suggests climate is one of several factors structuring interaction.

---

### Claim 3

**Statement**: Six spatial drought patterns (empirical orthogonal functions, EOFs) explain 83% of observed drought variability in the American Southwest, and these patterns are robust across observational data and reconstructions spanning the past millennium.
**Page**: p. 5
**Type**: empirical
**Evidence cited by author**: PCA of 122-year gridded SPEI record; varimax rotation; comparison with SPEI reconstruction (Supplementary Figures S5, S12, S13)
**Depends on**: SPEI data from Abatzoglou et al. 2017; PRISM climate grids (Daly et al. 1997, 2008)
**Notes**: The six EOFs represent different moisture transport pathways: EOF1 (tropical Pacific/SW flow), EOF2 (Gulf of Mexico/SE flow), EOF3 (polar continental/northerly flow), EOF4 (Pacific westerly/Sierra Nevada), EOF5 (Great Plains/Rocky Mountain), EOF6 (Colorado Plateau local circulation).

**Evidence strength**: Strong
**Assessment**: The PCA methodology is standard in climate science. The robustness across time periods supports using these patterns for interpreting prehistoric climate variability.

---

### Claim 4

**Statement**: The empirical distance deterrence function predicts a falloff in social interaction at distances of more than 100 hours of walking. The relationship between distance and interaction is nonlinear, with most interaction occurring within 10 hours travel time.
**Page**: p. 5 (Figure 4)
**Type**: empirical
**Evidence cited by author**: Penalized regression spline estimated from all time periods; least-cost path network based on Tobler's hiking function
**Depends on**: SRTM DEM resampled to 250 m; isotropic walking speed calculation
**Notes**: The 100-hour threshold roughly corresponds to 5-7 days of continuous walking, or approximately 200-400 km depending on terrain. This sets an outer limit for regular face-to-face interaction and implies that maintaining ties beyond this distance required substantial investment.

**Evidence strength**: Strong
**Assessment**: The distance deterrence function is well-estimated. The 100-hour threshold is relevant to the model: maintaining ties beyond this distance represents a costly signal of commitment to inter-regional cooperation.

---

### Claim 5

**Statement**: The improvement in explanatory power of the climate-augmented model over the distance-only null is most pronounced at and after AD 1300, during and after the period of regional relocation.
**Page**: p. 6
**Type**: empirical
**Evidence cited by author**: Refitting each model on data from each time step individually (see SI)
**Depends on**: Time-specific model comparisons
**Notes**: The 1200 and 1250 CE time steps show small improvement from climate terms, while 1300 CE and later show larger improvements. This temporal pattern suggests that climate-structured ties became more important during and after the major demographic upheaval of the late 1200s.

**Evidence strength**: Moderate
**Assessment**: The temporal pattern is suggestive but based on only five 50-year time steps. The result is consistent with the hypothesis that drought-driven migration strengthened climate-regime-based network ties.

---

### Claim 6

**Statement**: Tropical Pacific and Atlantic influences (EOFs 1 and 2) seem to have been most important for structuring social interaction, with ties connecting regions of different oceanic influence being stronger than expected by distance alone.
**Page**: p. 8
**Type**: interpretive
**Evidence cited by author**: EOF spatial patterns and their correlations with global sea surface temperatures; comparison of model coefficients across EOFs and time periods (Figure 5)
**Depends on**: Claims 2, 3
**Notes**: EOF1 (tropical Pacific/ENSO-related) and EOF2 (Gulf of Mexico/Atlantic) are the dominant moisture sources. Sites in different EOF zones experience poorly or negatively correlated drought patterns, making them ideal exchange partners for risk buffering.

**Evidence strength**: Moderate
**Assessment**: The interpretation is plausible and directly relevant to the model's Layer 3. If groups in different ENSO-response zones form exchange ties, they gain insurance against locally correlated drought, consistent with the cooperation-network crisis-buffering mechanism.

---

### Claim 7

**Statement**: Social adaptations to one mode of climate variability are fragile to changes in the nature of that variability. Large-scale patterns of hydroclimate variability act as a dynamic selective environment in which societies evolve new norms and institutions for regulating social interaction.
**Page**: p. 8
**Type**: interpretive
**Evidence cited by author**: Janssen et al. 2007 (robustness of social-ecological systems to spatial and temporal variability); general discussion
**Depends on**: Claims 2, 5, 6
**Notes**: This claim frames climate variability as a selective environment, directly analogous to the model's treatment of sigma (environmental uncertainty) as shaping the returns to signaling investment. The fragility claim implies that when climate modes shift, existing network structures may fail, consistent with the model's collapse predictions.

**Evidence strength**: Moderate
**Assessment**: The claim is conceptually sound but not formally tested. The model's lambda(sigma) feedback provides a mechanism for how institutions adapted to one variability regime become maladapted when that regime changes.

---

### Claim 8

**Statement**: Free-riders who avoid the effort of maintaining social networks can damage critical social infrastructure when it is most needed. A simulation approach could better capture these processes.
**Page**: p. 8
**Type**: interpretive
**Evidence cited by author**: Kohler and West 1996
**Depends on**: General discussion of network maintenance costs
**Notes**: This directly invokes the free-rider problem central to costly signaling theory. If maintaining exchange ties requires costly investment (consistent with Layer 3), then signaling provides a mechanism for honest commitment that reduces free-riding.

**Evidence strength**: Weak (assertion without specific empirical support in this paper)
**Assessment**: The point is theoretically important for the model. Gauthier identifies the free-rider problem but does not propose costly signaling as a solution. The mls-monuments model fills this gap.

---

### Claim 9

**Statement**: The data were aggregated into 10 km grid cells to reduce sensitivity to local settlement dispersal or aggregation. This choice reflects a day's round-trip travel, bounding the area for farming and raw material collection around a site.
**Page**: p. 2
**Type**: methodological
**Evidence cited by author**: Paliou and Bevan 2016; Varien 1999; Hill et al. 2015
**Depends on**: None (methodological choice)
**Notes**: The 10 km grid cell size is a reasonable approximation for a foraging/farming catchment. The aggregation reduces noise from site-level sampling variation.

**Evidence strength**: Strong (well-justified methodological choice)
**Assessment**: Standard approach in regional archaeological network analysis.

---

### Claim 10

**Statement**: Cultural similarity, measured by Jensen-Shannon divergence of decorated ceramic ware distributions, serves as an inverse proxy for information flow between sites. Identical patterns indicate high probability of interaction regardless of mechanism (trade, migration, shared history, copying).
**Page**: pp. 2-3
**Type**: methodological
**Evidence cited by author**: Masucci et al. 2011 (Jensen-Shannon divergence); Mills et al. 2013a (Brainerd-Robinson index comparison)
**Depends on**: 15 decorated ceramic ware types across the SWSN v1.0 dataset
**Notes**: The Jensen-Shannon index provides a natural interpretation as information flow, unlike the Brainerd-Robinson coefficient which behaves differently in the tails. The measure is agnostic about mechanism, which is both a strength (generality) and a limitation (cannot distinguish trade from migration).

**Evidence strength**: Strong (well-justified methodological choice)
**Assessment**: The measure is appropriate for the research question. For the model, the key implication is that ceramic similarity tracks the aggregate intensity of social interaction, which is the outcome variable for Layer 3 (cooperation networks).

---

### Claim 11

**Statement**: The model residuals display evidence of transitivity and triad closure, with more closed triangle structures than would be expected by chance, a common feature of human social networks.
**Page**: p. 8
**Type**: empirical
**Evidence cited by author**: Stillman et al. 2017
**Depends on**: Analysis of model residual structure
**Notes**: Triad closure (friends of friends tend to be friends) is a basic structural feature of human social networks. Its presence in the residuals suggests that the spatial interaction model does not fully capture network formation processes, which may include signaling-based partner selection.

**Evidence strength**: Moderate
**Assessment**: The triad closure finding is consistent with the model's prediction that signaling attracts exchange partners who then form clusters, but this is not a direct test.

---

## Claim Type Definitions

- **Empirical**: Direct observation or measurement reported by the author
- **Interpretive**: Inference from empirical data; not directly observable
- **Speculative**: Acknowledged by the author as tentative, or basis unclear
- **Methodological**: Claim about how to conduct or interpret research

## Evidence Strength Ratings

- **Strong**: Claim is well-supported by the evidence presented
- **Moderate**: Claim is partially supported; some evidence but gaps remain
- **Weak**: Claim is poorly supported by the evidence presented
- **Assertion without evidence**: No evidence cited; claim is stated as fact without support

## Summary Assessment

Gauthier 2021 provides robust empirical evidence that hydroclimate variability structured social interaction networks in the prehistoric Southwest, independent of distance effects. The six drought patterns (EOFs) represent different oceanic and continental moisture sources, and sites in different climate zones maintained stronger ties than distance alone would predict. This finding directly supports the model's Layer 3 prediction: exchange networks form to buffer against spatially correlated environmental shocks, and the value of inter-regional ties increases when partners experience different drought regimes. The paper does not address costly signaling directly but identifies the free-rider problem in network maintenance and calls for simulation approaches, both of which the mls-monuments model addresses. The temporal finding that climate-structured ties became more important after AD 1300 is relevant to understanding network reorganization during and after the Chaco era.
