# Feature Importance – Gini vs Permutation

> **Type:** Knowledge Reference | **Domain:** Machine Learning | **Last Updated:** 2025

---

## Overview

Feature importance quantifies how much each input variable contributes to a model's predictive power. In Random Forests, two dominant methods exist: **Gini (Mean Decrease in Impurity)** and **Permutation Importance (Mean Decrease in Accuracy)**. They answer subtly different questions and have different failure modes.

---

## Gini Importance (Mean Decrease in Impurity)

### How It Works
At each internal split in a decision tree, impurity is reduced. For classification, **Gini impurity** is:

> Gini(t) = 1 − Σ pᵢ²

where pᵢ is the proportion of class i at node t.

**Feature importance for feature X** = sum of weighted impurity reductions across all nodes where X was used to split, averaged across all trees.

### Strengths
- Computed during training — zero additional cost
- Numerically stable and fast for large datasets
- Works well when features are roughly similar in scale

### Known Biases
- **Favors high-cardinality features**: Continuous variables or those with many unique values create more potential split points → appear more "useful"
- **Correlated features**: Importance is split between correlated features, underestimating each one's true value
- **Does not use test data**: Cannot detect if the model is overfitting to spurious splits

---

## Permutation Importance

### How It Works
For a fitted model evaluated on a validation set:
1. Record baseline performance (e.g., OOB accuracy or AUC)
2. For feature X: randomly shuffle its values across all samples, breaking its relationship with the target
3. Re-evaluate performance. The drop in performance = importance of X
4. Repeat for each feature

> Importance(X) = baseline_score − score_with_X_shuffled

### Strengths
- **Model-agnostic** in principle (though here applied to RF)
- Uses out-of-sample data — reflects true generalization contribution
- Correctly handles correlated features by measuring marginal contribution

### Weaknesses
- Computationally expensive: one full prediction pass per feature × number of repeats
- **Multicollinearity issue**: If two features are highly correlated, shuffling one degrades performance less because the other compensates — both appear less important than they are

---

## Comparison Table

| Property | Gini Importance | Permutation Importance |
|---|---|---|
| Computed on | Training data | Validation / OOB data |
| Handles high cardinality | Biased (overestimates) | Unbiased |
| Correlated features | Dilutes importance | Partially compensates |
| Computational cost | Free (during training) | O(n_features × n_repeats) |
| Reflects generalization | No | Yes |
| Implementation | `rf.feature_importances_` | `sklearn.inspection.permutation_importance` |

---

## Application: Keratoconus Feature Analysis

In corneal topography datasets:
- Features like `Kmax`, `ISV`, `IVA`, `KI`, `CKI` from Pentacam often have different cardinalities
- Gini importance may overweight `Kmax` simply because it's continuous with wide range
- Permutation importance on OOB samples gives more reliable clinical insight
- Always compare both: agreement suggests robust importance; disagreement warrants investigation

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(rf_model, X_test, y_test, n_repeats=30, random_state=42)
sorted_idx = result.importances_mean.argsort()
```

---

## Best Practice

Use **Gini for quick exploration** and **Permutation for final reporting**. For publication, report permutation importance with confidence intervals across multiple repeats.
