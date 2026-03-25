# Peer Review Report (Round 3: Re-Audit)

**Manuscript:** Formalizing Costly Signaling at Chaco Canyon: A Multilevel Model of Monumental Architecture, Exotic Goods, and Cooperation Networks Under Environmental Uncertainty

**Authors:** Carl P. Lipo and Robert J. DiNapoli

**Date:** 2026-03-25

**Review mode:** Re-audit Round 3 (prior reviews: Round 1 and Round 2, 2026-03-24)

---

## Round 2 Issue Tracking Summary

### Round 2 "Must Fix" (3 items)

| # | Issue | Status |
|---|-------|--------|
| 1 | Correct fitness gain formula | **Addressed.** Main text matches Appendix A. |
| 2 | Reframe P5 as unsupported at tested resolution | **Addressed.** "Not Supported at tested resolution" throughout. |
| 3 | Verify Appendix A complete | **Addressed.** Five subsections (A.1-A.5), self-contained. |

### Round 2 "Consider Addressing" (9 items)

| # | Issue | Status |
|---|-------|--------|
| 1 | P1 severity caveat | **Addressed.** "Supported (convergent; severity caveat)." |
| 2 | Simulation disclaimer or alignment | **Addressed.** Simulation rewritten; implements all three layers. |
| 3 | Figure 3 lambda sensitivity | **Addressed.** Lambda 0.2-1.2 with shaded envelope. |
| 4 | Assessment noise micro-foundation | **Addressed.** Grounded in sequential assessment theory. |
| 5 | Clarify Lakatos degeneracy | **Addressed.** Distinguishes frameworks from empirical research. |
| 6 | Engage Vivian (1990) | **Addressed.** Section 1.2 with reference. |
| 7 | Rho values as illustrative | **Addressed.** Ordering is load-bearing, not magnitudes. |
| 8 | Reframe period-level test | **Addressed.** Levene's on annual data (n=110, 170). |
| 9 | Mayo/Lakatos per prediction | **Partially addressed.** P1 and P5 have severity analysis; P6 does not. |

**Score: 3/3 must-fix resolved. 8/9 consider-addressing resolved (1 partial).**

---

## Reviewer 1: Domain Expert (Round 3)

### Summary
The revision addresses four of five Round 2 remaining weaknesses and all five suggestions except the rolling-window PMDI correlation. The most consequential improvements: Appendix A is complete, fitness gain formula corrected, P5 forthrightly downgraded, Vivian engaged, Lakatos clarified, simulation aligned. The single surviving weakness (annual-resolution PMDI test) is now less damaging because P5 has been honestly downgraded.

### Remaining Weaknesses
1. **Annual-resolution PMDI-construction correlation still not conducted.** Deferred to next stage. Less critical now that P5 is downgraded, but the data are in hand.
2. **New: Simulation parameter sensitivity not demonstrated.** Figure 8 shows 20 replicates under one configuration; robustness to parameter variation not shown.
3. **New: Quality-from-rooms mapping in simulation embeds the same circularity as P1.** Should be flagged as a simulation design limitation.
4. **Minor: Unverified citations on line 402 should be resolved before submission.**

---

## Reviewer 2: Methods Expert (Round 3)

### Summary
All six Round 2 remaining weaknesses are resolved. The simulation now implements the manuscript's equations. The fitness gain formula is corrected. Figure 3 shows lambda sensitivity. Assessment noise is grounded in sequential assessment theory. Signal fidelity is framed as illustrative. Period-level test is properly framed. The methods are sound for a framework paper.

### Remaining Weaknesses
1. **Simulation validates on calibration data without acknowledging this.** Reproducing qualitative patterns from Chaco inputs is internal consistency, not independent confirmation.
2. **Quality-from-rooms creates soft circularity in the simulation.**
3. **No autocorrelation-adjusted effective sample sizes for Levene's test.** With lag-1 r=0.36, effective n may be 40-50% of nominal.

---

## Reviewer 3: Adversarial (Round 3)

### Summary
The P5 treatment is now exemplary. The simulation alignment and formula correction are complete. Vulnerabilities have shifted from technical errors to subtler conceptual issues that domain/methods reviewers are less likely to catch.

### Critical Concerns

1. **Simulation reproduces calibration data, not independent predictions.** The simulation uses Chaco PMDI as input, initializes from archaeological room counts, and uses founding dates from the chronology. Reproducing qualitative patterns is a consistency check, not a test. The paper should state this explicitly.

