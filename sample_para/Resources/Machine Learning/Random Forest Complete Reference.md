# Random Forest – Complete Reference Note

**Resource:** Machine Learning  
**Type:** Knowledge building block  
**Last Updated:** 2025-01

---

## Conceptual Foundation

### Decision Trees (Building Block)
A single decision tree partitions feature space through recursive binary splits. Each internal node asks: "Is feature X ≤ threshold t?" Leaves contain class predictions. Fully grown trees have very low bias but extremely high variance — they memorize training data.

### Bagging (Bootstrap AGGregating)
Train B trees, each on a different bootstrap sample (n samples drawn *with replacement* from training data). Average their predictions. Key insight: averaging many high-variance, low-bias predictors reduces variance dramatically while maintaining low bias.

**Why it works:** If individual trees have error rate ε and are independent, the ensemble error drops as O(1/B). Trees are never fully independent (they share data), but are decorrelated enough to see significant variance reduction.

### Random Feature Selection (Extra Decorrelation)
At each node, consider only a random subset of √p features (where p = total features). This further decorrelates trees — without it, all trees tend to use the same strong features and remain correlated.

---

## Key Properties

| Property | Behavior |
|----------|----------|
| Bias | Similar to a single deep tree (low) |
| Variance | Much lower than single tree |
| Overfitting | Does not overfit with more trees |
| Feature scaling | Not required (tree-based splits) |
| Missing values | Cannot handle natively (must impute) |
| Interpretability | Low (ensemble), but feature importance available |
| Training speed | Parallelizable across trees |

---

## Out-of-Bag Error

Each bootstrap sample uses ~63.2% of data. The remaining ~36.8% (OOB) provide a natural validation estimate without a separate test set. This is statistically equivalent to k≈3 fold CV, but with no extra computation overhead. Practically equivalent to 5-fold for n > 1000.

**Set `oob_score=True` always in scikit-learn RF.**

---

## Feature Importance: Gini vs. Permutation

| Type | Mechanism | Bias | Recommended Use |
|------|-----------|------|-----------------|
| Gini MDI | Sum of impurity reduction | Biased toward high-cardinality features | Fast screening |
| Permutation | Drop in score when feature shuffled | Unbiased | Model-agnostic validation |
| SHAP | Game-theoretic contribution | Consistent | Individual predictions |

**Best practice:** Use Gini for speed, validate top features with permutation importance. If rankings agree, trust the result.

---

## Scikit-learn Cheat Sheet

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=300,       # More = lower variance, no overfitting
    max_features='sqrt',    # Best for classification
    max_depth=None,         # Fully grown = lowest bias
    min_samples_leaf=1,     # Increase to reduce overfitting if needed
    class_weight='balanced',# For imbalanced datasets
    oob_score=True,         # Always enable
    n_jobs=-1,              # Use all CPU cores
    random_state=42
)

rf.fit(X_train, y_train)
print(f"OOB Accuracy: {rf.oob_score_:.3f}")

# Feature importance
import pandas as pd
imp = pd.Series(rf.feature_importances_, index=feature_names).sort_values(ascending=False)
```

---

## Comparison with Alternatives

| Model | Advantage over RF | Disadvantage vs. RF |
|-------|------------------|---------------------|
| XGBoost | Often better performance on tabular data | Less robust to hyperparameters; slower tuning |
| SVM | Better in high-dimensional spaces | Doesn't scale to large datasets; no natural importance |
| Logistic Regression | Fully interpretable | Limited to linear decision boundaries |
| Neural Network | Models complex non-linear functions | Needs much more data; no feature importance |

**RF sweet spot:** Tabular data, moderate size (n: 100–100k), need for interpretability, limited tuning budget.

