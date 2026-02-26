# Research Paper Structure Blueprint

**Type:** Knowledge Reference | **Domain:** Writing & Content Ideas  
**Last Updated:** 2025

---

## Overview

This document is a reusable template and decision guide for structuring a machine learning / clinical research paper. Applicable to keratoconus classification, medical imaging, and applied ML domains.

---

## IMRaD Structure

The standard for most scientific journals:

| Section | Function | Typical Word Count |
|---|---|---|
| Abstract | Standalone summary | 200–300 |
| Introduction | Problem, gap, contribution | 400–700 |
| Methods | Reproducible procedure | 600–1000 |
| Results | What you found (no interpretation) | 500–800 |
| Discussion | Interpretation, comparison, limitations | 600–900 |
| Conclusion | Main takeaways, future work | 150–250 |

---

## Abstract Formula (Structured)

Use the AIM format for medical/clinical ML:
1. **Background:** What clinical problem motivates this work?
2. **Purpose/Objective:** What did you aim to do?
3. **Methods:** Dataset, model, evaluation.
4. **Results:** Primary metric (e.g., "Weighted F1 = 0.91").
5. **Conclusion:** Clinical utility and implications.

---

## Introduction Architecture

### Paragraph 1 — Clinical Context
- What is keratoconus? Why does grading matter? What is the consequence of misclassification?
- End with a statement of clinical need: "Current grading systems rely on...which requires...This limits..."

### Paragraph 2 — State of the Art
- What ML approaches have been tried? What gaps exist?
- Cite 4–6 seminal papers.
- Identify the specific gap you address.

### Paragraph 3 — Contribution Statement
Be specific and enumerable:
> "In this study, we (1) propose a Random Forest classifier for four-class keratoconus grading, (2) analyze feature importance using Gini impurity and permutation methods, and (3) evaluate performance with focus on clinically critical recall for severe cases."

---

## Methods Section Checklist

- [ ] Dataset description: source, inclusion/exclusion criteria, demographic summary
- [ ] Feature extraction: which Pentacam parameters, how derived
- [ ] Class distribution: counts per class (table)
- [ ] Preprocessing: normalization, handling missing data
- [ ] Model: algorithm, key hyperparameters, rationale
- [ ] Evaluation: train/test split, cross-validation strategy, metrics used
- [ ] Statistical analysis: significance testing if comparing models

---

## Results Section Rules

- **Do not interpret in Results** — reserve interpretation for Discussion.
- Lead with the most important finding (overall performance).
- Report confusion matrix AND per-class metrics.
- Use a table for metric comparison; use figure for confusion matrix.
- Report OOB or CV error alongside test error.

---

## Discussion Architecture

1. **Restate primary finding** — "The Random Forest model achieved 91% weighted F1..."
2. **Compare to prior work** — benchmark against state of the art.
3. **Explain unexpected results** — e.g., why Moderate class had lower recall.
4. **Clinical interpretation** — what does this mean for practice?
5. **Limitations** — dataset size, generalizability, external validation.
6. **Future directions** — prospective validation, additional features, real-time integration.

---

## Figure Design Principles

- Confusion matrices: use color scale (sequential, not diverging unless showing deviation).
- Feature importance: horizontal bar chart, sorted by importance.
- All figures: minimum 300 DPI for publication; label axes; include units.

---

*Reference: Turk et al. (2012) "How to Write a Great Research Paper." | CONSORT/STROBE reporting guidelines for clinical studies.*
