# Fixed-panel audit of GSE277997

Written before downloading or reading the full differential-expression table. The file header and GEO sample metadata have been inspected. The associated paper's abstract and broad reported disease findings are known. This is a literature-informed exploratory audit, not a blinded validation or registered analysis.

Question: Does the public heart result table corroborate the directions of the seven markers previously examined in the independent muscle/fat study? Fixed panel: Cdkn2a, Cdkn1a, Serpine1, Igfbp2, Il6, Ccl2, Mmp3. Include every marker. Do not add favorable genes after inspecting results.

The downloadable GSE277997_H_v_WT.csv.gz header is gene/log2FC/pvalue/padj, not sample-level counts. GEO describes this as significantly dysregulated genes. First verify full-table contents and the paper's stated contrast/analysis. Preserve reported statistics as the original authors' estimates. Do not calculate new differential-expression P values, re-normalize summary values or infer unreported sample-level dispersion. An absent marker means unreported in this filtered table, not zero effect, nonsignificance, or evidence against senescence.

Check gene-symbol uniqueness, numeric finite effects, probabilities within [0,1], source hash and contrast direction. Duplicate or ambiguous panel rows halt interpretation. Compare effect directions only against the previously computed HH/WT contrasts in muscle and fat; do not compare their numerical effect sizes across tissues/studies/ages or pool P values. Different measurement pipelines, ages and sample composition prevent a clean tissue-effect inference.

Sample metadata identifies 12 deposited heart samples (three per genotype/sex group). Without a sample matrix, no independent sex adjustment, sex interaction, leave-one-out analysis or biological replication test is possible. Record this limitation explicitly.

Outputs: source receipt, exact panel lookup with missing rows retained, complete exported author results, comparison table and a concise interpretation. Report no drug-response prediction, clinical efficacy, validated senescence classifier or generalization score. The outcome may be an inconclusive audit if filtering removes the informative panel.
