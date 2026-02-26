# Random Forest: Deep Concepts Reference

**Type:** Knowledge Reference | **Domain:** Machine Learning – Ensemble Methods  
**Last Updated:** 2025

---

## Core Mechanism

Random Forest is a **bagging ensemble** of decision trees, with an added randomization layer: at each split, only a random subset of features (`max_features`) is considered. This de-correlates trees, reducing variance without increasing bias.

**Two sources of randomization:**
1. **Bootstrap sampling** — each tree trains on a different resample of the training data.
2. **Feature subsampling** — each split considers only `sqrt(n_features)` (classification default) or `n_features/3` (regression default) features.

---

## Key Hyperparameters and Their Effects

| Parameter | Effect | Default | Tuning Direction |
|---|---|---|---|
| `n_estimators` | More trees → lower variance, diminishing returns after ~200 | 100 | Increase until OOB stabilizes |
| `max_features` | Lower → more diverse trees, more bias | sqrt(p) | Try log2(p), 0.5*p |
| `max_depth` | Shallower → more regularization | None (full) | Grid search 5–30 |
| `min_samples_leaf` | Higher → smoother decision boundaries | 1 | Try 2–10 for noisy data |
| `class_weight` | Adjust for imbalanced classes | None | Use 'balanced' |

---

## Why Random Forests Work: Bias–Variance Decomposition

Individual deep trees have **low bias** but **high variance** — they overfit. Averaging N uncorrelated trees:

```
Variance(ensemble) = ρ × σ² + (1-ρ)/N × σ²
```

Where ρ = correlation between trees, σ² = individual tree variance.

- Increasing `n_estimators` reduces the second term.
- Reducing `max_features` reduces ρ (tree correlation) — the key innovation.

---

## Feature Importance: Gini Impurity Decrease

At each split in each tree, the weighted Gini impurity decrease is computed:

```
ΔGini = Gini(parent) - [w_left × Gini(left) + w_right × Gini(right)]
```

Feature importance for feature j = mean ΔGini across all splits on j, across all trees, normalized to sum to 1.

**Limitations of Gini importance:**
- Biased toward high-cardinality continuous features.
- Can inflate importance of correlated features.
- Does not indicate direction of effect (unlike SHAP).

**When to use Gini vs. Permutation Importance:**
- Use Gini for fast initial screening.
- Use permutation importance (or SHAP) for final publication — more reliable, less biased.

---

## Proximity Matrix

Each pair of training samples accumulates a count of how often they land in the same leaf. Normalized by number of trees → **proximity matrix**.

Uses:
- Outlier detection (low proximity to all other samples → potential outlier)
- Imputation of missing values
- Visualization (MDS on proximity distances)

---

## Extrapolation Limitation

Random Forests cannot extrapolate beyond the range of training data. All predictions are weighted averages of training leaf values. For KC grading with novel extreme measurements, this can cause underestimation at distribution tails.

---

## Parallelism

Trees are trained independently → embarrassingly parallel. Use `n_jobs=-1` in sklearn to use all CPU cores.

```python
rf = RandomForestClassifier(n_estimators=500, n_jobs=-1, oob_score=True)
```

---

*References: Breiman (2001). | Louppe et al. (2013) "Understanding Variable Importances in Forests of Randomized Trees." NeurIPS.*
