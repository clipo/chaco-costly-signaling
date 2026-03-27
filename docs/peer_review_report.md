# Peer Review Report (Round 4: Re-Audit)

**Manuscript:** Formalizing Costly Signaling at Chaco Canyon
**Authors:** Carl P. Lipo and Robert J. DiNapoli
**Date:** 2026-03-27
**Review mode:** Re-audit Round 4

---

## Round 3 "Consider" Items: 4/5 resolved, 1 pre-submission

| # | Issue | Status |
|---|-------|--------|
| 1 | Simulation is consistency check | **Addressed** |
| 2 | P6 severity caveat | **Addressed** |
| 3 | Quality-from-rooms circularity | **Addressed** |
| 4 | Levene's power claim | **Addressed** |
| 5 | Unverified citations | **Not addressed** (pre-submission) |

---

## "Must Fix" (Round 4): None

## "Consider Addressing" (Round 4)

### Agreement (2+ reviewers)

1. **The Section 6.2 surplus comparator is too simple** (Adversarial raises; Domain would agree). The surplus model tested is "construction declines only during drought." A depletion-augmented surplus model (cumulative resource degradation + rising procurement costs + labor mobility) predicts the same collapse features. Section 6.2 should either steel-man the comparator or acknowledge the limitation.

2. **Rolling-window correlation p-values are inflated by autocorrelation** (Methods raises). The 20-year rolling windows applied to autocorrelated PMDI produce strongly correlated series; nominal n=301 overstates effective degrees of freedom. Direction is robust; p-values should be qualified.

3. **Lambda-sigma feedback is empirically inert but still rhetorically prominent** (Adversarial and Domain agree). The abstract, Sections 2.4, 3.2, 3.4, 6.1, 6.4, 6.5 all invoke it as operative. Section 6.2 concedes the collapse tests "do not require" it. The conclusion should reflect where the empirical weight actually lies.

4. **LOO model comparison needs elpd values reported** (Methods). Weight=1.0 for signaling contradicts "effectively equivalent" caption. Report actual elpd differences and SEs.

5. **Duplicate section numbering** (Domain). Two "6.2" headers; needs cleanup.

6. **CRA dataset vs. Guiterman et al. conflation** (Domain). Section 6.7 references "Guiterman et al. 240,000-timber dataset" for future analysis but the annual-resolution test was already conducted with the CRA data.

### Pre-submission items

7. Resolve 4 unverified citations
8. Report Bayesian changepoint convergence diagnostics
9. Report full prior specification (HalfNormal on sigma)
10. Harmonize likelihood (Normal vs. Poisson) across Bayesian analyses

---

## Strongest Counterargument (Round 4)

The adversarial reviewer's core objection: **Section 6.2 tests a straw-man surplus model.** A depletion-augmented surplus model predicts the same three collapse features (pre-drought decline from resource exhaustion, non-recovery from landscape degradation, Aztec displacement from labor migration to better location). The signaling model's uniquely novel mechanism (Layer 3 lambda-sigma) is definitively falsified. The surviving support comes from formalizing Layers 1-2, which were already proposed verbally by Kantner and Vaughn (2012) and Safi (2015).

**Assessment:** This is a legitimate concern. The paper should acknowledge that the Section 6.2 discrimination tests were formulated post hoc and that a more sophisticated surplus model could accommodate the collapse evidence. The paper's primary contribution is the formalization itself, which makes predictions testable and falsifiable. That P5 was specific enough to fail is itself the strongest argument for formalization over narrative approaches.

---

## Revision Plan (Round 4)

1. **[Moderate]** Steel-man the surplus comparator in Section 6.2 or acknowledge the limitation. Note that a depletion-augmented surplus model could accommodate the collapse features. The discrimination is between the naive surplus model and the signaling model; more sophisticated surplus models remain viable.

2. **[Moderate]** Reframe the conclusion to reflect that empirical weight rests on Layers 1-2 formalization and the collapse sequence, not on the lambda-sigma feedback (Layer 3). Layer 3 is a hypothesis awaiting reformulation.

3. **[Moderate]** Qualify rolling-window p-values or add block bootstrap CIs.

4. **[Low]** Fix duplicate section numbering, dataset conflation, LOO elpd reporting.

5. **[Pre-submission]** Unverified citations, Bayesian diagnostics, prior specification, likelihood harmonization.

---

## Overall Trajectory

Round 1: 5 must-fix. Round 2: 3 must-fix. Round 3: 0 must-fix. Round 4: 0 must-fix.

The manuscript is publishable. The surviving issues are refinements of framing and statistical reporting, not structural problems. The adversarial reviewer's strongest point (straw-man surplus model) is well-taken and should be acknowledged, but it does not undermine the paper's core contribution: the first formal, falsifiable framework for Chaco costly signaling, with honest reporting of both successes and failures.