2. **P6 (network co-evolution) should receive the same severity analysis as P1 and P5.** It is classified as "discriminating" but surplus models predict the same temporal co-occurrence. Without a lag analysis at finer than 50-year resolution, P6 cannot be distinguished from surplus-driven growth. Should be reclassified as convergent or given a severity caveat.

3. **"Illustrative" parameters shield the simulation from falsification.** Any mismatch can be attributed to parameter choice rather than model failure. The quality-from-rooms calibration ensures the Spence gradient by construction.

### Strongest Counterargument (Updated)

**The supported discriminating predictions are either observability patterns any signal-function hypothesis would predict (P3), temporal co-occurrences surplus models also predict (P6), or complicated by EP Events (P4). The one prediction uniquely requiring the lambda-sigma feedback (P5) has failed its test. Without P5, the model's distinctive contribution is the formal apparatus, not the empirical predictions.** The paper can survive this by reframing the contribution as formalization that makes severe testing possible, rather than as a programme that has already passed severe tests. The annual-resolution test remains available and would resolve this.

---

## Synthesis

### Agreement (2+ reviewers)

1. **Simulation demonstrates internal consistency, not independent prediction** (all 3). The simulation uses Chaco data as input and reproduces patterns from that input. This should be stated explicitly as a consistency check, not as empirical confirmation.

2. **Quality-from-rooms circularity in the simulation** (Reviewers 1 and 2). The same circularity acknowledged for P1 is embedded in the simulation but not flagged there.

3. **P6 may need a severity caveat or reclassification** (Reviewer 3 raises; Reviewers 1 and 2 would likely agree on reflection). Surplus models predict the same temporal co-occurrence of construction and network growth.

### What Improved (Round 2 → Round 3)

The revision resolved all 3 "must fix" items and 8 of 9 "consider addressing" items from Round 2. Key advances:
- Simulation now implements the formal model equations (Spence, lambda-sigma, assessment noise, exponential survival)
- Fitness gain formula corrected
- Assessment noise grounded in sequential assessment theory
- Figure 3 lambda sensitivity, Figure 6 updated without threshold, Figure 7 updated prediction summary, Figure 8 simulation dynamics, Figure 13 quality-investment scatter
- Schwarz (2023) comparative case on cost-shifting
- Vivian (1990) engaged
- Lakatos/Mayo distinction clarified

### "Must Fix" (Round 3)

None. The manuscript has no blocking issues. The remaining items are refinements.

### "Consider Addressing" (Round 3)

1. **State explicitly that the simulation demonstrates internal consistency (dynamic sufficiency), not independent empirical confirmation.** One sentence in Section 6.6 would suffice: "The simulation demonstrates that the model's equations are dynamically sufficient to generate Chaco-like trajectories from Chaco-calibrated inputs; it does not constitute an independent empirical test because the inputs are derived from the same archaeological record the outputs are compared against."

2. **Add a severity caveat to P6 or reclassify as convergent.** The temporal co-occurrence of peak construction and peak network connectivity is predicted by surplus models as easily as by signaling models. At 50-year resolution, lag vs. co-occurrence cannot be distinguished. A caveat analogous to P1's would be appropriate.

3. **Note the quality-from-rooms circularity in the simulation description.** A sentence in Section 6.6 or Data Availability noting that the simulation's quality proxy shares the circularity acknowledged for P1.

4. **Qualify the Levene's test power claim** by noting the autocorrelation adjustment, or remove the "adequate power" assertion.

5. **Resolve the four unverified citations** (line 402) before submission.

### Revision Plan (Round 3, ordered by priority)

1. **[Moderate]** Add one sentence to Section 6.6 clarifying that the simulation is a consistency check (dynamic sufficiency), not an independent test.
2. **[Moderate]** Add severity caveat to P6 assessment, or reclassify as convergent.
3. **[Low]** Note simulation quality-from-rooms circularity.
4. **[Low]** Qualify or remove the Levene's test power claim.
5. **[Pre-submission]** Resolve unverified citations.

### Overall Trajectory

Round 1 identified 5 "must fix" and 10 "consider" items. Round 2 identified 3 "must fix" and 9 "consider" items. Round 3 identifies 0 "must fix" and 5 "consider" items. The manuscript has progressed from structural problems (no derivations, wrong equations, misaligned code) through honest empirical reckoning (P5 null result) to refinements of framing and classification. The paper is at or near publication readiness. The surviving issues are legitimate but none would block acceptance at a journal like JAMT or JAA. The strongest remaining vulnerability is that the model's most distinctive mechanism (lambda-sigma feedback) lacks empirical support, but the paper is transparent about this and specifies the test that would provide it.
