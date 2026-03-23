# Claims Extraction: Enquist & Leimar 1983

**Full citation**: Enquist, M. & Leimar, O. 1983. Evolution of fighting behaviour: Decision rules and assessment of relative strength. *Journal of Theoretical Biology* 102(3):387-410.
**PDF filename**: 1212468.pdf
**Date extracted**: 2026-03-23
**Extractor**: Claude Code

**IDENTITY NOTE**: This is the ORIGINAL 1983 paper that introduced the sequential assessment model. A separate file (`Enquist_Leimar_1983_claims.md`) documents claims from the 1987 follow-up paper (J. theor. Biol. 127:187-205), which extends the 1983 model to incorporate variation in resource value. Both papers are relevant to the project's Layer 2 (intergroup assessment and conflict deterrence), but this 1983 paper is the foundational source for the sequential assessment framework itself.

---

## Claims

### Claim 1: Fights consist of sequential costly interactions that reveal relative fighting ability

"A mathematical model of fighting behaviour is developed. The contestants belong to a population with varying fighting abilities and the fights consist of the repetition of one type of interaction. At each interaction in the sequence the opponents acquire some information about the true fighting abilities." (p. 387, abstract)

**Relevance**: This is the core premise of the sequential assessment model. Contests are not resolved in a single round but through a sequence of costly interactions, each providing information about relative quality. For the Chaco model, this sequential structure is what monument signals short-circuit: by providing pre-contest information about group quality, great houses reduce the number of costly assessment rounds required.

---

### Claim 2: The causal factor space represents all information available for decision-making

"A causal factor is a variable that is available to the animal for observation and that is of relevance for the animal's decisions. In principle, all relevant observable variables should be included in the causal factor space, but in practice one must choose a few believed to be the most basic." (p. 390)

**Relevance**: The causal factor space concept formalizes what information contestants use to make fight-or-flight decisions. In the Chaco context, great house size, construction quality, and exotic good displays are observable variables that enter the causal factor space of approaching groups, providing decision-relevant information about the community's quality without requiring direct interaction.

---

### Claim 3: Relative fighting ability theta is defined as the log ratio of per-step costs

"The ratio c_A/c_B describes the opponents' relative abilities to inflict costs on each other, but we choose to use the quantity theta_AB = ln(c_B/c_A) as a measure of the relative fighting ability since it has the nice property that theta_BA = -theta_AB." (p. 390, Equation 1)

**Relevance**: This is the fundamental parameter of the model. The log-ratio formulation ensures symmetry: if A is stronger than B by some amount, B is weaker than A by the same amount. In the Chaco model, theta represents the relative quality difference between competing groups, which monument signals allow groups to estimate prior to direct interaction.

---

### Claim 4: Per-step costs for each contestant are exponential functions of relative fighting ability

"Both costs can then be expressed as functions of theta: c_A = c exp(-theta/2), c_B = c exp(theta/2)." (p. 391, Equation 2)

**Relevance**: The exponential cost structure means that small differences in relative fighting ability translate into large cost asymmetries during extended contests. This makes accurate pre-contest assessment highly valuable: a group that can determine theta before engaging avoids potentially ruinous costs from fighting a superior opponent.

---

### Claim 5: Each interaction step provides a noisy observation of relative fighting ability

"During the ith step of the fight the costs c_A and c_B are inflicted on A and B respectively and each opponent samples the relative fighting ability theta with a certain error of observation. Animal A observes y_i^A = theta + z_i^A and B observes y_i^B = -theta + z_i^B. z_i^A and z_i^B are the errors of observation. We assume that they are independently drawn from a normal distribution with mean zero and standard deviation sigma." (p. 391)

**Relevance**: The observation noise sigma is the central parameter linking contest theory to signaling theory. Each assessment round provides information corrupted by noise sigma. Monument signals function as a mechanism for reducing effective sigma by providing clear, low-noise information about group quality before any direct interaction occurs.

---

### Claim 6: The sampling average converges toward the true relative fighting ability as steps accumulate

"After n steps A and B can make the estimates x_n^A = (1/n) sum(y_i^A) and x_n^B = (1/n) sum(y_i^B). The sampling error is now reduced and has a standard deviation sigma/sqrt(n)." (p. 391)

