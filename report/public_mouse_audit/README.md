# GSE134780 exploratory public mouse audit

Start with `findings.md` and the frozen `analysis_plan.md`. This package contains public mouse data and descriptive computations only. It contains no child genome data and no completed drug-response experiment.

## Reproduce

The verified environment used Python 3.12 and NumPy 2.3.5; the optional figure uses matplotlib 3.10.6. The audited run used Python and NumPy versions recorded in `results/manifest.json`. From this directory:

```sh
python3 audit_public_mouse.py --test
python3 audit_public_mouse.py \
  --counts inputs/GSE134780_counts.txt.gz \
  --metadata inputs/samples.tsv \
  --plan analysis_plan.md \
  --receipt inputs/count_download_receipt.json \
  --out reproduced_results
```

The script runs the 12 integrity/formula tests before every analysis. It rejects missing or extra sample labels, duplicate genes or samples, noninteger/negative/nonfinite counts, a changed input count hash or a changed analysis plan. There are no network calls or new dependency installations in the script.

Input count SHA-256:

`f12a73805eb3aaf95d666e78756def647a11e95e37bd007dda580bc08ec77cba`

The public 854,190-byte gzip file comes from:

https://ftp.ncbi.nlm.nih.gov/geo/series/GSE134nnn/GSE134780/suppl/GSE134780_counts.txt.gz

`inputs/GSE134780_family.soft` is the original public sample metadata. The tabular `samples.tsv` includes the 32 metadata rows collected at feasibility (GSE134780 and GSE134781); the script selects only the 23 GSE134780 rows and validates their exact match. No expression outcomes from GSE134781 are analyzed or included.

## Files

- `results/panel_contrasts.tsv`: all 42 gene/tissue/contrast rows, raw and normalized group means, both normalization effects, low-count flag and omission summaries.
- `results/panel_sample_expression.tsv`: all 161 panel gene/sample rows, including zeros.
- `results/leave_one_out.tsv`: all 483 perturbation effects, with omitted sample/genotype and normalization eligibility counts.
- `results/sample_qc.tsv`: 23 library sizes, nonzero gene counts, size factors and metadata availability flags.
- `results/normalization_qc.tsv`: tissue-level normalization eligibility and all-zero counts.
- `results/manifest.json`: input, script and output hashes; formula and software versions.
- `results/test_results.json`: passed test names.
- `reproducibility_check.json`: seven byte-identical files from a repeat run using copied inputs in the same environment.

The coordinator added marker_contrasts.png using matplotlib from the unchanged contrast table. The figure shows all 42 contrasts; source values remain in the TSV files.

Positive contrasts mean higher arithmetic group mean in the numerator. Effects use +1 pseudocounts in different units for median-ratio counts versus CPM, so secondary normalization is a direction check. Leave-one-out ranges are not confidence intervals. No p-values, significance calls, senescence classifier, patient-risk score or treatment recommendation is generated.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.

## Optional figure reproduction

Install the pinned requirements into an isolated environment, then run `python3 plot_marker_contrasts.py`. The plot reads the verified contrast table; it performs no new statistical analysis. Public experimental data remain attributable to the original investigators and their source terms; the participant does not claim authorship of them.
