# Keratoconus Progression Indicators

> **Type:** Knowledge Reference | **Domain:** Ophthalmology & Vision Science | **Last Updated:** 2025

---

## Definition

Keratoconus is a progressive, non-inflammatory ectatic corneal disorder characterized by stromal thinning, apical protrusion, and irregular astigmatism. Identifying early progression is critical because it determines candidacy for **corneal cross-linking (CXL)**, the only treatment that halts progression.

---

## Clinical Criteria for Progression

Consensus criteria (global consensus 2015, ABCD grading system) define progression as any of the following occurring over 6–12 months:

- Increase in Kmax (maximum keratometry) ≥ **1.0 D**
- Increase in anterior mean keratometry (Km) ≥ **1.0 D**
- Increase in cylinder (refraction) ≥ **0.5 D**
- Decrease in minimum corneal thickness ≥ **10 µm**
- Loss of CDVA (Corrected Distance Visual Acuity) ≥ **2 Snellen lines**

---

## Pentacam Parameters as Progression Markers

The Scheimpflug-based Pentacam HR provides objective topographic indices used in longitudinal progression monitoring:

| Parameter | Meaning | Progression Indicator |
|---|---|---|
| **Kmax** | Maximum simulated keratometry | Most sensitive single marker |
| **ISV** (Index of Surface Variance) | Deviation of keratometry from mean | Increases with irregularity |
| **IVA** (Index of Vertical Asymmetry) | Asymmetry between superior/inferior | Elevation in progressive KC |
| **KI** (Keratoconus Index) | Overall ectasia index | Composite indicator |
| **CKI** (Central Keratoconus Index) | Central corneal change | Early-stage marker |
| **Rmin** | Minimum radius of curvature | Decreases as protrusion worsens |
| **Thinnest Point Pachymetry** | Minimum corneal thickness | Direct structural measure |
| **BAD-D** (Belin-Ambrósio Enhanced Ectasia Display D-value) | Deviation from normative database | Combines multiple maps |

---

## ABCD Grading System

Proposed by Belin et al., the ABCD system grades each component independently:

- **A** = Anterior radius of curvature (3mm zone)
- **B** = Posterior radius of curvature (3mm zone)
- **C** = Thinnest corneal pachymetry
- **D** = Distance-corrected visual acuity

Each is graded 0–4, allowing independent tracking of anatomic vs. functional progression.

---

## Early Detection: Subclinical / Forme Fruste Keratoconus

Pre-clinical KC is the most challenging to identify. Indicators include:

- Posterior corneal elevation > 15 µm above best-fit sphere
- Asymmetric bowtie pattern with skewed axes on axial map
- ISV > 37 or IVA > 0.28 (borderline values)
- Asymmetry index (AI) between fellow eyes > 1.5 D
- **Topographic Keratoconus Classification (TKC)** grade 0–1 with suspicious index combination

---

## Imaging Modalities for Progression Monitoring

| Modality | Key Output | Clinical Role |
|---|---|---|
| **Pentacam Scheimpflug** | Anterior + posterior elevation, pachymetry | Standard of care |
| **Placido-disc topography** | Anterior curvature only | Screening, less comprehensive |
| **Optical Coherence Tomography (OCT)** | High-res pachymetry | Epithelial mapping |
| **Brillouin microscopy** | Corneal biomechanical stiffness | Research; predicts CXL response |
| **Corvis ST** | Dynamic corneal response | Biomechanical deformation metrics |

---

## Key Principle for Machine Learning Applications

When building a severity classification model:
- Features should cover **curvature**, **elevation**, **pachymetry**, and **asymmetry** dimensions
- Temporal data (serial topographies) improves progression prediction significantly
- Cross-sectional models classify severity; longitudinal models predict progression trajectory
