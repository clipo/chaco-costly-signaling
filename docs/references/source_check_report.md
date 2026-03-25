# Source-Checker Audit Report

**Date:** 2026-03-24
**Manuscript:** Chaco_Signaling_Manuscript.md
**Auditor:** Claude Code (automated)

---

## Infrastructure Summary

| Component | Location | Count |
|-----------|----------|-------|
| Manuscript | `docs/manuscript/Chaco_Signaling_Manuscript.md` | 687 lines |
| INDEX | `docs/references/INDEX.md` | 42 entries |
| Claims files | `docs/references/claims/` | 42 files |
| Summary files | `docs/references/summaries/` | 42 files |
| PDFs | `docs/references/pdfs/` | present |
| .bib file | n/a | none |

---

## Citation Inventory

Total unique citations in manuscript body (lines 1-440): **71**
Total entries in References section (lines 441-576): **55**
Total entries in INDEX.md: **42**

---

## Critical Issues

### C1. Citations in body with NO entry in References section

These citations appear in the manuscript text but have no corresponding entry in the References list. This must be fixed before submission.

| Citation | Body lines | Notes |
|----------|------------|-------|
| Bliege Bird and Smith 2005 | 402 | Cited in limitations paragraph; no reference entry |
| Dean 1988 | 284 | Secondary citation via Lekson 2002; needs own entry or "cited in" notation |
| Dean 1996 | 284 | Secondary citation via Lekson 2002; needs own entry or "cited in" notation |
| Ember and Ember 1992 | 284 | Secondary citation via Lekson 2002; needs own entry or "cited in" notation |
| LeBlanc 1999 | 284 | Secondary citation via Lekson 2002; needs own entry or "cited in" notation |
| Roscoe 2009 | 402 | Cited in limitations paragraph; no reference entry |
| Trigger 1990 | 402 | Cited in limitations paragraph; no reference entry |

**Action required:** Either add full reference entries for all seven, or convert Dean 1988/1996, Ember and Ember 1992, and LeBlanc 1999 to explicit secondary citations (e.g., "Lekson 2002, citing Dean 1988") and add entries for Bliege Bird and Smith 2005, Roscoe 2009, and Trigger 1990.

### C2. Orphan citations: in manuscript body but NOT in INDEX.md

These 38 citations appear in the manuscript but have no INDEX entry. Twenty are expected new references from the revision; 18 are other gaps.

**Expected new references (need INDEX entries added):**

| Citation | Body lines |
|----------|------------|
| Cordell and Gumerman 1989 | 48 |
| Crown and Judge 1991 | 48 |
| Gille et al. 2017 | 76, 300, 412 |
| Gumerman 1988 | 48 |
| Gumerman 1994 | 48 |
| Heitman and Plog 2015 | 48 |
| Kitcher 1981 | 52, 432 |
| Kuckelman et al. 2002 | 286, 290 |
| Lakatos 1970 | 50, 70 |
| Lewontin 1974 | 82 |
| Mailath 1987 | 643 (Appendix) |
| Mayo 2018 | 52, 84, 213, 254, 308 |
| Noble 1984 | 48 |
| Noble 2004 | 48 |
| Ortiz 1972 | 48 |
| Perreault 2019 | 48, 422 |
| Priem et al. 2022 | 48 |
| Turner and Turner 1999 | 284 |
| Van Dyke and Heitman 2021 | 48 |
| Vivian 1990 | 48 |

**Other citations not in INDEX (pre-existing gaps):**

