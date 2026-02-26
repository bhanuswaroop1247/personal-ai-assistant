# OOB Error Analysis – Random Forest Tuning

**Project:** Keratoconus Severity Model – Paper Submission  
**Last Updated:** 2025-01  
**Purpose:** Track OOB error behavior across hyperparameter configurations

---

## What is OOB Error?

In a Random Forest, each tree is trained on a bootstrap sample (~63.2% of the training data). The remaining ~36.8% of samples — called **out-of-bag (OOB) samples** — are used to evaluate that tree's predictions.

**Aggregating OOB predictions** across all trees gives an unbiased estimate of generalization error without requiring a separate validation set. This is one of Random Forest's most powerful built-in features.

```
OOB Error = 1 - OOB Accuracy
OOB Accuracy = (correct OOB predictions) / (total OOB predictions)
```

---

## Why OOB Error Matters for This Project

- Our dataset is relatively small (n=412 eyes)
- Losing a 20% validation split would reduce training data significantly
- OOB error effectively gives us a "free" leave-one-out approximation
- Literature precedent: Breiman (2001) validated OOB as reliable generalization estimate

---

## OOB Error vs. n_estimators

| n_estimators | OOB Error |
|-------------|-----------|
| 50          | 0.119     |
| 100         | 0.098     |
| 150         | 0.091     |
| 200         | 0.088     |
| 250         | 0.087     |
| 300         | **0.087** |
| 400         | 0.087     |
| 500         | 0.087     |

**Conclusion:** OOB error plateaus at ~300 trees. Chosen `n_estimators=300` as optimal. This is the "elbow point" — further trees add computation without reducing error.

---

## OOB Error vs. max_depth

| max_depth | OOB Error | Notes |
|-----------|-----------|-------|
| 5         | 0.143     | Underfitting – model too shallow |
| 8         | 0.112     | Moderate underfitting |
| 12        | 0.093     | Good but not optimal |
| None      | **0.087** | Fully grown trees – best performance |

**Analysis:** With `class_weight='balanced'` compensating for minor class imbalance, unrestricted depth gives the best OOB score. RF's ensemble averaging prevents overfitting even with deep trees.

---

## OOB vs. 5-Fold CV Comparison

| Metric | OOB Estimate | 5-Fold CV |
|--------|-------------|-----------|
| Accuracy | 91.3% | 90.8% ± 1.2% |
| Macro F1 | 0.890 | 0.884 ± 0.018 |

The two estimates are closely aligned. This validates that OOB is a reliable proxy for CV in our setting. Minor differences are due to bootstrap sampling variance.

---

## Interpretation for Paper

> "The model was tuned using the OOB error estimate inherent to Random Forest ensembles, which provides an unbiased generalization estimate comparable to k-fold cross-validation. OOB error stabilized at n_estimators = 300 (OOB accuracy = 91.3%), consistent with independent 5-fold CV results (90.8%), validating the selected hyperparameter configuration."

---

## Code Snippet

```python
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

oob_errors = []
n_range = range(10, 501, 10)

for n in n_range:
    rf = RandomForestClassifier(n_estimators=n, oob_score=True, random_state=42)
    rf.fit(X_train, y_train)
    oob_errors.append(1 - rf.oob_score_)

plt.plot(list(n_range), oob_errors)
plt.xlabel("n_estimators")
plt.ylabel("OOB Error")
plt.title("OOB Error vs. Number of Trees")
plt.axvline(x=300, linestyle='--', color='red', label='Selected: 300')
plt.legend()
plt.savefig("oob_error_curve.png", dpi=150)
```

