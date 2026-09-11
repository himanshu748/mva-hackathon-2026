# GSE134780 exploratory descriptive audit: analysis plan

Written 8 September 2026 IST before downloading the full count matrix or calculating panel outcomes. The feasibility step inspected sample metadata, the count header and the first two unrelated gene rows. This is an analysis plan for a literature-informed exploratory audit; it is not blinded, preregistered, independent or confirmatory validation.

## Question and scope

Describe how seven literature/prior-report-selected markers vary with BubR1 genotype separately in gastrocnemius muscle and inguinal adipose tissue. Panel, fixed before outcome calculation: **Cdkn2a, Cdkn1a, Serpine1, Igfbp2, Il6, Ccl2, Mmp3**. Include every marker, including missing and low-count markers. This panel is not a validated senescence classifier or a quantitative SASP assay.

Dataset: public mouse GSE134780 only. Muscle: WT=4, HH=3, HL1002P=4; fat: WT=4, HH=4, HL1002P=4. Comparisons within each tissue: HH / WT, HL1002P / WT, HL1002P / HH. A positive log2 contrast means higher expression in the numerator group. No cross-tissue expression-level comparisons, sample pairing, or drug-effect inference.

## Integrity checks

Download the exact public gzip matrix; record URL, byte count, SHA-256, UTC acquisition time, sample metadata SHA-256, script SHA-256, package versions and plan SHA-256. Validate: unique nonempty gene symbols and sample labels; all 23 expected samples present exactly once; nonmissing, finite, integer, nonnegative counts; complete exact label alignment to GEO metadata; nonzero sample library sums; expected group sizes. Fail rather than silently aggregate duplicate gene symbols, impute counts or reorder by position. Report all genes, zero-only genes, positive-in-all samples genes used for normalization, and library sizes.

## Calculations

Normalize the two tissues separately. For the primary descriptive view, compute each gene's geometric mean over samples **only for genes with positive counts in every sample of that tissue**. Each sample size factor is the median of its ratios to these geometric means. Use the unrescaled median ratios directly. Divide every count by its sample size factor. Show individual sample normalized counts and arithmetic group means.

For each panel marker, compute `log2((mean normalized count in numerator + 1) / (mean normalized count in denominator + 1))`. The +1 normalized-count pseudocount is fixed and reported; low-expression effects may depend strongly on it. A secondary normalization uses all-feature library totals to obtain CPM and the same arithmetic-group-mean/log2 formula with **+1 CPM**. This comparison checks effect direction, not numeric comparability between different scales or identical pseudocount influence.

Flag a gene as low-count for a tissue if its mean raw count over all that tissue's samples is below 10. Also report zero counts and each comparison group's mean raw count. The flag is descriptive, not an exclusion rule or a significance threshold. Absent markers remain explicit rows with blank effects.

Sensitivity: omit each sample in a tissue once, recompute its median-ratio size factors from all remaining genes/samples, then recompute each contrast. Thus each muscle contrast has 11 and each fat contrast 12 perturbations, including omissions from the third genotype through their possible normalization effect. Retain per-omission results and summarize minimum/maximum effect, sign matches and number of sign reversals. Use a fixed numerical zero tolerance of 1e-12. Direction stability is not confidence, significance or evidence of generalization. No p-values, adjusted p-values, inferred differential-expression counts or claimed biological replication.

## Tests and reporting

Before interpreting outputs, run hand-calculable toy-count normalization tests, CPM sum/formula checks, label-reordering checks and rejection checks for mismatched labels/noninteger/negative/duplicate inputs. Repeat the finished pipeline once and compare reproducible result hashes; acquisition/run timestamps may differ.

Outputs: self-contained script, downloaded public count matrix, input provenance, sample QC, all-gene normalization QC, 42 panel contrast rows, individual marker/sample rows, leave-one-out rows and a concise factual findings report. If a readily available plotting library exists, one clearly labeled descriptive effect figure may be added.

## Interpretation limits

Mouse L1002P models human L1012P, not human Asn1002Lys. No drug-treated or neural samples exist. Gene-level Cdkn2a cannot resolve p16 versus p19; Cdkn1a is not automatically a harmful signal. Bulk-tissue differences can reflect cell composition as well as cell state. Senescence, protein secretion, drug susceptibility, tissue function, chromosome correction and patient benefit cannot be concluded from these counts. Sample-specific sex, exact age, batch/litter and cross-tissue animal IDs are unavailable in GEO annotations. The age bracket is 8–10 months and n=3–4 per group; selection of surviving mutant animals limits generalization. Null/discordant/unstable results must remain visible. Stop and report any unresolved integrity problem.
