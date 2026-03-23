# Summary: Enquist & Leimar 1987

**Full citation**: Enquist, M. & Leimar, O. 1987. Evolution of fighting behaviour: The effect of variation in resource value. *Journal of Theoretical Biology* 127(2):187-205.
**Claims file**: `docs/references/claims/Enquist_Leimar_1983_claims.md`
**Verified against PDF**: Yes
**Date summarized**: 2026-03-23

**IDENTITY NOTE**: The PDF in the repository (`evolution-of-fighting-behaviour-the-effect-of-variation-in-4q851om2xh.pdf`) is the 1987 paper, not the 1983 paper originally listed. The 1983 paper (J. theor. Biol. 102:387-410) introduced the sequential assessment model; this 1987 paper extends it to incorporate variation in resource value. Both papers develop the sequential assessment framework central to the project's Layer 2. The 1983 paper is cited extensively within the 1987 paper and the key concepts (sequential assessment, noisy estimation of relative fighting ability, switching lines) are described and used as the basis for the new models.

---

## Relevance to Argument

This paper provides the formal theoretical foundation for the mls-monuments model's Layer 2 (intergroup assessment and conflict deterrence). The sequential assessment model establishes that: (1) contestants acquire information about relative fighting ability through costly interaction; (2) contests end when one party's estimate of relative ability crosses a threshold (switching line); (3) the noisier the assessment process, the longer and costlier contests become; and (4) resource value modulates persistence, cost, and win probability. Monument signals map onto this framework as a mechanism for reducing assessment noise (sigma): by providing observable, pre-contest information about group quality, monuments reduce the number of costly assessment steps needed for accurate evaluation, lowering the expected cost of intergroup interaction.

## Key Claims

1. **Utility equation**: U = pV - C, where p is probability of winning, V is resource value, and C is cost. This is the foundation for the Layer 2 conflict probability function. (p. 188)
2. **Sequential assessment mechanism**: Contestants acquire information through costly rounds of interaction, updating estimates of relative quality and persisting until their estimate crosses a switching-line threshold. (pp. 191-192)
3. **Assessment noise (sigma)**: Observation errors are normally distributed with standard deviation sigma. Higher sigma means more rounds needed for accurate assessment, hence costlier contests. (p. 192)
4. **Resource value scales fighting investment**: ESS strategies prescribe more costly and persistent behavior as subjective resource value increases, with this result supported across 18 species (Table 1). (pp. 190, 199)
5. **Information asymmetry (owner-intruder)**: When owners know resource value but intruders do not, owners become more persistent as value increases, and intruders tend to win "wrong" fights over low-value resources while losing high-value contests. (pp. 195-196)
6. **Matched contests are costliest**: The longest and most expensive interactions occur between closely matched opponents, not between clearly mismatched ones. (pp. 194-195)

## Data Presented

- Two numerical ESS solutions for sequential assessment games with resource value variation (Figs. 1, 3)
- Expected fight duration as function of resource value (Figs. 2, 6)
- Probability of owner winning as function of resource value in information-asymmetric contests (Fig. 4)
- Intruder's expected resource value as function of fight duration and relative fighting ability estimate (Fig. 5)
- Empirical data compilation from 18 species showing fight duration, offensive behavior, and probability of victory all increase with resource value (Table 1, p. 199)
- Isotope ratio data for 22 turquoise source areas (Table 1, p. 189; wrong paper, this is from Hull)

## Methodological Notes

- ESS determination via numerical iteration: starting from an initial strategy, best replies are computed until convergence (Appendix C, pp. 203-205)
- The model assumes cost per step is symmetric (c_A * c_B = c^2) to reduce dimensionality (p. 192)
- Prior distribution of relative fighting ability is normal with mean zero and standard deviation 0.5; cost parameter c = 0.05 in worked examples (p. 193)
- Model considers three informational situations: (1) symmetric resource value, (2) role asymmetry with resource value determined by role, (3) variation in subjective resource value with no correlation between contestants (pp. 190-191)

## Connections to Other Sources

- **Enquist & Leimar 1983** (J. theor. Biol. 102:387): The original sequential assessment model, cited extensively. The 1987 paper builds directly on this framework.
- **Leimar & Enquist 1984** (J. theor. Biol. 111:475): Effects of asymmetries in owner-intruder interactions; directly extended in the second example of this paper.
- **Maynard Smith 1982**: Evolutionary game theory framework within which the model is developed.
- **Bishop, Cannings & Maynard Smith 1978**: War of attrition with random rewards; the first example in this paper extends this model.
- **Penn & Szamado 2020**: Notes that Enquist (1985) "established the foundations of ESS signalling theory" (p. 280). The 1987 paper further develops this foundation.
- **Roscoe 2009**: Group-level signaling and conflict deterrence in New Guinea, providing ethnographic application of the theoretical principles formalized here.

## Verification Notes

- PDF verified as present and complete (19 pages, J. theor. Biol. 127:187-205, 1987)
- All claims extracted directly from PDF with page numbers
- The paper is the 1987 follow-up, not the 1983 original. The INDEX entry has been filed under Enquist_Leimar_1983 for continuity but the citation must be updated.
