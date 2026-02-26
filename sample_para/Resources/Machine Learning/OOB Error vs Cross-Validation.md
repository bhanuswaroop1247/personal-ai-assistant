# OOB Error vs Cross-Validation: When to Use Each

**Type:** Knowledge Reference | **Domain:** Machine Learning – Model Evaluation  
**Last Updated:** 2025

---

## What Is Out-of-Bag Error?

Random Forest trains each decision tree on a **bootstrap sample** (~63.2% of training data). The remaining ~36.8% of samples — not seen by that tree — are the **out-of-bag (OOB)** samples.

For each training instance, predictions are aggregated only from trees that did **not** see it. This produces an unbiased error estimate without needing a separate validation set.

```
OOB Error Rate = (# misclassified OOB samples) / (total training samples)
```

---

## OOB Error vs. K-Fold Cross-Validation

| Property | OOB Error | K-Fold CV |
|---|---|---|
| Requires extra data split | No | Yes |
| Computationally free | Yes (computed during training) | No (k separate training runs) |
| Works with any model | No (RF-specific) | Yes |
| Variance of estimate | Slightly higher | Lower with higher k |
| Typical use | RF hyperparameter tuning, quick validation | Final model evaluation, any estimator |

### Key Insight
OOB error tends to slightly **overestimate** true test error because each tree only uses ~63% of data (vs. (k-1)/k in k-fold). For small datasets (< 500 samples), this bias can matter.

---

## When to Rely on OOB Error

1. **During Random Forest hyperparameter tuning:** Adjusting `n_estimators`, `max_features`, `max_depth` — OOB error gives near-instant feedback.
2. **When data is limited:** Avoids losing a validation set entirely.
3. **For feature importance stability checks:** Track OOB error as features are added/removed.
4. **Quick sanity checks:** If OOB error >> test error, suspect data leakage.

### Code Reference
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=200, oob_score=True, random_state=42)
rf.fit(X_train, y_train)
print(f"OOB Accuracy: {rf.oob_score_:.4f}")
print(f"OOB Error:    {1 - rf.oob_score_:.4f}")
```

---

## When to Use K-Fold CV Instead

1. **Final model evaluation** — publish CV results for reproducibility.
2. **Comparing RF vs. other classifiers** (SVM, XGBoost) — fair common ground.
3. **Nested CV for combined hyperparameter search + evaluation.**
4. **Small datasets** — 5-fold or 10-fold provides better bias–variance balance.

### Stratified K-Fold for Imbalanced Classes
When KC severity classes are imbalanced, always use `StratifiedKFold` to ensure each fold preserves class proportions:
```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(rf, X, y, cv=skf, scoring='balanced_accuracy')
```

---

## Common Mistake to Avoid

**Do not report OOB error as your final published test performance.** OOB is a training-time estimate. Always hold out a true test set (or use nested CV) for the final performance claim in a paper.

---

## Summary Rule of Thumb

> Use OOB error during development and tuning. Use K-fold CV (stratified) for evaluation and publication.

---

*References: Breiman (2001) "Random Forests." Machine Learning. | Hastie, Tibshirani, Friedman – Elements of Statistical Learning, Ch. 7 & 15.*
