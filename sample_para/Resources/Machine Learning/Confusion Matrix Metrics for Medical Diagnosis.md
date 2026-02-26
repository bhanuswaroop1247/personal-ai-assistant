# Confusion Matrix Metrics for Medical Diagnosis

**Type:** Knowledge Reference | **Domain:** Machine Learning / Clinical Decision Support  
**Last Updated:** 2025

---

## Overview

In clinical machine learning, the confusion matrix is far more than an accuracy check — it encodes the cost of error. The stakes differ: a missed keratoconus case (false negative) leads to delayed treatment; an unnecessary referral (false positive) causes anxiety and cost. Understanding which metric to optimize is foundational.

---

## The Four Cells

For a binary classifier (e.g., Normal vs. Keratoconus):

|               | Predicted Positive | Predicted Negative |
|---------------|--------------------|--------------------|
| **Actual Positive** | TP | FN |
| **Actual Negative** | FP | TN |

In multiclass settings (e.g., Normal / Mild / Moderate / Severe KC), the confusion matrix becomes N×N, and per-class metrics are computed using one-vs-rest decomposition.

---

## Key Metrics

### Sensitivity (Recall / True Positive Rate)
```
Sensitivity = TP / (TP + FN)
```
- **Clinical relevance:** Measures how well the model catches true disease cases.
- **Prioritize when:** Missing a case is costly (screening tasks, progressive disease).
- In keratoconus grading: high recall for Severe KC is non-negotiable.

### Specificity (True Negative Rate)
```
Specificity = TN / (TN + FP)
```
- Measures avoidance of false alarms.
- Low specificity → high false positive rate → overdiagnosis.

### Precision (Positive Predictive Value)
```
Precision = TP / (TP + FP)
```
- Important when treatment carries risk or cost.
- A model with 95% recall but 40% precision floods clinicians with false referrals.

### F1 Score
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
- Harmonic mean balancing both.
- Use **weighted F1** for imbalanced multiclass problems.

### Macro vs. Weighted Averaging
- **Macro:** Treats all classes equally — poor if class frequencies differ widely.
- **Weighted:** Weights by support per class — better for imbalanced keratoconus severity distributions (Mild >> Severe in real data).

---

## Interpreting Off-Diagonal Errors

In multiclass KC grading, the most actionable errors are:
- **Severe misclassified as Moderate:** Dangerous — delays intervention.
- **Normal misclassified as Mild:** Causes over-referral but less harm.
- **Non-adjacent errors** (e.g., Normal → Severe): Should be near zero; if not, review feature overlap or data leakage.

Ordinal confusion (off-by-one) is inherently less dangerous than non-ordinal confusion. Reporting both is good practice in a clinical paper.

---

## Reporting Standards for Publications

When writing a paper on KC classification:
1. Report the full confusion matrix (not just accuracy).
2. Report per-class precision, recall, F1.
3. Justify metric choice relative to clinical cost.
4. Compare against chance-level baseline (e.g., majority class classifier).
5. Use McNemar's test or DeLong's test when comparing two classifiers.

---

## Practical Notes

- Sklearn's `classification_report()` gives per-class and averaged metrics — always run this alongside the confusion matrix.
- For highly imbalanced data, consider **balanced accuracy** = mean(per-class recall).
- ROC-AUC is threshold-independent; prefer it for comparing models, not for final clinical threshold decisions.

---

*Reference: Fawcett (2006) "An introduction to ROC analysis." Pattern Recognition Letters.*
