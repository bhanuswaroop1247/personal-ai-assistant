# Paper Submission Tracker & Writing Plan

**Project:** Keratoconus Severity Model – Paper Submission  
**Target Journal:** Computer Methods and Programs in Biomedicine (Elsevier) | IF: 6.1  
**Submission Deadline:** TBD – targeting Q2 2025  
**Status:** Draft in progress – Methods complete, Results 60%

---

## Manuscript Structure

| Section | Status | Notes |
|---------|--------|-------|
| Title + Abstract | ✅ Draft done | 250 words, needs revision after results finalize |
| Introduction | ✅ Complete | 4 paragraphs, 12 references |
| Related Work | 🔄 In progress | Need 2 more DL comparison papers |
| Methods | ✅ Complete | RF description, feature table, evaluation metrics |
| Results | 🔄 In progress | Confusion matrix + feature importance done; ablation pending |
| Discussion | ❌ Not started | |
| Conclusion | ❌ Not started | |
| References | 🔄 Ongoing | 28/35 target references added |

---

## Target Journals (Priority Order)

1. **Computer Methods and Programs in Biomedicine** – Best fit (clinical ML)
2. **Biomedical Signal Processing and Control** – Good IF, lower bar
3. **Journal of Ophthalmology** – Clinical audience, less technical depth required
4. **PLOS ONE** – Fallback (open access, broad scope)

---

## Key Arguments to Make in Paper

1. Multi-class severity grading (4 classes) vs. binary classification in most prior work
2. OOB error as built-in validation eliminates data leakage risk from k-fold
3. Recall-focused evaluation is clinically more relevant than accuracy
4. Gini + permutation importance agreement validates feature selection
5. Model explainability is addressed (important for clinical adoption)

---

## Writing Schedule

- Week 1: Finalize Results section (ablation study, ROC curves)
- Week 2: Write Discussion (compare to literature, acknowledge limitations)
- Week 3: Conclusion + Abstract revision
- Week 4: Internal review (send to supervisor)
- Week 5–6: Revise based on feedback
- Week 7: Format for journal submission (Elsevier template)

---

## Figures Needed

- [ ] OOB error curve (n_estimators vs. error)
- [ ] Normalized confusion matrix heatmap
- [ ] Gini importance bar chart
- [ ] ROC curves (one-vs-rest, 4 classes)
- [ ] Feature correlation heatmap (to show Gini bias discussion)
- [ ] Dataset distribution pie chart (class balance visualization)

---

## Reviewer Concerns to Pre-empt

- *"Why not deep learning?"* → Address in Discussion: DL requires larger datasets; RF is interpretable and suitable for clinical settings with limited data
- *"Is dataset size sufficient?"* → Reference similar studies with n ≈ 300–500 in ophthalmology ML literature
- *"How is class imbalance handled?"* → `class_weight='balanced'` with empirical validation in supplementary

