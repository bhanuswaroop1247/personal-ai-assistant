# Pupil Segmentation Pipeline – Design & Implementation

**Project:** Real-Time Pupil Tracking Application  
**Camera:** IDS UI-3060CP NIR (Near-Infrared)  
**OS:** Linux (Ubuntu 22.04)  
**Last Updated:** 2025-01  
**Status:** Core pipeline working; green circle overlay in progress

---

## System Overview

```
IDS NIR Camera → uEye SDK (C/Python) → Frame Buffer → 
Preprocessing → Segmentation → Ellipse Fit → 
Green Circle Overlay → Display / Log
```

---

## Hardware Setup

- **Camera model:** IDS uEye UI-3060CP-M-GL (monochrome, NIR-sensitive)
- **Illumination:** 850nm NIR ring light (coaxial)
- **Frame rate:** 60 fps @ 1280×1024
- **Trigger:** Software trigger (free-running mode for real-time)
- **SDK:** IDS uEye SDK 4.96, Python wrapper via `pyueye`

---

## Preprocessing Pipeline

### Step 1: Frame Acquisition
```python
from pyueye import ueye
import numpy as np
import cv2

# Initialize camera
hCam = ueye.HIDS(0)
ueye.is_InitCamera(hCam, None)

# Set pixel clock and frame rate
ueye.is_SetPixelClock(hCam, 30)
ueye.is_SetFrameRate(hCam, 60.0, None)

# Allocate image memory
mem_ptr = ueye.c_mem_p()
mem_id = ueye.INT()
ueye.is_AllocImageMem(hCam, width, height, bits, mem_ptr, mem_id)
ueye.is_SetImageMem(hCam, mem_ptr, mem_id)
ueye.is_CaptureVideo(hCam, ueye.IS_WAIT)
```

### Step 2: Grayscale Normalization
- NIR images arrive as 8-bit grayscale (mono camera)
- Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for consistent illumination
```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
frame_eq = clahe.apply(frame_gray)
```

### Step 3: ROI Cropping
- Restrict processing to central 50% of frame (eye region)
- Reduces computation by ~75%, critical for real-time performance

---

## Segmentation Strategy

### Approach 1: Thresholding (Current)
Pupil appears as dark region in NIR:
```python
_, thresh = cv2.threshold(frame_eq, 60, 255, cv2.THRESH_BINARY_INV)
# Morphological cleanup
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
```

### Approach 2: Contour + Ellipse Fitting
```python
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Select largest contour by area
largest = max(contours, key=cv2.contourArea)
if len(largest) >= 5:
    ellipse = cv2.fitEllipse(largest)
    center, axes, angle = ellipse
```

### Approach 3 (Planned): Circular Hough Transform
- More robust to partial occlusion (by eyelid)
- Slower; will benchmark against thresholding approach

---

## Green Circle Overlay

```python
# Draw fitted ellipse as green overlay
cv2.ellipse(frame_display, ellipse, color=(0, 255, 0), thickness=2)

# Draw center point
cx, cy = int(center[0]), int(center[1])
cv2.circle(frame_display, (cx, cy), 3, (0, 255, 0), -1)

# Text overlay: pupil diameter in pixels
diameter_px = (axes[0] + axes[1]) / 2
cv2.putText(frame_display, f"D: {diameter_px:.1f}px", (cx+10, cy),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
```

---

## Performance Metrics (Target)

| Metric | Target | Current |
|--------|--------|---------|
| FPS | ≥ 30 | 38 |
| Latency (acquisition to display) | < 33ms | ~26ms |
| Pupil center accuracy | ± 2px | ± 3–4px |
| Failure rate (blink/occlusion) | < 5% | ~8% |

---

## Known Issues
- Specular reflection from NIR light creates false bright spot → masked using top-hat filter
- Eyelid occlusion at extreme gaze angles causes segmentation failure → tracking with Kalman filter planned
- SDK occasionally drops frames at 60fps → added frame drop counter and recovery logic

---

## TODO
- [ ] Implement Kalman filter for pupil center smoothing
- [ ] Benchmark Hough transform vs. contour approach
- [ ] Add CSV logging (timestamp, cx, cy, diameter) for experiment recording
- [ ] Package as standalone CLI tool with config YAML

