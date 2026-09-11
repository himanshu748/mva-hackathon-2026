# Independent heart-data evidence audit

A fixed seven-marker panel was checked in the authors' public GSE277997 heart differential-expression table and compared with the earlier muscle/fat audit. All seven heart estimates were positive. Three genes—Cdkn2a, Cdkn1a and Igfbp2—had author-reported adjusted P below .05. This is a new reproducible audit of published summary statistics, not a new biological experiment or independently fitted differential-expression analysis.

## Complete panel

Positive log2FC denotes higher expression in hypomorphic versus wild-type hearts. P values and adjusted P values below are copied from the authors' file; no new significance testing was performed.

| Gene | Heart log2FC | Author P | Author adjusted P | Earlier muscle direction | Earlier fat direction |
|---|---:|---:|---:|---|---|
| Cdkn2a | 1.433 | 0.00126 | 0.046 | higher | higher |
| Cdkn1a | 1.823 | 9.98e-13 | 7.81e-11 | higher | lower |
| Serpine1 | 0.822 | 0.0417 | 0.402 | lower | lower |
| Igfbp2 | 3.164 | 4.49e-08 | 3.07e-06 | higher | higher |
| Il6 | 0.821 | 0.0575 | 0.464 | lower | higher |
| Ccl2 | 0.949 | 0.0284 | 0.332 | higher | lower |
| Mmp3 | 1.333 | 0.035 | 0.366 | lower | higher |

The table provides partial cross-study corroboration: Cdkn2a and Igfbp2 point upward in all three tissue datasets, whereas Cdkn1a differs in fat. Heart directions agree with four of seven markers in each earlier tissue comparison. These counts are descriptive, not a classifier accuracy or probability of biological replication. Some earlier effects are very small or sparse; identical or opposite signs near zero have limited biological meaning.

The three adjusted-P findings do not establish senescent-cell number, protein secretion, susceptibility to dasatinib or improved function after clearance. Gene-level Cdkn2a does not separate p16 from p19. Bulk-tissue composition can also change expression. The result supports tissue-specific investigation, while challenging the use of a single universal marker pattern.

## Input qualification and correction

GEO describes the downloadable CSV as significantly dysregulated genes. Inspection found 12,308 unique gene rows, including 10,917 with unadjusted P at least .05, so that description is not accurate for the complete download. All seven prespecified markers were present. This correction was made after the analysis plan was saved; neither the marker panel nor the contrast was changed. The table is not a sample-count matrix, and completeness of the originally tested gene universe was not established.

The 12 deposited samples comprise three male and three female samples per genotype. The authors also describe separate sex analyses. We did not obtain a usable supplementary workbook or sample-count matrix in this pass, and therefore did not independently adjust for sex, analyze interactions, recalculate dispersion, or perform sample-omission checks. No claim is made that the pooled reported effects apply equally to both sexes.

## Cross-study limitations

The heart samples are 16-week animals; the earlier muscle/fat dataset is older. Age, tissue, survival selection, sample processing and statistical methods differ. Comparing direction across these studies cannot isolate a tissue effect. The muscle/fat quantities are descriptive mean-ratio contrasts with a pseudocount, whereas the heart quantities are the authors' differential-expression estimates. Their magnitudes and P values must not be pooled.

The heart study was selected after its disease association and broad findings were known. The seven-marker panel was carried over unchanged from earlier work, and its exact results were not inspected before the plan. This is literature-informed exploration, not blinded validation. No patient genotype, drug-treated sample or functional response was analyzed.

## Reproduction

Requires Python 3 standard library only:

```sh
python3 audit.py
python3 test_audit.py
```

The script resolves paths relative to itself. Inputs, download receipt, fixed plan, complete marker results and cross-study directions are included. Five integrity tests passed; a repeated run produced byte-identical result files. These checks verify extraction and reporting, not the authors' upstream sequencing or statistics.

## Sources

- [GSE277997](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277997), public author-results CSV; source hash and URL in `inputs/receipt.json`.
- [BubR1 Insufficiency Drives Transcriptomic Alterations and Pathology Associated With Cardiac Aging and Heart Failure](https://doi.org/10.1111/acel.70160), 2025; primary methods/results and supplement descriptions inspected.
- [GSE134780](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE134780), earlier muscle/fat descriptive audit. Its full calculations and limitations remain in the companion public_mouse_audit folder; exact prior contrast file is copied here for the comparison.

## Acknowledgement


This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
