# Pupil Dynamics Under Near-Infrared Illumination

**Type:** Knowledge Reference | **Domain:** Ophthalmology – Ocular Imaging & Instrumentation  
**Last Updated:** 2025

---

## Why NIR for Pupil Tracking?

Visible light causes the pupillary light reflex (PLR) — the pupil constricts when illuminated. Using **near-infrared (NIR) light** (wavelengths 750–950 nm) allows continuous pupil imaging without triggering constriction, enabling real-time tracking under naturalistic conditions.

The human iris absorbs NIR minimally; the pupil (aperture into the dark eye interior) appears as a **dark, high-contrast region** against the brighter iris — ideal for segmentation.

---

## Pupillary Anatomy Relevant to Imaging

- **Pupil:** Circular aperture of the iris, ~2–8 mm depending on light level.
- **Iris:** Pigmented sphincter controlling pupil size. Dark irides absorb more NIR; light irides are more reflective.
- **Corneal reflex (Purkinje image P1):** Bright specular reflection from corneal surface. Can interfere with segmentation — must be handled in pipeline.
- **Limbus:** Corneoscleral junction — can serve as anatomical reference for head/eye tracking.

---

## IDS NIR Camera Characteristics

The IDS uEye/IDS NXT camera family (used with the IDS SDK on Linux) provides:
- **Sensor:** CMOS, optimized for NIR when IR filter removed or with NIR-optimized sensor variant.
- **Pixel clock / frame rate trade-off:** Higher pixel clock → higher frame rate → more noise. Balance required.
- **Exposure and gain:** Pupil at 850 nm with appropriate IR LED illumination typically requires low gain (< 50%) and exposure ~5–20 ms.
- **Trigger modes:** Software trigger (latency-limited) or hardware trigger (microsecond precision for stimulus-locked experiments).

---

## Pupil Measurement Parameters

| Parameter | Definition | Typical Range |
|---|---|---|
| Pupil diameter | Diameter in mm or pixels | 2–8 mm |
| Pupil area | π × (d/2)² | Varies |
| Centroid (x, y) | Center of mass of pupil region | Camera-dependent |
| Eccentricity | Deviation from circular | > 0.3 suspect artifact |
| PLR latency | Time to first constriction after light onset | ~200–250 ms |
| Constriction amplitude | Baseline - minimum diameter | 1–4 mm |
| Redilation velocity | mm/s | 0.5–2 mm/s |

---

## Imaging Artifacts in NIR Pupillometry

1. **Corneal specular reflection (P1 reflex):** Bright spot overlapping pupil boundary. Mitigation: offset the IR LED; use morphological operations to fill/exclude.
2. **Eyelid occlusion:** Upper lid occludes pupil during blinks and partial closure. Mitigation: frame rejection, interpolation, landmark detection.
3. **Iris shadow artifacts:** Visible in extreme gaze positions. Mitigation: participant fixation constraint.
4. **Iris vascular patterns:** High-contrast vessel patterns in light irides can confuse edge detectors. Mitigation: Hough transform with minimum radius constraint.

---

## Segmentation Approaches for Pupil Detection

### Thresholding
- Otsu's method or fixed-threshold (calibrated per session).
- Works well in controlled illumination.
- Fails with specular reflection or uneven illumination.

### Canny + Hough Circle Transform
- Edge detection followed by RANSAC-like circular fitting.
- Robust to partial occlusion.
- Parameterization: `dp=1`, `minDist=50`, `param1=50`, `param2=30` (starting values).

### Deep Learning (NanoSAM, SAM-based)
- Segment-Anything style models can segment pupil without explicit parameter tuning.
- Higher latency; may not be real-time on embedded hardware.
- Useful as an offline ground-truth reference.

---

## Real-Time Considerations

For real-time tracking at 30–60 fps:
- Prefer Hough or contour-based methods over deep learning on standard CPUs.
- Pre-crop ROI from previous frame centroid to reduce search area.
- Use exponential moving average for smooth centroid tracking.

---

*References: Wilhelm et al. (2015) "Pupillography." Prog Retin Eye Res. | IDS uEye SDK documentation (Linux).*
