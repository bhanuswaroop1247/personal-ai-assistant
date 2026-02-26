# Handling Class Imbalance in Clinical Data

**Type:** Knowledge Reference | **Domain:** Machine Learning – Data Engineering  
**Last Updated:** 2025

---

## Why Imbalance Is a Problem

In keratoconus severity datasets, severe cases are rare relative to normal/mild. A naive model trained on imbalanced data learns to predict the majority class, achieving high accuracy while completely failing on minority classes — the clinically critical ones.

**Example:** If 70% of samples are "Normal", a trivial classifier achieves 70% accuracy by always predicting Normal. Yet it has zero clinical utility.

---

## Diagnosing Imbalance

```python
from collections import Counter
Counter(y_train)
# Output: {'Normal': 420, 'Mild': 180, 'Moderate': 90, 'Severe': 40}
```

Imbalance ratio = majority class count / minority class count. Ratios > 4:1 warrant active intervention.

---

## Strategy 1: Resampling

### Oversampling (SMOTE)
Synthetic Minority Oversampling Technique generates synthetic samples by interpolating between existing minority instances.

```python
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)
```

- **Use when:** Small dataset, minority class has genuine intra-class structure.
- **Risk:** Can generate unrealistic synthetic samples if feature space is sparse.

### Undersampling
Randomly remove majority class samples. Fast but discards real data — only suitable with large datasets.

### SMOTEENN / SMOTETomek
Combined over + under sampling. Often outperforms either alone.

---

## Strategy 2: Class Weights

Tell the algorithm to penalize misclassification of minority classes more heavily.

```python
rf = RandomForestClassifier(class_weight='balanced', random_state=42)
```

`class_weight='balanced'` automatically computes weights inversely proportional to class frequency:
```
weight_i = n_samples / (n_classes × count_i)
```

This is the **simplest, lowest-risk intervention** and should always be tried first.

---

## Strategy 3: Threshold Adjustment

Default classification threshold is 0.5. For medical screening (high recall needed):
- Lower the threshold for the minority (disease) class → catches more true positives at cost of more false positives.
- Use ROC curve to select threshold that satisfies clinical sensitivity requirement (e.g., ≥ 90% recall for Severe KC).

```python
proba = rf.predict_proba(X_test)
# Adjust threshold for class 3 (Severe)
threshold = 0.35
y_pred_adjusted = (proba[:, 3] >= threshold).astype(int)
```

---

## Strategy 4: Evaluation Metrics

Never report accuracy alone on imbalanced data:
- **Balanced Accuracy** = mean per-class recall
- **Macro F1** = unweighted mean F1 across all classes
- **Cohen's Kappa** = accounts for expected agreement by chance
- **Per-class recall** — especially for Severe KC class

---

## Combining Strategies

Recommended pipeline for clinical KC classification:
1. Apply `class_weight='balanced'` to Random Forest.
2. Evaluate with stratified 5-fold CV using balanced accuracy.
3. If severe class recall still < 80%, apply SMOTE only on training folds (not on test data — this is a common data leakage mistake).
4. Report per-class metrics in full.

---

## Common Mistakes

- **Applying SMOTE before train/test split** → data leakage, inflated performance.
- **Oversampling test data** → invalid evaluation.
- **Using accuracy as the only metric** → misleading on imbalanced data.

---

*References: Chawla et al. (2002) "SMOTE." JAIR. | He & Garcia (2009) "Learning from Imbalanced Data." IEEE TKDE.*