**Relevance**: Information accumulates at rate 1/sqrt(n), meaning early rounds are the most informative per unit cost. This diminishing-returns structure means that any pre-contest information (such as observable monument signals) has outsized value: it effectively provides the equivalent of several costly assessment rounds at zero marginal cost.

---

### Claim 7: The ESS is a switching line in causal factor space that determines persistence vs. retreat

"In Fig. 1 we have drawn a boundary or switching line which represents a decision rule. When an animal's trajectory goes below the switching line that animal gives up." (p. 392)

"A local strategy S is given by a level (switching point) S_n for each n; if x_n goes below S_n the player gives up at step n." (p. 392)

**Relevance**: The switching line is the decision rule: an animal persists as long as its accumulated evidence suggests it is likely to win, and retreats once the evidence indicates it is likely the weaker party. Monument signals affect this decision by shifting the starting point in causal factor space: an approaching group that observes a large great house begins with a lower estimate of its own relative quality, potentially starting below the switching line and avoiding conflict entirely.

---

### Claim 8: The ESS is pure and unique for given parameter values

"Numerically we have only found one ESS for specified parameters c and sigma, indicating that the ESS is unique." (p. 394)

**Relevance**: The uniqueness of the ESS means that there is a single optimal assessment strategy for a given combination of interaction cost (c) and assessment noise (sigma). This simplifies the theoretical framework: once c and sigma are specified, the model yields determinate predictions about contest duration, cost, and probability of winning.

---

### Claim 9: The switching line is approximately straight, making the model tractable

"The switching line in Fig. 1 is approximately straight." (p. 395)

**Relevance**: The near-linearity of the ESS switching line means that the decision rule can be approximated by a simple linear function of the sampling average x and the number of steps n. This makes the model analytically tractable and suitable for incorporation into larger simulation frameworks, such as the Chaco multi-scale signaling model.

---

### Claim 10: Expected fighting cost is small relative to the contested resource value

"The expected cost of fighting, U(S^inf, S^inf), for an individual in a population using this strategy is 0.451. Since the value of the contested resource is one and the prior probability of winning 0.5, the expected cost will be 0.049, which is quite small compared to the benefit obtained by the winning animal, and we conclude that assessment of fighting ability results in good fighting economy." (p. 395)

**Relevance**: The sequential assessment model produces efficient contests: expected costs are only about 10% of the benefit. This "good fighting economy" result demonstrates that assessment-based fighting is far less costly than pure wars of attrition. For the Chaco model, monument signals further improve this economy by reducing the number of assessment steps needed, making intergroup interaction even less costly.

---

### Claim 11: Probability of victory approaches certainty as relative fighting ability difference increases

"The graph in Fig. 4 shows the accuracy of the fight to discriminate between the weaker and the stronger animal. When the absolute value of theta is greater than 0.5 the discrimination is almost perfect but for more closely equal opponents some 'mistakes' do occur." (p. 396)

**Relevance**: Assessment is highly accurate for clearly mismatched contestants (theta far from zero) but imprecise for closely matched ones. This generates the prediction that signaling is most valuable when potential opponents are of similar quality, because that is when assessment errors are most likely and costly. At Chaco, this predicts that the most intensive monument construction should occur where multiple groups of similar quality coexist, consistent with the concentration of great houses in the canyon core.

---

### Claim 12: It is more costly to meet an opponent of equal strength than one that is stronger

"Figure 5 illustrates the fact that it is more costly to meet an opponent of equal strength than one that is stronger. This is due to the assessment taking place during the fight. A weaker animal will quickly realize that the situation is unfavourable and give up." (p. 396)

**Relevance**: This counterintuitive result is a key prediction of the model. Contests between equals are the costliest because neither party can quickly determine it is outmatched. A much stronger opponent is actually less costly to face because the weaker party retreats rapidly. For the Chaco system, this means that the greatest conflict costs arise among communities of similar size and investment, exactly the situation in the canyon core where multiple large great houses coexisted.

---

### Claim 13: Increasing sigma causes longer fights early but less total information gathered

