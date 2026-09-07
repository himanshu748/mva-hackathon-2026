# Track 1 report: variant prediction

MVA Hackathon 2026, “Rare Disease, Real Kid”
Team: Himanshu Kumar (@HIMANSHUKUMARJHA)
Proband: PROBAND01
Revised: 7 September 2026; replaces the methods account accompanying the 1 September entry

## 1. Result and interpretation

We propose two heterozygous *BUB1B* variants as a compound-heterozygous candidate. The original submission received 100.0 rank points and F-max 1.000 on the organizer’s leaderboard, verified on 7 September. This confirms agreement with the challenge’s clinical answer key. Our single-sample analysis does not independently establish phase or residual protein function.

| GRCh38 variant | MANE cDNA | Protein | Consequence | Exon | Reported gnomAD frequency |
|---|---|---|---|---|---|
| chr15:40209701 T>G | NM_001211.6:c.2210T>G | p.Leu737Ter | Stop gained | 17/23 | 3.29e-05 genome; 7.87e-05 exome |
| chr15:40220612 T>G | NM_001211.6:c.3006T>G | p.Asn1002Lys | Missense | 23/23 | No frequency returned in the cached VEP annotation |

The stop allele is predicted to cause loss of function, potentially through nonsense-mediated decay. The missense allele has SIFT 0.01 and PolyPhen 0.997 predictions, but its functional effect remains unmeasured. A null-plus-hypomorph interpretation is a hypothesis requiring RNA, protein and checkpoint assays. The supplied VCF uses unprefixed contigs; the submission uses `chr15` as required by the template.

## 2. Development history

Initial candidate discovery used the three known MVA loci, *BUB1B*, *CEP57* and *TRIP13*. On 1 September at 08:39 UTC, that targeted analysis had identified the reported pair. Development of the genome-wide ranking began at 13:05 UTC, after the pair was known; the artefact heuristic followed inspection of that ranking.

The final score contains no candidate-gene bonus or MVA gene panel. Nevertheless, its design was informed by this case and its known candidate, so the result is a retrospective genome-wide recovery, not a blinded discovery or an independent estimate of diagnostic accuracy. This revision corrects the earlier report’s wording. No held-out patient cohort was evaluated.

## 3. Data and pipeline

The analysis used the supplied VCF, index and phenotype document. It did not use the approximately 84 GB FASTQ set. External references were GENCODE v44, the HPO ontology and gene-to-phenotype table, and VEP REST annotations. The original run was reported as approximately 30 minutes on a laptop. That timing is a historical run estimate, not a benchmark of fresh downloads under current service conditions. AI subscriptions and media generation are excluded from the original zero-incremental-compute-cost estimate.

```
5,012,204 input VCF records
   28,071 PASS coding-region records with DP >= 10 and GQ >= 30
      229 rare variants with selected protein-altering or splice consequences
      194 after the case-informed artefact heuristic
```

**Region and quality restriction.** We used GENCODE protein-coding CDS intervals padded by 10 bp. The merged BED contains 201,944 intervals spanning approximately 38.9 Mb. INFO/AF from a single-sample callset was not used as a population-frequency estimate.

**Annotation.** VEP REST annotated all 28,071 coding inputs in 141 batches. The chosen transcript is the first MANE Select consequence when available, otherwise the first canonical consequence, otherwise the first returned transcript. This first-transcript fallback can miss a relevant consequence in an overlapping gene. It is a limitation of this implementation.

**Rarity and impact.** The filter accepts a variant if the maximum returned overall gnomAD genome/exome ALT frequency is at most 0.001, or if no frequency is returned. Missing annotation does not prove absence from every population database. HIGH consequences receive impact 1.0. MODERATE consequences receive 0.55, with 0.15 added for each of deleterious SIFT and probably-damaging PolyPhen predictions. The script does not use ancestry-specific maximum frequencies.

