# Summary: Enquist & Leimar 1983

**Full citation**: Enquist, M. & Leimar, O. 1983. Evolution of fighting behaviour: Decision rules and assessment of relative strength. *Journal of Theoretical Biology* 102(3):387-410.
**Claims file**: `docs/references/claims/Enquist_Leimar_1983_original_claims.md`
**Verified against PDF**: Yes (1212468.pdf)
**Date summarized**: 2026-03-23

**IDENTITY NOTE**: This is the ORIGINAL 1983 paper introducing the sequential assessment model. A separate summary (`Enquist_Leimar_1983.md`) covers the 1987 follow-up paper (J. theor. Biol. 127:187-205), which extends the 1983 model to incorporate variation in resource value. This 1983 paper is the foundational source for Layer 2 (intergroup assessment and conflict deterrence).

---

## Relevance to Argument

This paper provides the core theoretical machinery for Layer 2 of the three-layer costly signaling model for Chaco Canyon. The sequential assessment model formalizes how contestants with incomplete information about each other's quality resolve conflicts through a series of costly interactions, each providing a noisy signal of relative fighting ability. Two parameters govern the process: c (cost per interaction step) and sigma (observation noise per step). The key insight for the Chaco model is that sigma determines how many costly rounds are needed before contestants can accurately assess who is stronger. Monument signals function as a sigma-reducing technology: by making group quality observable prior to direct interaction, great houses allow approaching groups to estimate relative quality without paying the costs of sequential assessment rounds. This produces the "Pax Chaco" pattern: reduced intergroup conflict where signaling is intensive, because pre-contest assessment substitutes for costly fighting.

The paper also establishes three results with direct implications for the spatial and temporal patterning of Chaco conflict:

1. Contests between equally matched opponents are the costliest (p. 396). This predicts that signaling should be most intensive where multiple groups of similar quality coexist, consistent with the concentration of great houses in Chaco Canyon.

2. Assessment-based fighting produces positive expected utility (0.451), while wars of attrition without assessment produce zero (p. 401). This quantifies the value of assessment and, by extension, the value of monument signals that enable it.

3. Assessment-based strategies are evolutionarily stable against convention-based alternatives (p. 402). The mutual assessment mechanism is robust; groups cannot profit from simple deference rules.

## Key Claims

1. **Sequential assessment mechanism**: Fights consist of repeated costly interactions; at each step, opponents acquire noisy information about relative fighting ability theta, defined as ln(c_B/c_A). (pp. 387, 390-391)

2. **Observation noise sigma**: Each observation of theta is corrupted by normally distributed noise with standard deviation sigma. After n steps, the sampling error reduces to sigma/sqrt(n). (p. 391)

3. **ESS switching line**: The optimal strategy is a switching line in the causal factor space of (sampling average x, uncertainty sigma/sqrt(n)). A contestant retreats when its accumulated evidence falls below this line. The ESS is pure and unique for given c and sigma. (pp. 392, 394)

4. **Switching line is approximately linear**: The near-linearity of the ESS makes the model analytically tractable and suitable for incorporation into multi-agent simulations. (p. 395)

5. **Cost-per-step exponential in theta**: c_A = c exp(-theta/2) and c_B = c exp(theta/2), so small differences in fighting ability produce large cost asymmetries in extended contests. (p. 391)

6. **Expected cost is small relative to resource value**: For c = 0.005 and sigma = 1, expected fighting cost is 0.049, only ~10% of the expected benefit (0.451 utility from contested resource of value 1). Assessment produces "good fighting economy." (p. 395)

7. **Equal opponents produce costliest contests**: "It is more costly to meet an opponent of equal strength than one that is stronger" because neither party can rapidly determine it is outmatched. (p. 396)

8. **Higher sigma increases contest cost**: Table 1 shows that for c = 0.005, expected cost rises from 0.029 (sigma = 0.5) to 0.049 (sigma = 1.0) to 0.063 (sigma = 1.5). Similarly, increasing c from 0.005 to 0.02 raises expected cost from 0.049 to 0.095. (p. 399, Table 1)

9. **War of attrition as zero-assessment limit**: Without assessment, the ESS is a mixed strategy yielding zero expected utility. Assessment-based strategies are strictly superior. (p. 401)

10. **Assessment is evolutionarily stable against conventions**: A convention mutant (defer in intruder role) earns U(C, S) = 1/2 * U(S, S), strictly less than U(S, S), and cannot invade. (p. 402)

11. **Role asymmetries are less important when assessment occurs**: When fighting ability differences are assessed, role asymmetries (e.g., owner-intruder) are "less likely to play a role" in determining outcomes because the causal factor space will be dominated by ability estimates. (p. 403)

