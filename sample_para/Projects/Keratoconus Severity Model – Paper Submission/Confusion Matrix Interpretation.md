# Confusion Matrix Interpretation – Recall Focus

**Project:** Keratoconus Severity Model – Paper Submission  
**Last Updated:** 2025-01  
**Purpose:** Interpret per-class confusion matrix, prioritize recall analysis for clinical relevance

---

## Why Recall is the Priority Metric

In clinical keratoconus staging, the **cost of a false negative is asymmetric:**

- Classifying a **Moderate KCN as Mild** → patient may receive inappropriate conservative treatment → risk of progression and vision loss
- Classifying **Severe KCN as Moderate** → delayed surgical referral (corneal crosslinking, PKP) → irreversible damage

**Therefore, we optimize recall per class over precision or overall accuracy.**

> Recall (Sensitivity) = TP / (TP + FN)  
> Maximizing recall = minimizing false negatives for each grade

---

## Confusion Matrix (Current Model, n_test = 83)

```
                 Predicted
                 Normal  Mild  Moderate  Severe
Actual Normal  [  21      1       0        0  ]
       Mild    [   2     16       3        0  ]
       Moderate[   0      2      22        2  ]
       Severe  [   0      0       1       13  ]
```

---

## Per-Class Metrics

| Class    | TP | FN | FP | Recall | Precision | F1   |
|----------|----|----|-----|--------|-----------|------|
| Normal   | 21 | 1  | 2   | 0.955  | 0.913     | 0.933|
| Mild     | 16 | 5  | 3   | 0.762  | 0.842     | 0.800|
| Moderate | 22 | 4  | 4   | 0.846  | 0.846     | 0.846|
| Severe   | 13 | 1  | 2   | 0.929  | 0.867     | 0.897|

**Macro Recall:** 0.873  
**Weighted Recall:** 0.880

---

## Clinical Interpretation of Errors

### Mild KCN – Worst Recall (0.762)
- 2 misclassified as Normal → **Critical error** – subclinical patients miss monitoring
- 3 misclassified as Moderate → less severe but still a misclassification
- **Action:** Review feature thresholds for Mild class. Consider oversampling Mild grade (SMOTE) or adding Mild-specific features (SRAX, corneal asymmetry index)

### Moderate KCN – Moderate Recall (0.846)
- 2 misclassified as Mild → clinical underestimation
- 2 misclassified as Severe → over-referral (less dangerous, but resource-costly)

### Severe KCN – Strong Recall (0.929)
- 1 misclassified as Moderate
- Good performance – model correctly identifies advanced cases

### Normal – Strongest Recall (0.955)
- 1 normal misclassified as Mild → false positive, leads to unnecessary monitoring

---

## Visualization Plan for Paper

1. **Heatmap confusion matrix** (normalized by actual class)
2. **Per-class recall bar chart** with clinical threshold line (e.g., 0.85 minimum acceptable recall)
3. **ROC-OVR curves** (One-vs-Rest) for each class

```python
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal','Mild','Moderate','Severe'])
disp.plot(cmap='Blues', colorbar=False, normalize='true')
plt.title('Normalized Confusion Matrix – Keratoconus Severity RF')
plt.savefig('confusion_matrix_normalized.png', dpi=150, bbox_inches='tight')
```

---

## Key Conclusion for Discussion Section

> "The model demonstrated clinically acceptable recall for Normal (0.955) and Severe (0.929) grades. The Mild keratoconus class exhibited the lowest recall (0.762), consistent with the inherent ambiguity of transitional grade boundaries. Future work should focus on improving Mild-grade sensitivity through feature engineering and class-balanced sampling strategies."

