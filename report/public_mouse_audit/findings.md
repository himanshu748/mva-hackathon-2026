# Exploratory public mouse count audit — 8 September 2026

**The seven-gene panel has a mixed, tissue-dependent expression pattern.** These descriptive results support testing individual biological outcomes rather than treating all selected markers as one uniform senescence signal. They do not establish that senolytic treatment would help.

The literature-informed panel and calculations were written down before the full count matrix was downloaded. This is an unblinded reanalysis of a study selected because its published findings were already known. The [analysis plan](analysis_plan.md) is unchanged from its hash in the download receipt.

## What was checked

Public dataset **GSE134780** contains 24,062 unique gene rows and 23 exactly matched mouse samples. Counts are finite, integer and nonnegative, without duplicate sample/gene labels. Muscle has WT=4, HH=3, HL1002P=4; fat has four samples per genotype. All seven panel genes are present. Twelve hand-calculated formula, label-alignment and invalid-input tests pass. A repeat run using copies of the inputs produced seven byte-identical output files, including its manifest; this is same-environment reproducibility, not an independent validation.

Within-tissue median-ratio normalization used 14,460 genes positive in every muscle sample and 15,576 in every fat sample. Total assigned gene counts ranged from 34,137,821–55,266,273 in muscle and 22,552,184–58,828,571 in fat. These are count-matrix integrity checks; they do not verify original sample identity, mapping quality or experimental quality. No sample was removed.

## Results

Table entries are **descriptive log2 contrasts using median-ratio normalized group means with +1**, followed by `(same direction after omission / all omissions)`. Positive means higher in the numerator. Omission includes every sample in that tissue, with size factors recomputed; the denominator is 11 for muscle and 12 for fat. These fractions are sensitivity diagnostics, not probabilities, confidence intervals or statistical significance. No p-values were computed.

| Tissue | Gene | HH / WT | HL1002P / WT | HL1002P / HH |
|---|---|---:|---:|---:|
| Muscle | Cdkn2a | +2.99 (11/11) | +2.90 (11/11) | -0.09 (9/11) |
| Muscle | Cdkn1a | +1.59 (11/11) | +1.48 (11/11) | -0.10 (8/11) |
| Muscle | Serpine1 | -0.34 (11/11) | -0.21 (11/11) | +0.13 (11/11) |
| Muscle | Igfbp2 | +2.82 (11/11) | +3.83 (11/11) | +1.01 (10/11) |
| Muscle | Il6 * | -0.13 (8/11) | -0.45 (10/11) | -0.32 (10/11) |
| Muscle | Ccl2 | +1.04 (11/11) | +0.88 (11/11) | -0.16 (10/11) |
| Muscle | Mmp3 | -0.02 (7/11) | +0.84 (11/11) | +0.86 (11/11) |
| Fat | Cdkn2a | +1.82 (12/12) | +1.89 (12/12) | +0.06 (9/12) |
| Fat | Cdkn1a | -1.34 (12/12) | -1.23 (12/12) | +0.11 (11/12) |
| Fat | Serpine1 | -2.69 (12/12) | -2.75 (12/12) | -0.06 (7/12) |
| Fat | Igfbp2 | +0.22 (11/12) | -0.47 (11/12) | -0.70 (12/12) |
| Fat | Il6 | +0.25 (11/12) | +0.60 (12/12) | +0.35 (10/12) |
| Fat | Ccl2 | -1.68 (12/12) | -0.60 (11/12) | +1.08 (12/12) |
| Fat | Mmp3 | +0.01 (8/12) | +0.12 (11/12) | +0.11 (11/12) |

\* Muscle Il6 has mean raw count 2.64 and three zero-count samples; it is the only panel gene/tissue pair below the fixed mean-raw-count threshold of 10. This flag did not exclude it. Muscle Cdkn2a is not below that tissue-wide threshold, but its WT group mean is only 3 raw counts, making the pseudocount particularly relevant.

Specific observations:

- **Cdkn2a is higher in both mutant groups than WT in both tissues.** All four directions survive every omission. This is gene-level Cdkn2a; it cannot distinguish p16 from p19 transcripts or count senescent cells.
- **Cdkn1a has opposite directions between tissues:** higher in mutant muscle and lower in mutant fat, stable to all omissions for these WT comparisons. Cdkn1a is not automatically a harmful marker; this analysis cannot assign a beneficial or harmful role.
- **Serpine1 is lower in both mutant groups than WT in both tissues.** All four directions survive omission. The panel therefore does not show universal upward movement of selected markers.
- Small mutant-versus-mutant differences and several other comparisons are sensitive to which sample is present. **23 of 42** full-data contrasts retain direction across every omission; **19 of 42** do not. This includes some visibly small effects close to zero.
- Median-ratio and CPM effects have the same direction in **41 of 42** comparisons. The exception is muscle Mmp3, HH/WT: **−0.020** versus **+0.050**, both near zero. Magnitudes across the two methods must not be directly compared: +1 normalized count and +1 CPM are different pseudocount scales, especially for sparse genes. The complete CPM results remain in the machine-readable table.

## What the audit cannot show

There are no drug-treated or neural samples. Mouse L1002P corresponds to human L1012P, **not** human Asn1002Lys. Bulk RNA counts cannot identify source cells, secreted proteins, senescent-cell burden, treatment selectivity, chromosome repair, tissue function or patient benefit. Cell-composition changes can alter these gene-level averages. Sample-specific sex, exact age, batch/litter and cross-tissue animal pairing are not supplied in GEO annotations; no pairing or covariate values were invented. The 8–10-month mutant survivors and n=3–4 per group limit generalization. This is a selected seven-gene panel, not a pathway-wide SASP reproduction or an independent cohort.

The useful submission claim is: **a completed exploratory public mouse reanalysis found heterogeneous marker patterns and identified normalization and sample sensitivity that the proposed biological tests must address.** All biological drug-response work remains proposed.

Sources: [GSE134780](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE134780), [Sieben et al., original study](https://www.jci.org/articles/view/126863), [2020 corrigendum](https://www.jci.org/articles/view/144781). Credit for the experimental data belongs to the original investigators. This audit created no new animal or human experimental data.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
