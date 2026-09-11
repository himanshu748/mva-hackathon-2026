# Offline ranking audit — 11 September 2026

A complete local cache check and transcript-selection audit recovered 20 candidate variant–gene entries omitted by the original first-transcript rule. BUB1B remains at ranks 1 and 3 in all six evaluated branches. This is a retrospective method check on the same case, not independent diagnostic validation, proof of phase, or evidence for a drug treatment.

## Method and results

No network requests or raw-read downloads were used. Existing annotations covered all 28,071 coding inputs in 141 batches, with matching cache/input/reference hashes. The audit exactly reproduced all 194 saved baseline entries, their order and numerical scores before changing transcript selection.

The original script chooses the first MANE transcript globally for each input, falling back to canonical and then any transcript. The alternative selects preferred transcripts separately for each gene. A second alternative selects the highest-scoring consequence within that gene's preferred tier. These are explicit sensitivity analyses; maximizing predicted consequence is not a clinical transcript-selection standard.

| Annotation selection | Gene exclusions applied | Exclusions removed | BUB1B ranks |
|---|---:|---:|---|
| Original global first transcript | 194 | 229 | 1, 3 |
| Preferred transcript per gene | 214 | 249 | 1, 3 |
| Highest-scoring preferred consequence per gene | 214 | 249 | 1, 3 |

The additional entries are variant–gene pairs, not 20 new diseases or necessarily 20 distinct variants. 9,385 cached inputs touch multiple annotated genes; this includes noncoding overlaps and does not mean each is pathogenic. Seventy coding inputs are multiallelic; none occurs in the original retained shortlist. This does not establish correct allele-specific handling across those 70 inputs.

## Follow-up candidates and annotation conflict

In the per-gene branch with exclusions, CTU2 and LZTR1 enter ranks 4 and 5. Direct local VCF checks confirm their cached genotypes/depths: both PASS, CTU2 depth 27/GQ82 and LZTR1 depth 48/GQ99. Call quality does not establish disease relevance. These entries require transcript, inheritance and phenotype assessment before promotion. The inherited scoring assumptions, missing-frequency treatment and gene-exclusion heuristics remain unchanged.

PEX5 stays rank 2. Its cached MANE transcript contains both splice-donor and intronic terms, while its HGVS description places the deletion within an intron. The cached GENCODE reference contains the exact same transcript versions for PEX5, CTU2 and LZTR1. Genomic intervals overlap CDS/exons for all three; PEX5 and CTU2 HGVS descriptions remain intronic. Representation shifts could explain this, but local reference sequence is unavailable to establish equivalence. We therefore do not declare the splice terms erroneous or functionally proven. Do not label it a confirmed splice-disrupting or causal allele. No new external annotation was requested.

## Reproducibility and scope

Run `python3 audit.py --root /path/to/existing/private/checkout`. `audit.py` reads the existing private checkout and writes this audit folder. It validates the saved cache and phenotype references, reproduces the baseline, and writes separate branch results. It does not modify the original ranking or submitted files. `results.json` holds all branch summaries and added entries; `added_call_checks.json` records the two source-call checks. Variant coordinates and alleles are not included in this report. The original data remain local.

The principal improvement is a more complete candidate review with explicit transcript-selection sensitivity. No candidate is promoted to a diagnosis or treatment target by this audit. Noncoding variants outside the original extraction, comprehensive structural variation and raw-read evidence remain unassessed. Submission remains paused.
