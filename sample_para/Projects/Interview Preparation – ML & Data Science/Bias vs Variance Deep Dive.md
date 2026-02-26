# Bias vs. Variance – Deep Dive

**Project:** Interview Preparation – ML & Data Science  
**Topic:** Core ML Theory  
**Last Updated:** 2025-01  
**Status:** Reviewed – needs practice questions

---

## The Bias-Variance Decomposition

For a regression model, the expected test error can be decomposed as:

```
E[(y - f̂(x))²] = Bias²[f̂(x)] + Var[f̂(x)] + σ²
```

Where:
- **Bias²** = error from wrong assumptions in the learning algorithm
- **Variance** = sensitivity to fluctuations in the training set
- **σ²** = irreducible noise

---

## Intuitive Definitions

**High Bias (Underfitting):**
- Model too simple to capture true pattern
- Error is high on both training and test set
- Example: Linear regression on a quadratic relationship
- Fix: More complex model, more features, reduce regularization

**High Variance (Overfitting):**
- Model learns noise specific to the training set
- Error is low on training, high on test
- Example: Unpruned decision tree with depth = sample size
- Fix: Regularization, more data, simpler model, ensemble methods

---

## The Tradeoff

As model complexity increases:
- Bias decreases (model can fit more patterns)
- Variance increases (model becomes more sensitive to training data)
- Test error follows a U-shape → optimal complexity in the middle

```
Error
  |        *                         <- High variance region
  |       * *                   
  |      *   *   <- Optimal
  |    **     **
  |  **         ***
  |**               ****
  +------------------------------> Complexity
        High bias <-> High variance
```

---

## Examples Across Algorithms

| Algorithm | Typical Bias | Typical Variance | Notes |
|-----------|-------------|-----------------|-------|
| Linear Regression | High | Low | Classic high-bias |
| Deep Decision Tree | Low | High | Classic high-variance |
| Random Forest | Low | Medium-Low | Variance reduction via bagging |
| Gradient Boosting | Low-Medium | Medium | Bias reduction via boosting |
| SVM (RBF) | Adjustable via C, γ | Adjustable | Tune carefully |
| KNN (k=1) | Low | Very High | Memorizes training set |
| KNN (k=n) | High | Low | Predicts global mean |

---

## Connection to My Keratoconus Model

**Random Forest reduces variance through bagging:**
- Each tree is trained on a bootstrap sample → different trees see different data
- Averaging predictions across 300 trees reduces individual tree's high variance
- This is why RF outperforms a single decision tree even without tuning

**In my results:**
- OOB error (91.3%) ≈ 5-fold CV accuracy (90.8%) → low variance in generalization estimate
- No significant gap between training accuracy (~98%) and OOB → mild overfitting acceptable at this scale

---

## Common Interview Questions

1. "What's the bias-variance tradeoff?" → Define, give formula, explain U-curve
2. "How does regularization address this?" → L1/L2 increase bias, reduce variance
3. "Does Random Forest have high bias or variance compared to a single tree?" → Lower variance (bagging), similar/lower bias
4. "If your model has high training accuracy but low test accuracy, what's happening?" → High variance/overfitting
5. "How would you diagnose bias vs. variance empirically?" → Learning curves: training vs. validation error vs. dataset size

---

## Learning Curve Interpretation

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    estimator, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
)
# High bias: both curves converge at high error
# High variance: large gap between train and val, val still decreasing
```