**Phenotype.** Eight supplied HPO terms describe rhabdomyosarcoma, nephrocalcinosis, short stature, failure to thrive, skeletal muscle atrophy, premature birth, small for gestational age and recurrent spontaneous abortion. The last term records family history, which the clinical document asks participants to include. We compute a patient-to-gene mean of best Resnik matches using ontology ancestors and information content derived from gene annotation frequency. It is a directional mean, not a symmetric best-match-average score. `05_phenotype.py --hpo-file profile.json` accepts another HPO list; reference and score hashes are recorded locally.

**Inheritance and scoring.** A homozygous ALT record receives model score 1.0. A heterozygous record receives 1.0 if its gene contains at least two qualifying heterozygous records; otherwise it receives 0.35. This recognizes possible biallelic candidates without proving trans phase, independence of nearby calls or the gene’s disease-specific inheritance mode.

```
score = 2.0 * impact + 1.0 * rarity + 1.5 * phenotype + 1.5 * model
```

These terms are separate calculations, not statistically independent evidence. In particular, qualifying “damaging” alleles contribute to both impact and inheritance scoring.

## 4. Reproduced ranking and sensitivity

| Rank | Gene | Protein or cDNA description | Score |
|---|---|---|---|
| 1 | BUB1B | p.Asn1002Lys | 6.971 |
| 2 | PEX5 | c.147+77_147+121del | 6.633 |
| 3 | BUB1B | p.Leu737Ter | 6.547 |
| 4 | ITGB4 | p.Ala726Val | 4.527 |
| 5 | SLC22A1 | c.1276+9_1276+16del | 4.500 |

On 7 September, the revised pipeline reproduced the saved ranking. Exact input matching confirmed 141 batches, 28,071 unique annotated inputs, and no missing coding input.

On phenotype alone, BUB1B occupies position 14 of 5,268 genes, CEP57 position 15, and TRIP13 position 62. The phenotype calculation contains no variant input, but it was performed after targeted candidate discovery. Display order among tied scores should not be interpreted as additional biological separation.

We varied each of the four weights independently to 75%, 100% and 125% of baseline: 81 combinations with QC and 81 without QC. In all 162 settings, the first BUB1B allele ranked first and the second ranked second or third. At baseline, removing the artefact filter leaves their ranks at 1 and 3. Removing the phenotype term entirely moves them to ranks 3 and 6. The machine-readable results are in `report/sensitivity_summary.json` and are reproducible with `12_sensitivity.py`.

This is post-hoc stability within one case. It does not remove ascertainment bias or demonstrate performance on other patients.

**PEX5 requires annotation review.** Its selected MANE transcript returns `splice_donor_variant`, `splice_donor_5th_base_variant`, `coding_sequence_variant` and `intron_variant` together with a deep-intronic HGVS description. The splice-donor term causes the HIGH impact score. The earlier account incorrectly attributed the score to `coding_sequence_variant` and declared a harmless false positive. We now retain it as an unresolved annotation conflict. Transcript structure, representation/normalization and read evidence need review before any splice-effect conclusion.

## 5. Variant quality, mechanism and QC limits

| Measure | p.Leu737Ter | p.Asn1002Lys |
|---|---|---|
| FILTER / genotype quality | PASS / 99 | PASS / 99 |
| Genotype | 0/1 | 0/1 |
| Ref / ALT depth | 21 / 25 | 15 / 13 |
| Total depth | 46 | 28 |
| Mapping quality | 60 | 60 |

The available call metrics support the variants, but they do not substitute for read inspection, orthogonal confirmation or family testing. Neither record establishes trans phase. The alleles are 10,911 bp apart and no parental samples were analysed.

