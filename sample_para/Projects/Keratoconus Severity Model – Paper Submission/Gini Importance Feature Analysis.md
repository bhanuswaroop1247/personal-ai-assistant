# Gini Importance – Feature Analysis

**Project:** Keratoconus Severity Model – Paper Submission  
**Last Updated:** 2025-01  
**Purpose:** Document and interpret Gini-based feature importance, compare with permutation importance

---

## What is Gini Importance?

Also called **Mean Decrease in Impurity (MDI)**. For each feature, Gini importance is the sum of impurity reductions (weighted by the number of samples passing through the node) across all trees in the forest.

**Formula (per feature j):**
```
Importance(j) = Σ_trees Σ_nodes [w_node * ΔImpurity(node)] where split is on feature j
```

Where:
- `w_node = (samples at node) / (total samples)`
- `ΔImpurity = impurity_parent - (left_weight * impurity_left) - (right_weight * impurity_right)`
- For classification: Gini impurity = 1 - Σ p_k²

---

## Feature Importances (Current Model, sorted)

| Rank | Feature | Gini Importance | Permutation Importance |
|------|---------|----------------|----------------------|
| 1 | BAD-D | 0.187 | 0.176 |
| 2 | Km_mean | 0.154 | 0.148 |
| 3 | TCT | 0.141 | 0.139 |
| 4 | Posterior float BFS | 0.112 | 0.118 |
| 5 | KI | 0.089 | 0.084 |
| 6 | ISV | 0.072 | 0.069 |
| 7 | KISA% | 0.063 | 0.071 |
| 8 | BAD_B | 0.051 | 0.042 |
| 9 | Anterior float BFS | 0.038 | 0.044 |
| 10 | SRAX | 0.031 | 0.038 |
| 11–18 | (age, BCVA, PPI, etc.) | < 0.025 each | < 0.020 each |

**Total importance sums to 1.000 (normalized)**

---

## Observations & Clinical Validation

### Top 3 Features
1. **BAD-D (Belin-Ambrosio Deviation):** Composite score integrating anterior/posterior elevations and pachymetry. Its top ranking is clinically expected – it was specifically designed as a KCN discriminator.

2. **Km_mean (mean keratometry):** Central corneal steepening is the hallmark of KCN. Strong monotonic relationship with severity grade.

3. **TCT (Thinnest Corneal Thickness):** Progressive thinning is a diagnostic criterion in all major grading systems.

### Agreement Between Gini and Permutation Importance
- Spearman rank correlation between both rankings: **ρ = 0.94** (strong agreement)
- Small deviations in KISA% and posterior float BFS – likely due to feature correlation artifacts in Gini

### Known Limitation of Gini Importance
Gini MDI has a known bias toward **high-cardinality continuous features** — they get more split opportunities. For our dataset, this is partially addressed because most features have similar ranges. However, `age` (wide range) shows slightly inflated Gini importance compared to permutation importance.

---

## Low-Importance Features – Removal Candidates

Features with Gini importance < 0.020:
- Age (0.019)
- BCVA logMAR (0.016)
- PPI_max (0.014)

**Recommendation:** Test model with these 3 features removed. If OOB accuracy drops < 0.5%, remove them to reduce dimensionality and improve interpretability.

---

## Code

```python
import pandas as pd
import matplotlib.pyplot as plt

importances = pd.Series(rf.feature_importances_, index=feature_names)
importances.sort_values(ascending=True).plot(kind='barh', figsize=(8, 6), color='steelblue')
plt.title('Gini Feature Importances – Keratoconus RF')
plt.xlabel('Mean Decrease in Impurity')
plt.tight_layout()
plt.savefig('gini_importances.png', dpi=150)
```

---

## Conclusion for Paper

> "BAD-D, Km_mean, and TCT collectively accounted for 48.2% of total feature importance, consistent with their established clinical significance in keratoconus grading. High agreement between Gini-based and permutation-based importance rankings (ρ = 0.94) supports the robustness of these feature selections."