| Citation | Body lines | Notes |
|----------|------------|-------|
| Benson et al. 2019 | 28, 42, 114, 412 | Key Chaco reference; heavily cited |
| Cook et al. 2004 | 54, 76 | LBDA paleoclimate data |
| Crown and Hurst 2009 | 26 | Cacao evidence |
| Dean 1988 | 284 | Secondary via Lekson 2002 |
| Dean 1996 | 284 | Secondary via Lekson 2002 |
| Ember and Ember 1992 | 284 | Secondary via Lekson 2002 |
| Force et al. 2002 | 190, 302 | Chaco paleo-channels |
| Grafen 1990 | 92 | Signaling theory foundational |
| Grissino-Mayer 1996 | 190, 302 | Dendro precipitation reconstruction |
| Grissino-Mayer 1997 | 190, 302 | Dendro precipitation reconstruction |
| Guiterman et al. 2015 | 50, 54, 76, 308, 352, 412, 414, 430 | Key reference; very heavily cited |
| Judge 1989 | 40 | Chaco pilgrimage model |
| LeBlanc 1999 | 284 | Secondary via Lekson 2002 |
| Lekson 2006 | 24, 38, 48 | Key Chaco edited volume |
| Mathien 2001 | 26 | Turquoise production |
| Renfrew 2001 | 40 | Sacred economy model |
| Spence 1973 | 92 | Foundational signaling theory |
| Windes 1987 | 38 | Pueblo Alto excavation |

**Priority:** Benson et al. 2019, Cook et al. 2004, and Guiterman et al. 2015 are among the most heavily cited references in the manuscript and should be added to INDEX as high priority. Spence 1973 and Grafen 1990 are foundational signaling theory references critical to the argument.

### C3. INDEX naming discrepancy

| INDEX entry | Manuscript citation | Issue |
|-------------|-------------------|-------|
| Gillreath_Brown_et_al_2024 | Gillreath-Brown and Kohler 2024 | INDEX uses "et al." but the paper has only two authors |

---

## Warnings

### W1. Orphan INDEX entries: in INDEX but never cited in manuscript body

These seven sources have INDEX entries, summaries, and claims files but are not cited anywhere in the manuscript.

| INDEX entry | Notes |
|-------------|-------|
| Dorshow and Wills 2022 | GIS agricultural suitability analysis |
| Enquist and Leimar 1987 | Sequel to the 1983 paper; 1983 is cited instead |
| Glatz and Plourde 2011 | Hittite CST comparison case |
| LeBlanc 2017 | Note: INDEX flags wrong PDF for this entry |
| Sanger 2017 | Late Archaic storage; peripheral to Chaco |
| Schwarz 2023 | Maya CST collapse/regeneration; SSRN preprint |

**Recommendation:** Consider whether any of these should be cited (especially Schwarz 2023 for the collapse discussion and Dorshow and Wills 2022 for agricultural suitability). If intentionally excluded, no action needed.

### W2. Partially verified sources cited in manuscript

Line 402 explicitly flags four sources as based on secondary characterizations rather than direct page-verified readings:

1. **Bliege Bird and Smith 2005** (no reference entry; no PDF full text)
2. **Enquist and Leimar 1983** (has INDEX entry, claims file, and summary)
3. **Trigger 1990** (no reference entry; INDEX notes PDF is partial/paywall)
4. **Roscoe 2009** (no reference entry; INDEX notes PDF is partial/screenshot)

**Action required:** Obtain full PDFs and verify claims before submission. Add reference entries for Bliege Bird and Smith 2005, Trigger 1990, and Roscoe 2009.

### W3. Potential missing citations

The following manuscript claims appear to lack supporting citations. Only clear cases are flagged.

| Line | Claim | Suggested citation |
|------|-------|--------------------|
| 22 | "Between roughly 850 and 1150 CE..." | General knowledge; acceptable without citation in introduction |
| 24 | "at least a dozen major great houses were built within the canyon, and approximately 150 outlier great houses" | The "150 outlier" count could use a citation (possibly Kantner 2003 or Lekson 2006) |
| 48 | "regional (San Juan Basin): ~55,000" (implied) | Population figure stated in CLAUDE.md but not cited in the text at this location; the paragraph cites other sources |

### W4. Mailath (1987) citation appears only in Appendix

Mailath (1987) is cited at line 643 in Appendix A for the uniqueness proof. It has a reference entry (line 515) but no INDEX entry, claims file, or summary. This is a mathematics/economics reference used for a single theorem citation, so a full claims extraction may not be necessary, but an INDEX entry should be added.

---

## Unresolved Flags