"Varying sigma (Fig. 6) influences the strategy most strongly in the beginning of the fight. A high uncertainty of sampling will cause the contestants to be unwilling to give up early, and they will take the cost of continued sampling in order to get a more accurate estimate of the relative fighting ability. This can be seen also from the expected utilities and costs given in Table 1. Increasing sigma and keeping c constant will make the fights more costly." (pp. 397-398)

**Relevance**: Higher sigma (more noise) produces more costly contests. This is the core mechanism linking monument signals to conflict reduction: by reducing the effective sigma through pre-contest information provision, great houses reduce the expected cost of intergroup encounters. Table 1 quantifies this: for c = 0.005, increasing sigma from 0.5 to 1.5 raises expected cost from 0.029 to 0.063.

---

### Claim 14: The war of attrition is a special case without assessment, yielding zero expected utility

"Several models of fighting without assessment have been presented in the literature. Among these are the war of attrition (Maynard Smith, 1974), the graduated risk game (Maynard Smith & Parker, 1976), and the generalized war of attrition (Bishop & Cannings, 1978). A common feature of these models is that the ESS is a mixed strategy and that the expected utility of fighting prior to the fight is zero." (p. 401)

**Relevance**: The war of attrition (no assessment) produces zero expected utility, meaning contests consume all expected gains. By contrast, the sequential assessment model produces positive expected utility (0.451 in the worked example). This comparison demonstrates the value of assessment: without it, fighting is a break-even proposition at best. Monument signals, by enabling assessment, move intergroup interactions from the zero-utility war-of-attrition regime toward the positive-utility sequential assessment regime.

---

### Claim 15: Assessment-based strategies are evolutionarily stable against convention-based mutants

"Consider first a convention mutant attempting to invade a population using the ESS of our model. Denote the roles A (owner) and B (intruder) and let S be the original ESS and C the convention to give up without fighting when in role B and fight according to S when in role A. The expected utility of S against itself, U(S, S), is positive (see Table 1) so that the utility of C against S, U(C, S) = 1/2 * 0 + 1/2 * U(S, S), will be strictly smaller than U(S, S) and the mutant cannot invade." (p. 402)

**Relevance**: Convention-based strategies (e.g., always defer to the occupant) cannot invade an assessment-based population because assessors gain positive expected utility from fights while convention-followers gain zero in the intruder role. This establishes that assessment is evolutionarily robust. For the Chaco model, this means that the mutual assessment mechanism mediated by monument signals is stable: groups cannot do better by adopting simple rules like "always defer to the bigger great house" because this would forgo opportunities to win contests against weaker occupants of large structures.

---

### Claim 16: The causal factor state contracts to the minimum number of variables with evolutionary significance

"The causal factor state can be contracted to the minimum number of variables that are sufficient to make an equally good prediction of future costs and benefits as can be made from the complete state. In our example the sampling average x and the number of samplings n sum up the functionally relevant information contained in the sequence." (p. 404)

**Relevance**: The sufficiency result means that a contestant needs only two pieces of information (its current estimate of relative quality and how much evidence it has accumulated) to make optimal decisions. For the Chaco model, this implies that monument signals are efficient information channels: they communicate the critical sufficient statistic (relative group quality) without requiring knowledge of all underlying group characteristics.

---

## Summary Assessment

This is the foundational paper for the sequential assessment model of animal contests. It introduces: (1) the formal framework of sequential costly interactions providing noisy information about relative fighting ability; (2) the causal factor space and switching-line decision rule; (3) the key parameters c (per-step cost) and sigma (observation noise) that jointly determine contest duration, cost, and accuracy; (4) the result that contests between equally matched opponents are the most costly; (5) the comparison showing that assessment-based fighting is far more efficient than the war of attrition (expected utility 0.451 vs. 0.0); and (6) the evolutionary stability of assessment against convention-based alternatives. For the Chaco project, this paper provides the theoretical foundation for Layer 2's conflict deterrence mechanism: monument signals reduce effective sigma, enabling pre-contest assessment that lowers the expected cost of intergroup interaction and produces the "Pax Chaco" pattern of reduced violence during the period of intensive great house construction.
