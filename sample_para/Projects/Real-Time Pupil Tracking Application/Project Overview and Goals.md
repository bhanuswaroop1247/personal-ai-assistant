# Real-Time Pupil Tracking – Project Overview & Goals

**Project:** Real-Time Pupil Tracking Application  
**Supervisor:** [Lab PI Name]  
**Start Date:** October 2024  
**Expected Completion:** April 2025  
**Status:** Active development – v0.2 working

---

## Project Goal

Develop a real-time pupil tracking system using an IDS NIR monochrome camera on Linux. The system must:
1. Acquire frames at ≥ 30 fps from the uEye SDK
2. Segment the pupil using image processing (not deep learning – for portability and latency)
3. Fit an ellipse to the pupil boundary
4. Overlay a green circle/ellipse on the live video feed
5. Log pupil center (cx, cy), diameter (px), and timestamp to CSV

---

## Use Case

This system will be used in a lab experiment measuring **pupillary light reflex (PLR)** dynamics. Precise temporal resolution of pupil diameter changes is required when a brief light stimulus is presented.

**Clinical relevance:** Impaired PLR is associated with optic nerve pathology, traumatic brain injury, and neurological disease. Automated tracking enables objective, quantitative analysis.

---

## System Requirements

| Requirement | Specification |
|-------------|--------------|
| Latency | < 33ms (end-to-end) |
| Frame rate | ≥ 30 fps |
| Accuracy | ± 2px center, ± 1.5px diameter |
| OS | Ubuntu 22.04 LTS |
| Language | Python 3.10 (core), C extension if needed |
| Display | OpenCV `imshow` window with overlay |
| Output | CSV log + optional video recording |

---

## Architecture Overview

```
├── main.py                 # Entry point, CLI interface
├── camera/
│   ├── ueye_wrapper.py     # IDS SDK abstraction
│   └── frame_grabber.py    # Continuous acquisition thread
├── processing/
│   ├── preprocessor.py     # CLAHE, ROI crop
│   ├── segmentation.py     # Thresholding + contour fitting
│   └── tracker.py          # Kalman filter wrapper
├── display/
│   └── overlay.py          # Green circle, text overlay
├── logging/
│   └── data_logger.py      # CSV + video writer
└── config/
    └── settings.yaml       # Exposure, ROI, thresholds
```

---

## Milestones

| Milestone | Target Date | Status |
|-----------|------------|--------|
| SDK integration + frame acquisition | Nov 2024 | ✅ Done |
| Basic threshold segmentation | Nov 2024 | ✅ Done |
| Ellipse fitting + green overlay | Dec 2024 | ✅ Done |
| Kalman filter integration | Jan 2025 | 🔄 In progress |
| CSV + video logging | Feb 2025 | ❌ Not started |
| Testing with PLR stimulus | Mar 2025 | ❌ Not started |
| Lab deployment + documentation | Apr 2025 | ❌ Not started |

---

## Open Questions

1. Should I switch to Hough Circle Transform for more robust detection? (Benchmark needed)
2. Is 60fps necessary or is 30fps sufficient for PLR dynamics? (Literature review needed)
3. How to handle the bright specular reflection artifact at certain gaze angles?

