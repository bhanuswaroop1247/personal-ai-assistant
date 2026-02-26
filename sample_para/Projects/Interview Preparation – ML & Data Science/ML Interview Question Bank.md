# ML Interview Question Bank – Core Topics

**Project:** Interview Preparation – ML & Data Science  
**Last Updated:** 2025-01  
**Format:** Question → Crisp answer + depth notes  
**Target:** Data Scientist / Applied ML roles

---

## Random Forest – Deep Questions

**Q: How does a Random Forest reduce overfitting?**
> Bagging (bootstrap aggregating) trains each tree on a different random sample of data. Random feature subsets at each split (`max_features='sqrt'`) decorrelate trees. Averaging predictions of many high-variance, low-bias trees reduces overall variance without increasing bias.

**Q: What is OOB error and why is it useful?**
> Each tree in RF is trained on ~63.2% of data (one bootstrap sample). The remaining ~36.8% (out-of-bag samples) are used to evaluate that tree. Aggregating OOB predictions gives an unbiased generalization estimate without needing a separate validation set — statistically equivalent to k-fold CV for large forests.

**Q: How does increasing n_estimators affect bias and variance?**
> More trees reduce variance (ensemble averaging), have no effect on bias, and never cause overfitting. Error decreases monotonically until convergence (the "elbow"). Memory and compute increase linearly.

**Q: Gini impurity vs. entropy — when does it matter?**
> Both measure class purity. Gini is computationally cheaper (no log). Entropy is slightly more balanced for equal distributions. In practice, performance difference is negligible; Gini is default and preferred for speed.

---

## Classification Metrics

**Q: When do you prefer recall over precision?**
> When false negatives are more costly than false positives. Medical diagnosis: missing a disease (FN) is worse than flagging a healthy patient (FP). Fraud detection: missing fraud (FN) is worse than investigating a legitimate transaction (FP).

**Q: What does a macro vs. weighted F1 tell you?**
> Macro F1: treats all classes equally — good for detecting poor performance on minority classes. Weighted F1: weights by class frequency — better reflects overall system performance in imbalanced settings. If macro << weighted, the model is struggling on rare classes.

**Q: How do you handle class imbalance?**
Options ranked by effectiveness in practice:
1. `class_weight='balanced'` — simplest, often sufficient
2. SMOTE — synthetic oversampling; risk of overfitting to synthetic examples
3. Undersampling majority class — loses information
4. Threshold tuning — adjust decision boundary post-training
5. Use AUC-ROC instead of accuracy as the primary metric

---

## Model Selection & Validation

**Q: What's the difference between validation set and test set?**
> Validation set: used during model development to tune hyperparameters. Test set: held out entirely until final evaluation; used once. Using the test set multiple times leaks information and produces overly optimistic estimates.

**Q: K-fold CV vs. leave-one-out CV — tradeoffs?**
> LOOCV: unbiased but very high variance estimate; computationally expensive. K-fold (k=5 or 10): good bias-variance balance for validation error estimate. For small datasets (n < 500): k=10 or LOOCV preferred.

**Q: What is data leakage?**
> Any information from outside the training data that informs the model improperly. Examples: scaling on full dataset before split, using future features in time series, target encoding without proper CV. Always fit preprocessing pipelines on training data only.

---

## Feature Engineering

**Q: How do you handle correlated features?**
> For linear models: remove correlated features (VIF analysis). For RF: correlated features reduce importance of each individual feature (importance gets split), but model performance is usually unaffected. Use permutation importance (less biased than Gini for correlated features).

**Q: What is the curse of dimensionality?**
> As dimensions increase, data becomes sparse — distance metrics lose meaning, volume grows exponentially. KNN, kernel methods suffer most. Tree-based methods are relatively immune due to axis-aligned splits.

---

## Interview Tips (From Mock Session)
- Always connect ML concepts back to real examples from your project
- If unsure, think out loud — interviewers value reasoning process
- Don't just memorize formulas — explain intuition first, then formula
- Prepare to code: `train_test_split`, `GridSearchCV`, `classification_report` from memory

