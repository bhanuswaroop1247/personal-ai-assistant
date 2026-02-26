# Self Introduction Draft – ML & Data Science Interviews

**Project:** Interview Preparation – ML & Data Science  
**Version:** v2.1 (refined after mock interview feedback)  
**Last Updated:** 2025-01

---

## Core Narrative (60-second version)

> "I'm a Master's student in Ophthalmic Engineering, working at the intersection of computer vision and clinical ophthalmology. My thesis focuses on automated keratoconus severity classification using Random Forest — which involves designing the feature extraction pipeline from corneal topography data, tuning the model using out-of-bag error, and interpreting results through confusion matrix recall analysis with clinical focus.
>
> Alongside that, I've built a real-time pupil tracking system using an IDS NIR camera on Linux — handling everything from SDK integration, image preprocessing with CLAHE, contour-based ellipse fitting, to live overlay rendering. This gave me hands-on experience with the full perception pipeline outside of deep learning frameworks.
>
> I'm drawn to roles where machine learning meets real-world measurement and clinical impact — whether that's medical imaging, sensor-based diagnostics, or applied computer vision. I want to bring both the engineering discipline and the domain knowledge that most pure ML engineers don't have."

---

## Structured Answer – For Longer Introductions (3–5 min)

### Background
- Undergraduate in [your undergrad field]
- Currently: MSc Ophthalmic Engineering → research-heavy program, lab + thesis work
- Programming: Python (primary), some C for SDK work, Linux/bash daily

### What I've Built
**Keratoconus Classifier:**
- Multi-class (4-grade) severity classification from Pentacam topographic features
- Random Forest: 91.3% OOB accuracy, emphasis on recall for clinical safety
- Feature importance: BAD-D, Km_mean, TCT as top predictors (clinically validated)
- Paper targeting submission to *Computer Methods and Programs in Biomedicine*

**Pupil Tracking System:**
- IDS uEye NIR camera, pyueye SDK on Ubuntu 22.04
- Pipeline: CLAHE → binary threshold → contour detection → ellipse fit → green overlay
- Real-time at 38fps, < 30ms latency, Kalman filter in development

### Why Data Science / ML Roles
- Want to apply rigorous experimental thinking to real-world ML problems
- Comfortable with end-to-end ownership: data → model → evaluation → interpretation
- Interested in roles with domain specificity (medical, sensor, imaging) not just generic NLP/GenAI

---

## Variations for Different Role Types

### For Research Scientist Role
> Focus on: experimental rigor, OOB error methodology, feature importance validation, paper submission

### For Applied ML Engineer Role  
> Focus on: real-time pipeline, SDK integration, system performance metrics, latency optimization

### For Data Scientist Role
> Focus on: feature engineering, class imbalance handling, confusion matrix interpretation, clinical metric design

---

## Weak Points to Prepare For
- *"Do you have industry experience?"* → No, but research at this depth involves end-to-end ownership similar to industry projects
- *"Have you worked with neural networks?"* → Yes conceptually; my current work intentionally uses interpretable models for clinical use; I'm actively learning PyTorch for future work
- *"How large were your datasets?"* → n≈412 eyes; acknowledge this, explain why OOB is appropriate, mention sample size justification in literature

---

## Interview Story Bank (STAR format)

| Situation | Action | Result |
|-----------|--------|--------|
| SDK kept dropping frames at 60fps | Added frame drop counter, buffered acquisition in thread, reduced ROI | Stable 38fps |
| Mild KCN class had low recall | Added class_weight='balanced', investigated border cases manually | Recall improved from 0.71 → 0.76 |
| Supervisor wanted interpretable model | Used Gini importance + permutation importance comparison | Published-ready feature analysis section |