**[CITE-CHECK] flags found:** 0
**[UNVERIFIED] flags found:** 0

No formal flags are present in the manuscript. However, line 402 contains an explicit textual warning about four sources verified only from secondary characterizations (see W2 above). This serves the same function as [CITE-CHECK] flags and should be resolved before submission.

---

## Page Number Spot-Checks

Six citations with page numbers were verified against claims files. All passed.

| Citation | Manuscript page ref | Claims file | Result |
|----------|-------------------|-------------|--------|
| Gintis et al. 2001, p. 8 | Line 142 | Claim 2 (p. 8) | PASS |
| Gintis et al. 2001, pp. 12-13 | Line 142 | Claims 4-5 (pp. 12-13) | PASS |
| Kennett et al. 2017, p. 2 | Line 248 | Consistent with claims | PASS |
| Plog and Heitman 2010, p. 19622 | Line 248 | Claim 4 (p. 19622) | PASS |
| Plog and Heitman 2010, p. 19623 | Line 248 | Claim 2 (p. 19623) | PASS |
| Kantner and Vaughn 2012, p. 77 | Line 282 | Claims 11-12 (p. 77) | PASS |
| Watson et al. 2015, p. 8238 | Line 260 | Claim 1 (p. 8238) | PASS |
| Watson et al. 2015, pp. 8240-8241 | Line 260 | Claims 2-3 (pp. 8240-8241) | PASS |
| Crown 2018, p. 397 | Line 260 | Claim 4 (p. 397) | PASS |
| Crown 2018, p. 394 | Line 260 | Claims 2-3 (p. 394) | PASS |
| Crown and Wills 2018, p. 890 | Line 326 | Claim 1 (p. 890) | PASS |
| Crown and Wills 2018, p. 899 | Line 326 | Claim 4 (p. 899) | PASS |
| Van Dyke 2004, pp. 422-423 | Line 328 | Claim 3 (pp. 422-423) | PASS |
| Van Dyke 2004, p. 423 | Line 328 | Claim 2 (p. 423) | PASS |
| Mattson 2025, pp. 95, 106 | Line 260 | Claims 2, 5 (pp. 95, 106) | PASS |
| Mattson 2025, pp. 105, 107 | Line 260 | Claims 4, 7 (pp. 105, 107) | PASS |
| Lekson 2002, p. 611 | Line 284 | Claim 1 (p. 611) | PASS |
| Lekson 2002, pp. 612-613 | Line 284 | Claim 2 (pp. 612-613) | PASS |

All 18 spot-checked page number citations are consistent with claims file extractions.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Unique body citations | 71 |
| Reference list entries | 55 |
| INDEX entries | 42 |
| Claims files | 42 |
| Summary files | 42 |
| Citations missing from References section | **7** |
| Citations missing from INDEX (expected new) | 20 |
| Citations missing from INDEX (other) | 18 |
| Orphan INDEX entries (never cited) | 6 |
| [CITE-CHECK] flags | 0 |
| [UNVERIFIED] flags | 0 |
| Partially verified sources (line 402 warning) | 4 |
| Page number spot-checks performed | 18 |
| Page number spot-checks passed | 18 |
| Page number spot-checks failed | 0 |

---

## Priority Actions

1. **Add 7 missing reference entries** (C1): Bliege Bird and Smith 2005, Dean 1988, Dean 1996, Ember and Ember 1992, LeBlanc 1999, Roscoe 2009, Trigger 1990.
2. **Obtain full PDFs** for Bliege Bird and Smith 2005, Trigger 1990, Roscoe 2009, and verify claims against originals (W2).
3. **Add INDEX entries** for the 20 expected new references and the 18 other citations not yet indexed. Highest priority: Benson et al. 2019, Cook et al. 2004, Guiterman et al. 2015, Spence 1973, Grafen 1990.
4. **Fix INDEX naming:** Rename `Gillreath_Brown_et_al_2024` to `Gillreath_Brown_Kohler_2024` to match the two-author citation form (C3).
5. **Decide on orphan INDEX entries** (W1): Cite or intentionally retain as background infrastructure.
