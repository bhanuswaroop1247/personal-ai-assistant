# Kalman Filter for Pupil Tracking – Design Notes

**Project:** Real-Time Pupil Tracking Application  
**Status:** Design phase – implementation pending  
**Last Updated:** 2025-01

---

## Motivation

The current contour-based pupil segmentation works well under stable illumination but fails in two scenarios:
1. **Blinks** – complete occlusion lasting ~150–300ms
2. **Eyelid intrusion** – partial occlusion at extreme gaze angles corrupts ellipse fitting

A Kalman filter provides a principled way to:
- Smooth noisy pupil center estimates
- Predict pupil position during brief occlusions
- Reduce jitter in diameter measurement

---

## State Space Formulation

**State vector:**
```
x = [cx, cy, vx, vy, d]
```
Where:
- `cx, cy` = pupil center coordinates
- `vx, vy` = velocity (pixels/frame)
- `d` = pupil diameter (pixels)

**Observation vector:**
```
z = [cx_measured, cy_measured, d_measured]
```

---

## Transition Matrix (A)

Assuming constant velocity model:
```
A = [[1, 0, 1, 0, 0],
     [0, 1, 0, 1, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 0, 1, 0],
     [0, 0, 0, 0, 1]]
```

Observation matrix H:
```
H = [[1, 0, 0, 0, 0],
     [0, 1, 0, 0, 0],
     [0, 0, 0, 0, 1]]
```

---

## Implementation with OpenCV

```python
import cv2
import numpy as np

# Initialize Kalman filter
kf = cv2.KalmanFilter(5, 3)  # 5 state, 3 measurement

kf.transitionMatrix = np.float32([
    [1,0,1,0,0],
    [0,1,0,1,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
])

kf.measurementMatrix = np.float32([
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,0,0,0,1]
])

kf.processNoiseCov = np.eye(5, dtype=np.float32) * 1e-2
kf.measurementNoiseCov = np.eye(3, dtype=np.float32) * 1e-1
kf.errorCovPost = np.eye(5, dtype=np.float32)

# Per-frame usage
def update_tracker(kf, measurement, segmentation_success):
    predicted = kf.predict()
    
    if segmentation_success:
        corrected = kf.correct(np.float32(measurement).reshape(3, 1))
        return corrected[:2].flatten(), corrected[4, 0]
    else:
        # Use prediction only (during blink/occlusion)
        return predicted[:2].flatten(), predicted[4, 0]
```

---

## Blink Detection

Blink is detected when:
- Segmented area drops below threshold (< 200 px²) OR
- Segmentation fails entirely for > 2 consecutive frames

During detected blink:
1. Stop updating Kalman filter with measurements
2. Continue predicting with state model
3. Resume updating when segmentation recovers

---

## Performance Expectations

| Condition | Without KF | With KF |
|-----------|-----------|---------|
| Center jitter (std, px) | ~3.2 | ~0.8 |
| Diameter noise (std, px) | ~2.1 | ~0.6 |
| Recovery after blink | Hard cut | Smooth |

---

## Alternatives Considered

- **Particle filter:** More robust to non-Gaussian noise but computationally expensive
- **MediaPipe iris:** High accuracy but not designed for NIR images; tested → poor results
- **Savitzky-Golay smoothing:** Post-hoc, not real-time predictive; useful for offline analysis

**Decision:** Kalman filter is the best balance of simplicity, performance, and real-time suitability for this use case.

