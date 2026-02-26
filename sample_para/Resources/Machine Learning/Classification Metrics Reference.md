# Evaluation Metrics for Classification – Reference

**Resource:** Machine Learning  
**Type:** Knowledge building block  
**Last Updated:** 2025-01

---

## Confusion Matrix Anatomy

For binary classification:

```
              Predicted Positive   Predicted Negative
Actual Pos:       TP                    FN
Actual Neg:       FP                    TN
```

**True Positive (TP):** Correctly identified positive  
**False Positive (FP):** Negative incorrectly labeled as positive (Type I error)  
**False Negative (FN):** Positive missed (Type II error) — often the more costly error  
**True Negative (TN):** Correctly identified negative  

---

## Core Metrics

```
Accuracy    = (TP + TN) / (TP + TN + FP + FN)
Precision   = TP / (TP + FP)       → of predicted positives, how many are real?
Recall      = TP / (TP + FN)       → of actual positives, how many did we catch?
F1          = 2 * (P * R) / (P + R) → harmonic mean of precision and recall
Specificity = TN / (TN + FP)       → recall for negative class
```

### When to Use What

| Metric | Use When |
|--------|----------|
| Accuracy | Balanced classes, no asymmetric costs |
| Precision | FP is costly (spam filter: false alarms annoying) |
| Recall | FN is costly (disease detection: missing cases dangerous) |
| F1 | Imbalanced data, balanced FP/FN concern |
| AUC-ROC | Ranking quality, threshold-agnostic evaluation |
| AUC-PR | Highly imbalanced data (positive class rare) |

---

## Multi-Class Extensions

### Macro vs. Weighted Averaging
```python
from sklearn.metrics import classification_report

report = classification_report(y_true, y_pred, 
         target_names=['Normal', 'Mild', 'Moderate', 'Severe'])
```

- **Macro:** Unweighted mean across classes — detects poor minority class performance
- **Weighted:** Weighted by support (class size) — reflects real-world performance
- **Micro:** Global TP/FP/FN sum — equivalent to accuracy for balanced datasets

### One-vs-Rest AUC-ROC
For multi-class:
```python
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import label_binarize

y_bin = label_binarize(y_test, classes=[0,1,2,3])
auc = roc_auc_score(y_bin, y_prob, multi_class='ovr', average='macro')
```

---

## The Precision-Recall Tradeoff

Adjusting the classification threshold moves precision and recall inversely:
- Lower threshold → more positives predicted → recall ↑, precision ↓
- Higher threshold → fewer positives predicted → precision ↑, recall ↓

**For clinical applications:** Set threshold to guarantee minimum recall for dangerous classes, then optimize precision given that constraint.

```python
from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_true, y_score)
# Find threshold where recall >= 0.90
min_recall_threshold = thresholds[np.where(recall[:-1] >= 0.90)[0][-1]]
```

---

## AUC-ROC Interpretation

| AUC | Meaning |
|-----|---------|
| 1.0 | Perfect classifier |
| 0.9–1.0 | Excellent |
| 0.8–0.9 | Good |
| 0.7–0.8 | Fair |
| 0.5 | Random (no discriminative power) |
| < 0.5 | Worse than random (check label encoding) |

---

## Calibration

A well-calibrated model: if it predicts P(positive) = 0.7 for 100 samples, ~70 should be positive.

```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)
plt.plot(prob_pred, prob_true, 's-', label='RF')
plt.plot([0,1], [0,1], 'k--', label='Perfect calibration')
```

Random Forests often need isotonic regression or Platt scaling for well-calibrated probabilities.