BUBR1 participates with BUB3, MAD2 and CDC20 in the mitotic checkpoint complex, inhibiting APC/C activity and delaying chromosome segregation. Impaired checkpoint function is consistent with chromosome missegregation in MVA. We have not measured the proposed allele-to-protein or protein-to-cell effects in this child. Published work in other MVA patient-derived cells found checkpoint defects and restoration after BUBR1 expression. That supports a correction control for future work, but it does not establish the function of either exact allele here. [Suijkerbuijk 2010](https://pubmed.ncbi.nlm.nih.gov/20516114/). [Lischetti et al., 2014](https://www.nature.com/articles/ncomms6563).

The QC heuristic excludes genes with more than four qualifying variant records and genes named HLA-* or MUC*. Seven genes are excluded in this case, including SERPINA1. It was chosen after inspecting this case; it is not a read-alignment test. Dense variation can motivate investigation but is not proof of artefact. Both reported alleles remain in the top three without this exclusion, so it is not required to recover the challenge answer with the current score.

## 6. Exploratory mosaicism and secondary findings

The original VCF-only screen examined allelic depth at high-confidence heterozygous SNVs and chromosome mean depth. It flagged chromosomes 20–22, but the same measurements are susceptible to GC content, mappability, ascertainment and coverage effects. Both signals arise from the same callset and should not be called independent. We cannot estimate a reliable mosaic fraction from this single sample without calibration. No new cytogenetic finding is claimed. GC-corrected read-depth analysis, an appropriate comparison cohort and cytogenetic validation would be required.

The secondary-finding script is an exploratory lookup among the retained candidates. It is not a comprehensive ACMG clinical secondary-findings analysis: the input has already undergone phenotype-oriented filtering and the configured gene set is not asserted to be a complete current ACMG list. A TTN missense candidate was seen, but we do not establish pathogenicity or clinical actionability. No secondary rows are submitted. The earlier statement that this demonstrated no reportable secondary findings has been withdrawn.

## 7. Reproducibility and remaining limits

`run_all.sh` orchestrates setup, data extraction, annotation, phenotype scoring, ranking, exploratory checks and verification. The September revision adds fatal failure handling, exact annotation-coverage validation, cache/input hashes and phenotype provenance. Four synthetic tests exercise missing/duplicate annotations, service outages, changed inputs and modified/missing cache files. The original cache was adopted only after complete input validation; adoption records present-day hashes and does not reconstruct an unrecorded historical service release. The earlier claim of a verified VEP release 110 was unsupported and has been removed.

The local `09_verify.sh` checks the reported candidates against the VCF and checks CSV scoring against the proposed pair. That last step is a format/self-consistency check. The live organizer leaderboard is the separate evidence of answer-key agreement.

Limitations include absent parental phasing, no functional assays, limited noncoding coverage, no structural-variant/CNV analysis, first-transcript selection, no ancestry-aware frequency filter and no held-out validation. A fresh VEP/HPO run can differ after reference updates. The code cannot be presented as a validated diagnostic pipeline.

## 8. Methods description form

**Team name:** Himanshu Kumar. **Model:** revised methods accompanying the same proposed pair; the platform assigns the new submission number.

**Approach:** Sections 2–5 describe targeted initial discovery followed by retrospective genome-wide prioritisation using quality, functional annotation, rarity, HPO similarity and candidate biallelic evidence.

**Automated output or manual curation?** Ranking is automated. Selection of the BUB1B pair and EPCR values was manual. The submitted file includes the pair followed by the individual alleles. EPCR values 0.95, 0.90 and 0.85 are ordering judgments, not calibrated probabilities. PEX5 is omitted from the submitted hypotheses but remains in the full local ranking as an unresolved alternative.

**Downstream review:** Candidate quality, consequence predictions, phenotype fit and the challenge score were inspected. The September revision corrects development-history and mechanism statements and adds cache verification and sensitivity analysis. These checks are computational review, not clinical adjudication.

**Public/proprietary data:** We used the gated challenge dataset plus public GENCODE, HPO and Ensembl/gnomAD resources. The patient dataset is access-controlled; it should not be described as unrestricted public data. No additional proprietary biological database was used.

**Compound heterozygotes:** The code flags genes with multiple qualifying heterozygous records; pairing in the submitted CSV remains a manual curation step. Phase is unproven.

**Secondary findings:** Exploratory only, as explained in section 6. No secondary candidate is submitted and no comprehensive negative clinical finding is claimed.

**Time and cost:** The original analysis was reported as about 30 minutes of computation on a laptop; development, literature work, review and media production took additional time. There was no cloud compute charge for the variant pipeline. Subscription and media charges are not included in that statement.

**Generative AI and data handling:**

**Anthropic:** Claude Opus 5 (`claude-opus-5` in the session record), through Claude Code on a consumer Claude subscription. The assistant helped implement the original pipeline, interpret outputs, search literature and draft reports. Local tool results supplied candidate-variant information and HPO terms to its context. The previous statement that no genomic or clinical information reached a commercial AI provider was incorrect.

**OpenAI:** Codex assisted with the 7 September review, source checks, code corrections, tests, sensitivity analysis and revised writing. Its context included the reports, candidate findings and selected tool outputs. AI output is not biological evidence. The participant confirmed on 7 September that Codex uses the Pro plan with model training disabled. The participant also confirmed that Claude training was disabled during the original work. These account settings are participant-reported; this revision does not claim an independent audit of historical provider retention.

**Ensembl:** The original workflow sent variant coordinates and alleles to the public VEP REST API for annotation and queried reference bases through the sequence API. The September revision reused the existing annotation cache; it did not re-send the genome-wide coding set.

**Deepgram:** Earlier pitch versions used Aura 2 (`aura-2-thalia-en`) for synthesis and Nova 3 for vocabulary checks. The final revised cut is silent at the participant’s request; no new external speech request was made for this cut. The revised scripts include `mip_opt_out=true` in both requests. Deepgram documents that opted-out data is retained only to process the request. Earlier scripts omitted that per-request parameter; the account-level treatment of those earlier requests has not been independently established. The material sent for the pitch consists of report findings and general scientific reasoning, rather than a genome-wide genotype table. [Deepgram documentation](https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program).

The organizers distinguish qualifying processors from recipients and allow the report, candidate findings and HPO terms to remain available. We retain local genomic inputs, intermediate tables and annotation caches only for the permitted period, and will delete those materials and relevant local log content within 30 days of hackathon close, confirming deletion to the organizers. The repository excludes raw and genome-scale derived data. This disclosure describes the workflow; it does not assert that an unverified service setting has been audited. [Organizer clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2).

**Method abstract (under 500 words).**

We report two heterozygous BUB1B variants, p.Leu737Ter and p.Asn1002Lys, as a proposed compound-heterozygous explanation for PROBAND01. The original submission achieved 100 rank points and F-max 1.000 against the organizer’s clinical answer key. Phase and residual protein function remain unestablished by our analysis.

Initial discovery used known MVA loci. We subsequently built a genome-wide ranking, with no candidate-gene bonus, to examine recovery of the already identified pair. The development process was informed by the candidate; this is retrospective recovery rather than blinded validation.

From 5,012,204 VCF records, quality and coding-region restriction retained 28,071 inputs. VEP consequences and gnomAD filtering retained 229 candidates; a case-informed artefact heuristic retained 194. The score combines predicted impact, rarity, directional HPO Resnik similarity and candidate biallelic evidence. The BUB1B alleles rank first and third. They remain within the top three in all 162 tested weight/QC settings, including every setting without the artefact exclusion. Removing phenotype information moves them to ranks three and six.

The revised pipeline validates complete annotation coverage, rejects changed caches and stops on annotation failure. The saved cache contains one annotation per coding input. Historical service versions were not fully recorded, and current hashes do not reconstruct that missing provenance.

We predict loss of function for the stop allele and report damaging computational predictions for the missense allele without declaring measured hypomorphic activity. The second-ranked PEX5 deletion has conflicting consequence/HGVS annotations and requires further review. VCF-only mosaicism estimates remain inconclusive. Structural variation, much noncoding variation, clinical secondary-finding assessment and held-out validation remain outside the demonstrated scope. The next independent checks are family phasing, allele-function assays and evaluation of a frozen method on other cases.

## 9. Acknowledgement

> "This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible."
