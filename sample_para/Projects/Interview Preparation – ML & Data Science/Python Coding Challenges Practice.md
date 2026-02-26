# Python Coding Challenges – Interview Practice

**Project:** Interview Preparation – ML & Data Science  
**Last Updated:** 2025-01  
**Focus:** Data manipulation, ML utilities, problem patterns

---

## Core Patterns to Master

### 1. Sliding Window
```python
# Maximum sum subarray of size k
def max_sliding_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

### 2. Two Pointers
```python
# Find pair with given sum in sorted array
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target: return (left, right)
        elif s < target: left += 1
        else: right -= 1
    return None
```

### 3. Binary Search
```python
# Find first occurrence in sorted array
def first_occurrence(arr, target):
    lo, hi, result = 0, len(arr) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            result = mid
            hi = mid - 1  # Keep searching left
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result
```

---

## Pandas / NumPy Interview Tasks

### GroupBy + Aggregation
```python
import pandas as pd

# Per-class mean, std of features
df.groupby('severity')['Km_mean'].agg(['mean', 'std', 'count'])

# Pivot table
df.pivot_table(values='BAD_D', index='severity', 
               columns='gender', aggfunc='mean')
```

### Missing Value Handling
```python
# Strategy depends on data type and missingness mechanism
df['feature'].fillna(df['feature'].median(), inplace=True)  # Numeric
df['category'].fillna(df['category'].mode()[0], inplace=True)  # Categorical

# Or use sklearn imputer in pipeline
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
```

### Identifying Data Leakage in Code
```python
# BAD: Scaler fit on all data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # LEAKAGE!
X_train, X_test = train_test_split(X_scaled, ...)

# GOOD: Scaler fit only on train
X_train, X_test = train_test_split(X, ...)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # No leakage
```

---

## ML Utility Code (From Memory)

### Full Training Pipeline
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(
        n_estimators=300,
        class_weight='balanced',
        oob_score=True,
        random_state=42
    ))
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X, y, cv=cv, scoring='f1_macro')
print(f"CV F1: {scores.mean():.3f} ± {scores.std():.3f}")

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred, 
      target_names=['Normal', 'Mild', 'Moderate', 'Severe']))
```

---

## Problem Types to Practice (Tracker)

| Problem | Platform | Status | Difficulty |
|---------|----------|--------|------------|
| Two Sum | LeetCode #1 | ✅ Solved | Easy |
| Longest Substring Without Repeat | LC #3 | ✅ Solved | Medium |
| Binary Search | LC #704 | ✅ Solved | Easy |
| Merge Intervals | LC #56 | 🔄 Review | Medium |
| LRU Cache | LC #146 | ❌ Todo | Medium |
| Top K Frequent Elements | LC #347 | ✅ Solved | Medium |

---

## Tips from Mock Coding Interviews
- Always clarify input constraints before writing code (size, duplicates, sorted?)
- Write brute force first, then optimize — shows thinking process
- Test with edge cases: empty array, single element, all same values
- Don't stay silent — narrate your thinking

