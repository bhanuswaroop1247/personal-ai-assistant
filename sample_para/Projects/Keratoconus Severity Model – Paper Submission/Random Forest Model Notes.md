# Random Forest Model Notes – Keratoconus Severity Classification

**Project:** Keratoconus Severity Model – Paper Submission  
**Last Updated:** 2025-01  
**Status:** Model tuned, evaluation in progress

---

## Model Architecture

### Target Variable
- **Classes:** 4 (Normal, Mild KCN, Moderate KCN, Severe KCN)
- **Encoding:** 0 = Normal, 1 = Mild, 2 = Moderate, 3 = Severe

### Input Features (n=18)
Derived from Pentacam HR topography:
- Km_flat, Km_steep, Km_mean
- BAD-D, BAD_A, BAD_B
- TCT (thinnest corneal thickness, µm)
- Anterior float BFS, Posterior float BFS
- SRAX, KI (keratoconus index)
- ISV (index of surface variance)
- Pachymetry progression index (PPI_min, PPI_max)
- KISA%, D-index
- Age, BCVA (logMAR)

### Hyperparameters (Current Best)
```python
RandomForestClassifier(
    n_estimators=300,
    max_depth=None,       # fully grown trees
    min_samples_split=4,
    min_samples_leaf=2,
    max_features='sqrt',  # sqrt(18) ≈ 4 features per split
    class_weight='balanced',  # corrects class imbalance
    oob_score=True,
    random_state=42
)
```

---

## Training Protocol

- **Dataset size:** 412 eyes (103 Normal, 97 Mild, 112 Moderate, 100 Severe)
- **Validation strategy:** OOB score as primary validation metric (no separate test set needed for RF)
- **Cross-validation:** 5-fold stratified CV as secondary check
- **Preprocessing:** StandardScaler applied (important for feature comparison, not for RF split decisions, but useful for model comparison later)

---

## Current Performance (OOB-based)

| Metric | Value |
|--------|-------|
| OOB Accuracy | 91.3% |
| Macro F1 | 0.89 |
| Weighted F1 | 0.91 |
| Best class recall | Severe (0.96) |
| Worst class recall | Mild (0.83) |

**Key observation:** Mild KCN is consistently confused with Normal and Moderate. This matches clinical reality – the mild grade is a transitional state.

---

## Hyperparameter Tuning Notes

### n_estimators
- Tested: 100, 200, 300, 500
- OOB error stabilizes around 250–300 trees
- Beyond 300 → diminishing returns, increased computation

### max_depth
- Restricting to 10 → underfitting (OOB drops ~4%)
- Unrestricted → best OOB performance; no overfitting risk in RF due to bagging

### max_features
- `'sqrt'` outperforms `'log2'` and `'auto'` on this dataset
- Hypothesis: With correlated topographic features, restricting more aggressively helps decorrelate trees

---

## TODO
- [ ] Run permutation importance as sanity check against Gini
- [ ] Test SHAP values for individual prediction explanation
- [ ] Try XGBoost for comparison section in paper
- [ ] Add learning curve plot (training vs. OOB error vs. n_estimators)

