# Keratoconus – Clinical Overview & Diagnostic Features

**Resource:** Ophthalmology & Vision Science  
**Type:** Knowledge building block – clinical reference  
**Last Updated:** 2025-01

---

## What is Keratoconus?

Keratoconus (KCN) is a bilateral, asymmetric, progressive corneal ectasia characterized by:
- **Corneal thinning** — especially at the thinnest corneal location (TCT)
- **Protrusion** — anterior and posterior corneal surface deformation
- **Irregular astigmatism** — causes myopia and distorted vision
- **Stromal collagen disorganization** — underlying structural cause

Prevalence: ~1 in 2000 in the general population, higher in certain ethnicities (South Asian, Middle Eastern populations). Typically presents in adolescence to early adulthood.

---

## Pathophysiology

- Loss of stromal lamellar organization → reduced biomechanical stiffness
- Localized corneal thinning → imbalanced intraocular pressure support → progressive protrusion
- Genetic component: associated with eye rubbing, atopy, connective tissue disorders (Marfan, Ehlers-Danlos)
- Progression typically slows after age 30–35

---

## Diagnostic Instruments

### Scheimpflug Tomography (Pentacam HR)
- Gold standard for KCN detection and monitoring
- Captures full corneal profile: anterior surface, posterior surface, pachymetry map
- Key outputs:
  - Km (mean keratometry), K-flat, K-steep
  - TCT (thinnest corneal thickness, µm)
  - BAD-D (Belin-Ambrosio Deviation – composite AI-based score)
  - Elevation maps referenced to best-fit sphere (BFS)

### Specular Microscopy
- Endothelial cell density assessment
- Not used for KCN grading but relevant for surgical planning

### Slit Lamp
- Fleischer ring (iron deposition at cone base)
- Vogt's striae (vertical stress lines in deep stroma)
- Scarring (advanced KCN)

---

## Grading Systems

### Amsler-Krumeich (Classic)
| Grade | Km (D) | Min. Thickness (µm) | MRSE | Scarring |
|-------|--------|---------------------|------|---------|
| I | < 48 | > 500 | < -5 | No |
| II | 48–53 | 400–500 | -5 to -8 | No |
| III | 53–55 | 300–400 | > -8 | No |
| IV | > 55 | < 300 | N/A | Yes |

### ABCD Grading (Belin-Ambrosio)
- A = Anterior radius of curvature (8.0mm zone)
- B = Posterior radius of curvature
- C = Minimum corneal thickness
- D = CDVA (corrected distance visual acuity)
- Each graded 0–4; more sensitive to subclinical disease than AK

---

## Key Topographic Features for ML (My Feature Set)

| Feature | Clinical Meaning |
|---------|-----------------|
| Km_mean | Average corneal curvature — steeper = more KCN |
| BAD-D | Composite KCN deviation score |
| TCT | Thinnest point thickness — KCN thins locally |
| Posterior float BFS | Posterior surface elevation — earliest KCN sign |
| KI | Keratoconus Index |
| ISV | Index of Surface Variance — shape irregularity |
| SRAX | Skewed axis of radial asymmetry |
| KISA% | Combined discriminant index for KCN |

---

## Treatment Options by Stage

- **Grade I–II:** Monitoring; contact lens correction; crosslinking (CXL) to halt progression
- **Grade III:** Corneal crosslinking + intrastromal corneal ring segments (ICRS)
- **Grade IV:** Deep anterior lamellar keratoplasty (DALK) or penetrating keratoplasty (PKP)

**Clinical urgency of correct staging:** Misclassifying Grade II as Grade I may delay CXL, allowing irreversible progression. This is the key motivation for high-recall classification.

