# Literature Review Summary – Keratoconus Severity Classification

**Project:** Keratoconus Severity Model – Paper Submission  
**Last Updated:** 2025-01  
**Status:** Active – compiling references for Methods section

---

## Key Problem Statement

Keratoconus (KCN) is a progressive corneal ectasia causing irregular astigmatism and thinning of the corneal stroma. Clinical grading systems (Amsler-Krumeich, ABCD, Belin-Ambrosio) rely on subjective or single-parameter metrics. A data-driven, multi-feature classifier can offer more reproducible and granular staging.

---

## Existing Classification Approaches

### Traditional Grading Systems
- **Amsler-Krumeich (AK):** Grades I–IV based on mean keratometry, corneal scarring, and MRSE. Widely used clinically but not data-driven.
- **ABCD Grading (Belin-Ambrosio):** Uses anterior radius (A), posterior radius (B), corneal thickness (C), and CDVA (D). More holistic but still linear thresholds.

### Machine Learning Approaches in Literature
| Study | Method | Dataset | Accuracy |
|-------|--------|---------|----------|
| Smadja et al. (2013) | Linear discriminant analysis | Orbscan II | 88.6% |
| Kovacs et al. (2016) | SVM with Scheimpflug data | Pentacam | 91.3% |
| Issarti et al. (2019) | Logistic Regression | Corvis ST | 90.2% |
| Kamiya et al. (2019) | Random Forest | Pentacam + OPD | **94.8%** |

### Gaps in Literature
- Most studies use binary classification (KCN vs. normal); multi-class severity grading is underexplored.
- Feature importance and interpretability rarely addressed.
- Few studies use OOB error as a model tuning signal.
- Limited use of confusion matrix recall analysis per grade.

---

## Key Topographic Features Referenced

- **Km (mean keratometry):** Strong predictor in all studies
- **Belin-Ambrosio Deviation (BAD-D):** Composite score, high sensitivity
- **Thinnest Corneal Location (TCT):** Location shift indicative of ectasia
- **Anterior float (BFS-based):** Correlates with cone apex elevation
- **Posterior elevation:** Often the earliest sign of subclinical KCN
- **SRAX index:** Asymmetry index, useful for early detection

---

## Papers to Read Next
- [ ] Saad & Gatinel (2010) – Topographic features in subclinical KCN
- [ ] Arbelaez et al. (2012) – Neural network on Sirius topographer data
- [ ] Ferreira et al. (2020) – Deep learning on OCT data for KCN staging

---

## Notes for Methods Section

Cite Kamiya et al. as closest to our approach. Differentiate by emphasizing:
1. Our use of Gini importance vs. permutation importance
2. Grade-level recall breakdown via confusion matrix
3. OOB error as a proxy for generalization without separate test set