12. **Causal factor state sufficiency**: The sampling average x and step count n constitute a sufficient statistic for optimal decision-making, compressing all fight history into two numbers. (p. 404)

## Data Presented

- ESS switching lines plotted in two causal factor spaces: (x, sigma/sqrt(n)) and (x, n) (Figs. 1-2, p. 395)
- Curves of constant expected utility in the causal factor space (Fig. 3, p. 396)
- Probability of victory as a function of relative fighting ability theta (Fig. 4, p. 397): near-perfect discrimination for |theta| > 0.5; errors only for closely matched opponents
- Expected total cost as a function of theta (Fig. 5, p. 397): peak cost at theta = 0 (equal opponents), rapid decline for mismatched opponents
- ESS switching lines for sigma varying from 0.5 to 1.5, holding c = 0.005 (Fig. 6, p. 398): higher sigma produces lower switching lines early in the fight
- ESS switching lines for c varying from 0.0025 to 0.02, holding sigma = 1 (Fig. 7, p. 398): higher c produces higher switching lines (more cautious early behavior)
- Average fighting times as a function of |theta| for c = 0.005 and three sigma values (Fig. 8, p. 399): longest fights between matched opponents, with higher sigma increasing duration for unequal opponents
- Average fighting times as a function of |theta| for sigma = 1 and four c values (Fig. 9, p. 400): higher c (costlier interactions or lower resource value) produces shorter fights
- Standard deviation of fighting times as a function of |theta| (Fig. 10, p. 401): peaks sharply near theta = 0
- Table 1 (p. 399): Expected utility and expected cost for six combinations of sigma and c

## Methodological Notes

- The model assumes a single type of interaction repeated sequentially, with one contestant eventually retreating. This "best fits the case of a fight with only one intense phase." (p. 390)
- Per-step costs are assumed symmetric in the product sense: c_A * c_B = c^2 = constant. This reduces the model from three parameters (theta, c_A, c_B) to two (theta, c). (p. 390)
- The prior distribution of relative fighting ability is beta(theta) = exp(-theta)/(1 + exp(-theta))^2, derived from assuming weights m_A and m_B are exponentially distributed and c_B/c_A = m_A/m_B. (p. 392, Equation 3)
- ESS computation uses numerical iteration via a recursive utility equation (Equation 9, p. 393) solved from high n downward. Convergence confirmed for all tested parameter combinations. (p. 394; Appendix B, pp. 407-408)
- The stochastic model is formally defined using stopping times T_A and T_B, with fight duration T = min(T_A, T_B). If both stop simultaneously, a coin flip determines the winner. (p. 392, Equation 5)
- Appendix A (pp. 405-407) proves that the conditional distribution of theta given fight history is the same as the conditional distribution given only the sampling average, establishing the sufficiency of the causal factor space.
- Appendix C (pp. 408-410) discusses the computational implementation.

## Connections to Other Sources

- **Enquist & Leimar 1987** (J. theor. Biol. 127:187-205): The direct follow-up, which extends this model to incorporate variation in resource value (subjective V). The 1987 paper adds the utility equation U = pV - C, owner-intruder information asymmetry, and cross-species empirical validation across 18 species.
- **Maynard Smith 1974**: The war of attrition, shown here to be the special case without assessment (Section 5, p. 401). The sequential assessment model supersedes the war of attrition by incorporating information acquisition.
- **Maynard Smith & Parker 1976**: The graduated risk game, another assessment-free model with zero expected utility at ESS, contrasted with the positive expected utility of the sequential assessment model.
- **Parker 1974**: Discussed the idea that information about fighting ability is transmitted during a contest; the present paper formalizes this insight.
- **McFarland & Sibly 1975**: Source of the "causal factor space" concept adopted as the foundational representational framework for the model.
- **Penn & Szamado 2020**: Notes that Enquist (1985), building on this 1983 paper, "established the foundations of ESS signalling theory" (p. 280). The 1983 model is thus the direct precursor of formal signaling theory in evolutionary biology.
- **Neiman 1997**: Applies costly signaling logic to monumental architecture; the sequential assessment framework provides the formal mechanism for how monument signals reduce contest costs.
- **Roscoe 2009**: Applies social signaling to explain intergroup conflict in small-scale societies; the assessment mechanism formalized here underlies Roscoe's verbal argument.
- **Lekson 2002**: Documents the empirical pattern (Pax Chaco) that the sequential assessment model, combined with monument signaling, is designed to explain.

## Verification Notes

- PDF verified as present and complete (24 pages including ILL cover pages; article text on pp. 387-410)
- All claims extracted directly from PDF with page numbers from the original journal pagination
- Equations verified against PDF images
- Table 1 values verified against PDF
- This is confirmed to be the 1983 paper (J. theor. Biol. 102:387-410), distinct from the 1987 paper already in the repository
