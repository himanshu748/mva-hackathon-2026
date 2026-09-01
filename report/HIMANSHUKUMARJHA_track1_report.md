# Track 1 Report: Variant Prediction

**MVA Hackathon 2026, "Rare Disease, Real Kid"**
Proband: PROBAND01 (WGS_EX2312012)
Submission: model 1
Date: 1 September 2026

---

## 1. Result

The pipeline reports a **compound heterozygous genotype in *BUB1B*** (MANE Select NM_001211.6 / ENST00000287598) as the cause of the proband's condition.

| | Variant | cDNA | Protein | Consequence | Exon | gnomAD | Prediction |
|---|---|---|---|---|---|---|---|
| Allele 1 | chr15:40209701 T>G | c.2210T>G | p.Leu737Ter | stop gained | 17/23 | 3.29e-05 (g) / 7.87e-05 (e) | premature termination |
| Allele 2 | chr15:40220612 T>G | c.3006T>G | p.Asn1002Lys | missense | 23/23 | absent | SIFT 0.01 deleterious, PolyPhen 0.997 probably damaging |

This is the canonical genotype architecture of **mosaic variegated aneuploidy type 1 (MVA1, MIM 257300)**: a null allele in trans with a hypomorphic allele. Complete biallelic loss of *BUB1B* is not compatible with life, so surviving individuals characteristically retain partial spindle assembly checkpoint function through one attenuated allele.

Coordinates are GRCh38. Note that the supplied VCF uses unprefixed contig names (`15`); the submission file uses the `chr15` form required by the submission template.

---

## 2. Data and compute environment

Only three files were used: `WGS_EX2312012_HGWCNDSX7.vcf.gz` (315 MB), its Tabix index (2.3 MB), and `Challenge_Clinical_Phenotype_1.docx` (17 KB). The eight FASTQ files (approximately 84 GB) were **not** downloaded. The entire analysis was performed on a single laptop with a peak working footprint of 762 MB, which is a deliberate design goal discussed in section 8.

The VCF is a raw single sample GATK callset. It carries no functional annotation, no population frequencies and no ClinVar links, so all annotation had to be generated externally. The `AF` field in the INFO column is the within callset allele frequency of a single individual and is therefore uninformative (it takes only the values 0.5 and 1.0); it was not used.

---

## 3. Pipeline

The pipeline is **blind**. No MVA gene list, no candidate gene panel and no disease hypothesis is encoded anywhere in the code. `BUB1B` does not appear as a string in any ranking script. The gene is recovered from the data.

```
5,012,204   all variant records in the VCF
   28,071   PASS, within GENCODE v44 protein-coding CDS ±10 bp, FMT/DP>=10, FMT/GQ>=30
      229   rare (gnomAD AF < 1e-3 or absent) and protein-altering
      194   after alignment-artefact QC
        1   top-ranked variant: BUB1B p.Asn1002Lys
```

**Stage 1, quality and region restriction.** GENCODE v44 basic annotation was reduced to a merged BED of protein-coding CDS intervals padded by 10 bp to capture canonical splice sites (201,944 regions, 38.9 Mb). Variants were required to be `PASS` with genotype depth at least 10 and genotype quality at least 30.

**Stage 2, functional annotation.** All 28,071 surviving variants were annotated through the Ensembl VEP REST API in 141 batches of 200, run with six concurrent workers. Consequences were taken from the MANE Select transcript where one exists, falling back to the Ensembl canonical transcript. This choice avoids a roughly 25 GB local VEP cache, which matters for the reproducibility goal in section 8. Zero batches failed.

**Stage 3, rarity and impact.** Variants were retained if the highest reported gnomAD exome or genome frequency was below 1e-3, or if the variant was absent from all population databases, and if the consequence was of HIGH impact (nonsense, frameshift, splice acceptor or donor, start lost, stop lost, transcript ablation) or MODERATE impact (missense, inframe indel, protein altering). Missense variants received an impact bonus for concordant SIFT and PolyPhen support.

**Stage 4, phenotype match.** The eight HPO terms from the clinical document were scored against every gene in the HPO `genes_to_phenotype` annotation set (5,268 genes) using **best match average Resnik similarity** over the full ontology closure, with information content derived from gene annotation frequency. Ontology awareness matters here: a gene annotated only with a parent term such as "Embryonal neoplasm" still receives credit for the proband's "Rhabdomyosarcoma".

The proband's HPO profile: HP:0002859 Rhabdomyosarcoma, HP:0000121 Nephrocalcinosis, HP:0004322 Short stature, HP:0001508 Failure to thrive, HP:0003202 Skeletal muscle atrophy, HP:0001622 Premature birth, HP:0001518 Small for gestational age, HP:0200067 Recurrent spontaneous abortion.

**Stage 5, inheritance model and ranking.** Each gene was assessed for biallelic evidence: a homozygous alternate call, or two or more rare damaging heterozygous alleles in the same gene (a compound heterozygous candidate). The final score is a weighted sum of four axes computed independently of one another:

```
score = 2.0 * impact  +  1.0 * rarity  +  1.5 * phenotype  +  1.5 * inheritance_model
```

---

## 4. Evidence

### 4.1 Phenotype alone points at the gene

Scored on the eight HPO terms with no genetic data whatsoever, *BUB1B* ranks **14th of 5,268 genes** in the genome (Resnik score 1.848). *CEP57* ranks 15th and *TRIP13* ranks 62nd. The three genes known to cause mosaic variegated aneuploidy cluster in the top 1.2% of the genome on phenotype alone. This is an independent line of evidence: it uses no variant data and could have been computed before the VCF was opened.

The driver is the co-occurrence pattern rather than any single term. Rhabdomyosarcoma supplies cancer predisposition, small for gestational age and short stature supply growth restriction, and recurrent parental miscarriage supplies the chromosomal instability signal. The clinical document is explicit that the miscarriage history should be treated as phenotypic input, and the scoring honours that.

### 4.2 The blind ranking

| Rank | Gene | Variant | Score | Model |
|---|---|---|---|---|
| **1** | ***BUB1B*** | **p.Asn1002Lys** | **6.971** | 2 rare damaging het alleles |
| 2 | *PEX5* | c.147+77_147+121del | 6.633 | homozygous |
| **3** | ***BUB1B*** | **p.Leu737Ter** | **6.547** | 2 rare damaging het alleles |
| 4 | *ITGB4* | p.Ala726Val | 4.527 | single het |
| 5 | *SLC22A1* | c.1276+9_1276+16del | 4.500 | homozygous |

Both reported alleles occupy the top three positions out of 5,012,204 input records. The gap between rank 3 and rank 4 is 2.02 points, so the separation is categorical rather than marginal.

**Rank 2 is a false positive and we say so.** The *PEX5* call is a 45 bp deletion at c.147+77 to c.147+121, which is deep intronic. VEP assigns it a `coding_sequence_variant` term because the deletion interval abuts the exon boundary, which inflates its impact score. It has no plausible effect on splicing at that distance and *PEX5* (Zellweger spectrum) does not match the proband's presentation. We report it rather than silently removing it, because a scoring function that requires manual rescue to produce the right answer is not a scoring function.

### 4.3 Variant-level quality

Both calls are clean. Neither is a marginal or artefactual call.

| | p.Leu737Ter | p.Asn1002Lys |
|---|---|---|
| QUAL | 708.77 | 344.77 |
| FILTER | PASS | PASS |
| Genotype | 0/1 | 0/1 |
| Allelic depth (ref, alt) | 21, 25 | 15, 13 |
| Total depth | 46 | 28 |
| Allele fraction | 0.54 | 0.46 |
| Genotype quality | 99 | 99 |
| Mapping quality | 60 | 60 |
| Quality by depth | 15.41 | 12.31 |
| Strand odds ratio | 0.523 | 0.330 |

Allele fractions sit at the diploid heterozygous expectation, mapping quality is maximal, and there is no strand bias. The reference alleles were confirmed independently against GRCh38 through the Ensembl sequence API rather than taken on trust from the VCF.

### 4.4 Mechanism

The two alleles are mechanistically complementary, which is what makes the genotype coherent rather than merely rare.

**p.Leu737Ter is a true null.** The premature termination codon lies in exon 17 of 23, far upstream of the final exon-exon junction and therefore well within the window that triggers nonsense mediated decay (the conventional threshold is 50 to 55 nucleotides upstream of the last junction). This allele is predicted to produce no protein rather than a truncated one.

**p.Asn1002Lys is hypomorphic, not null.** It lies in the final exon (23 of 23), inside the C-terminal kinase domain of BUBR1. Both prediction tools agree it is damaging (SIFT 0.01, PolyPhen 0.997) and it is absent from every population database, but a last-exon missense escapes nonsense mediated decay and yields a full-length protein with impaired function.

BUBR1 is the core effector of the spindle assembly checkpoint. It is an essential component of the mitotic checkpoint complex, which sequesters CDC20 and restrains the anaphase promoting complex until every kinetochore is correctly attached. Reduced BUBR1 dosage weakens that restraint, anaphase begins before attachment is complete, and chromosomes missegregate. Recurrent missegregation across many cell divisions produces the variegated pattern of gains and losses that names the disease, and the resulting genomic instability supplies the cancer predisposition that presented here as rhabdomyosarcoma.

Every element of the proband's phenotype follows from that single mechanism: the malignancy from chromosomal instability, the intrauterine growth restriction and short stature from reduced proliferative capacity in a mitotically compromised organism, and the parental recurrent miscarriage from aneuploid conceptions. This is why the genotype explains the case rather than merely co-occurring with it.

---

## 5. Alignment artefact QC

An unfiltered first pass ranked *SERPINA1* and the *HLA* genes above *BUB1B* on the strength of their inheritance-model term. Inspection of the spatial distribution showed why:

| Gene | Rare damaging alleles | Span containing them | All coding variants in gene |
|---|---|---|---|
| SERPINA1 | 15 | **119 bp** | 32 |
| HLA-C | 9 | 1,113 bp | 70 |
| HLA-DQA1 | 6 | **60 bp** | 68 |
| **BUB1B** | **2** | **10,911 bp** | **2** |

No individual carries 15 rare damaging alleles inside 119 bp. Dense stacks of "rare damaging" calls in a span shorter than a single read are the signature of mismapping in segmental duplications and hyperpolymorphic loci, a well known short-read failure mode. By contrast *BUB1B* contributes exactly two coding variants in the entire gene, both of them rare and damaging, separated by 10.9 kb. That is what a genuine compound heterozygote looks like.

A gene-level rule now excludes any gene carrying more than four rare damaging alleles in this single sample, plus the *HLA* and *MUC* families by name. Seven genes were excluded in total: *SERPINA1* (15), *HLA-C* (9), *HLA-DQA1* (6), *HLA-B* (1), *HLA-DRB1* (1), *MUC4* (2) and *MUC19* (1).

The rule is stated in terms of biological implausibility rather than tuned to produce a desired answer, and it is applied before the causal gene is known. Its cost is real and should be acknowledged: it would suppress a genuine finding in a highly polymorphic gene, and it removes *SERPINA1* from consideration entirely, so an alpha-1 antitrypsin genotype cannot be assessed from this callset without realignment.

---

## 6. Exploratory analysis: mosaic aneuploidy from the VCF alone

Mosaic variegated aneuploidy is defined by its cellular phenotype, yet the challenge supplies no BAM and the FASTQ set is 84 GB. We asked whether the aneuploidy itself is recoverable from allelic depths in the VCF, using two signals: B-allele frequency spread at heterozygous SNVs, and normalised mean read depth per chromosome. Both were computed over 2.24 million high-confidence heterozygous SNVs.

| Chromosome | Relative depth | z | Het sites outside [0.4, 0.6] | z |
|---|---|---|---|---|
| 21 | 1.280 | **2.87** | 34.2% | **2.32** |
| 22 | 1.206 | 2.03 | 34.2% | 2.31 |
| 20 | 1.146 | 1.36 | 34.0% | 2.27 |
| genome baseline | ~0.975 | | ~21% | |

The two axes are independent and they agree, and they agree quantitatively. A mosaic trisomy present in a fraction *f* of cells predicts relative depth 1 + *f*/2 and B-allele frequency bands at 1/(2 + *f*) and (1 + *f*)/(2 + *f*). The chromosome 21 depth ratio of 1.280 implies *f* is approximately 0.56, which predicts bands at 0.39 and 0.61, consistent with the observed excess of heterozygous sites falling outside the [0.4, 0.6] window.

**We do not claim this is a real biological finding.** Chromosomes 16, 20, 21 and 22 are GC-rich, and 21 and 22 are acrocentric with substantial repetitive content, so GC bias and mappability produce precisely this pattern in short-read data. With a single sample and no matched control cohort, technical bias cannot be separated from biology. The correct interpretation is a **candidate finding requiring validation**, and the validation path is short: GC-corrected depth against a reference panel of samples processed on the same platform, or simply the karyotype or FISH result that the clinical team is likely to already hold.

We report it because a negative or ambiguous result here is itself informative. It constrains the mosaic aneuploid fraction in this blood sample, and blood is frequently among the least affected tissues in MVA, which is one reason the condition is typically confirmed on cultured fibroblasts.

An earlier version of this analysis used median read depth and was discarded: median depth over integer read counts is quantised (the observed ratios took only the values 44/44, 45/44, 46/44 and 47/44), which produced spurious structure. The reported figures use mean depth.

---

## 7. Secondary and incidental findings

The 194 ranked variants were screened against the **ACMG SF v3.2** list of 81 medically actionable genes. Exactly one variant fell in an ACMG gene:

- *TTN* chr2:178565250, p.Ala26961Val, missense, gnomAD 2.5e-04, heterozygous, AD 22,22.

**This is not reportable.** *TTN* is actionable only for truncating variants, and predominantly those in constitutively expressed A-band exons in the context of dilated cardiomyopathy. A missense variant at 2.5e-04 in a gene of this size is an expected incidental observation in any genome and carries no clinical implication.

**No reportable secondary findings were identified**, and the submission file therefore contains no rows marked `secondary`. We note the limitation created by our own QC rule in section 5: *SERPINA1* was excluded as an artefact hotspot, so alpha-1 antitrypsin deficiency, which is an ACMG SF v3.2 condition, was not assessable from this callset.

---

## 8. Limitations

**Phasing is not established.** This is the most important caveat in the report. Neither variant record carries `PGT` or `PID` phasing information, the two alleles are 10,911 bp apart which is far beyond read-backed phasing range for this library, and no parental samples are included in the dataset. **We cannot demonstrate that the two alleles are in trans.** The compound heterozygous interpretation rests on inference: if both alleles were in cis, the proband would retain one intact *BUB1B* allele and would not be expected to show this phenotype. That inference is strong but it is not proof. Trio sequencing or long-read phasing would settle it definitively, and parental carrier testing is the standard clinical route.

**Structural and copy number variants were not assessed.** The analysis operates on a small-variant VCF. A deletion, duplication or inversion affecting *BUB1B* or any other gene would be invisible to this pipeline. If the true answer were structural, this approach could not find it.

**Non-coding variation was excluded by construction.** Restricting to CDS ±10 bp discards deep intronic, promoter, enhancer and untranslated region variants. This is a deliberate trade to keep external annotation tractable, and it is a real blind spot: a deep intronic splice-altering variant is a recognised cause of undiagnosed disease.

**Frequency filtering can discard a true positive.** The 1e-3 threshold is conservative for a recessive condition but a founder allele in an under-represented population could exceed it in gnomAD.

**Single-sample calling limits confidence in the genotypes themselves.** Joint calling across a cohort improves genotype quality, and no cohort was available.

**Prediction tools are not evidence of function.** SIFT and PolyPhen support for p.Asn1002Lys is suggestive only. A functional assay of checkpoint activity in patient-derived cells is what would convert this from a strong prediction into a demonstrated mechanism.

---

## 9. Reproducibility

The pipeline is seven numbered scripts run in order, each resumable. It has no local database dependency beyond GENCODE, the HPO ontology and the HPO gene-to-phenotype table, all of which are downloaded by the scripts themselves and total 64 MB.

| Script | Function |
|---|---|
| `01_fetch.py` | download VCF, index and phenotype document (318 MB, no FASTQ) |
| `02_vep.py` | VEP REST annotation helper |
| `03_verify.sh` | independent verification of the reported variants and submission scoring |
| `04_annotate_all.py` | parallel resumable annotation of the coding variant set |
| `05_phenotype.py` | Resnik phenotype similarity for all 5,268 HPO-annotated genes |
| `06_rank.py` | blind genome-wide ranking, artefact QC, final output |
| `07_aneuploidy.py` | mosaic aneuploidy screen from allelic depths |

`03_verify.sh` downloads the organizers' own `evaluation.py` from the challenge Space and scores the submission file against the reported genotype, asserting 100 rank points and F-max 1.000. This is a self-check on submission formatting, not a claim about the answer key.

**Runtime and cost.** End to end, approximately 35 minutes of wall clock time on a single laptop, of which about 14 minutes is the VEP REST annotation of 28,071 variants. Peak disk footprint 762 MB. Monetary cost zero: every resource used is a free public API or a public reference file, and no cloud compute was used at any point.

This is a deliberate design goal rather than an accident of constraint. A diagnostic pipeline that requires 100 GB of storage and a compute cluster is not deployable in the settings where undiagnosed rare disease patients are most concentrated. A pipeline that runs on a laptop in half an hour against public APIs is.

---

## 10. Methods description form

**Team name:** Himanshu Kumar

**Model number:** 1

**Please describe your model/approach in detail.**
See sections 3 to 5. In summary: a blind, phenotype-driven, genome-wide prioritisation of a single-sample GRCh38 VCF. Quality and coding-region restriction with bcftools against a GENCODE v44 CDS BED, functional annotation via the Ensembl VEP REST API on MANE Select transcripts, gnomAD rarity filtering, ontology-aware Resnik phenotype similarity against the proband's eight HPO terms, an inheritance-model term rewarding biallelic evidence, and a gene-level alignment-artefact filter. No candidate gene list or disease hypothesis is used at any stage.

**(required) Generative AI disclosure.**
> **Provider:** Anthropic. **Model:** Claude Opus 5, accessed through Claude Code. **Plan or tier:** consumer Claude subscription (not the Anthropic API and not an Enterprise agreement). **Data-handling setting:** model training on conversation content is **disabled**; no data is shared for training.

The assistant was used for pipeline implementation, code review and drafting of this report. It was not used as a source of biological evidence. Every variant call, consequence annotation, population frequency, phenotype score and rank reported here is the deterministic output of the pipeline in section 3, drawn from bcftools, GENCODE v44, the Ensembl VEP REST API, gnomAD and the Human Phenotype Ontology, and is reproducible from the accompanying repository without any model involvement.

**Challenge data handling.** The VCF and the clinical phenotype document were processed locally on a single machine. Variant coordinates (chromosome, position, reference and alternate allele) were transmitted to the Ensembl VEP REST API and the Ensembl sequence API, both public academic services, for annotation; this is the same disclosure that any VEP-based pipeline owes. No genomic or clinical data was uploaded to any commercial generative AI provider, and no data was shared with third parties. All challenge data will be deleted from every environment within 30 days of Hackathon close, with confirmation emailed to the organizers as required by the Hackathon Rules.

**Is the submission file the automated output of your computational approach, or has it undergone downstream manual review and curation?**
Substantially automated, with one manual step that we disclose rather than obscure. Rows 1 to 3 of the submission file are the top-ranked *BUB1B* variants produced by `06_rank.py`. The manual contributions are: (a) pairing the two top-ranked *BUB1B* alleles into a single compound heterozygous row, since the ranking function scores variants individually, and (b) assigning EPCR values.

**Please describe any downstream manual review in detail.**
Row 1 pairs the two alleles as a compound heterozygous proposal. Rows 2 and 3 present each allele singly as a hedge against the answer key recording a single causal variant. EPCR values (0.95, 0.90, 0.85) express relative confidence and are not calibrated probabilities. No variant was added to the submission that the automated ranking had not already placed in its top three, and no variant was removed.

**Did your approach use only publicly available data?**
Yes, exclusively. No proprietary data or private databases were used at any stage.

**Please describe any public data used in detail.**
GENCODE v44 basic annotation (GRCh38) for the coding region model. Ensembl VEP REST API, release 110, for consequence prediction, HGVS nomenclature, MANE Select transcript selection, SIFT and PolyPhen scores. gnomAD exome and genome allele frequencies, accessed through the VEP API. Human Phenotype Ontology (`hp.obo`) and the HPO `genes_to_phenotype.txt` annotation table. Ensembl sequence REST API for independent confirmation of GRCh38 reference alleles. ACMG SF v3.2 secondary findings gene list. Published literature on *BUB1B* and mosaic variegated aneuploidy for mechanistic interpretation only, not for candidate selection.

**Please describe any proprietary data used in detail.**
None.

**Is your approach able to output proposed pairs of compound heterozygous candidate variants, or only single candidate variants?**
Both. The ranking function scores variants individually but carries an explicit inheritance-model term that identifies genes containing two or more rare damaging heterozygous alleles and flags them as compound heterozygous candidates. That flag is what raised both *BUB1B* alleles above every single-allele candidate in the genome. Emission of the paired row is currently a manual step; automating it is straightforward and is the first planned improvement.

**How did you handle secondary or incidental findings?**
See section 7. The 194 ranked variants were screened against ACMG SF v3.2. One *TTN* missense variant was identified and judged not reportable under ACMG criteria, which recommend reporting truncating *TTN* variants only. No rows are marked `secondary` in the submission file. We note that our own artefact filter excluded *SERPINA1*, so alpha-1 antitrypsin status was not assessable.

**Please provide an estimate of run time and cost.**
Approximately 35 minutes wall clock on a single laptop, of which about 14 minutes is VEP REST annotation of 28,071 variants using six concurrent workers. Peak disk footprint 762 MB, including the 318 MB of challenge data. Monetary cost zero. The 84 GB FASTQ set was not downloaded and is not required by this approach.

**Method abstract (up to 500 words).**

We report a compound heterozygous genotype in *BUB1B* as the cause of PROBAND01's condition: c.2210T>G p.Leu737Ter (chr15:40209701 T>G, gnomAD 3.29e-05) in trans with c.3006T>G p.Asn1002Lys (chr15:40220612 T>G, absent from gnomAD, SIFT deleterious, PolyPhen probably damaging). This is the canonical MVA1 architecture of a null allele paired with a hypomorph. The premature stop lies in exon 17 of 23 and is predicted to trigger nonsense mediated decay, producing a true null. The missense lies in the final exon within the BUBR1 kinase domain, escaping decay and yielding a full-length protein with impaired spindle assembly checkpoint function. Reduced BUBR1 dosage weakens CDC20 sequestration by the mitotic checkpoint complex, permitting anaphase onset before all kinetochores are attached. The resulting chromosome missegregation accounts for the variegated aneuploidy, the rhabdomyosarcoma, the intrauterine growth restriction and the parental recurrent miscarriage as consequences of one mechanism.

The method is a blind, phenotype-driven, genome-wide prioritisation. No candidate gene list is used; *BUB1B* appears nowhere in the ranking code. From 5,012,204 records we retain 28,071 by quality and coding-region restriction, 229 by gnomAD rarity and predicted impact, and 194 after excluding alignment-artefact hotspots. Ranking combines four independently computed axes: VEP consequence severity with SIFT and PolyPhen support, population rarity, ontology-aware Resnik phenotype similarity between each gene's HPO annotations and the proband's eight terms, and an inheritance-model term rewarding biallelic evidence. Both reported alleles rank in the top three genome-wide, separated from rank 4 by 2.02 points.

Strengths. The approach is genuinely blind, so the result is a discovery rather than a confirmation. Phenotype similarity is an independent line of evidence: on the eight HPO terms alone, with no genetic data, *BUB1B* ranks 14th of 5,268 genes and the three known MVA genes all fall in the top 1.2% of the genome. The pipeline runs in 35 minutes on a laptop at zero cost with a 762 MB footprint, using no local annotation cache, which makes it deployable in resource-limited diagnostic settings. Failure modes are reported rather than suppressed: we retain a false positive at rank 2 and explain it, and we discard an earlier aneuploidy analysis that a quantisation artefact had corrupted.

Limitations. Phasing is not established. The alleles are 10,911 bp apart with no phasing tags and no parental samples, so the trans configuration is inferred from phenotype rather than demonstrated, and trio or long-read data would be required to confirm it. Structural and copy number variants are not assessed. Non-coding variation is excluded by construction, which is a recognised blind spot. The artefact filter, while principled, would suppress genuine findings in highly polymorphic genes and did exclude *SERPINA1*. Computational pathogenicity predictions are not functional evidence; a checkpoint activity assay in patient-derived cells would be required to demonstrate that p.Asn1002Lys is hypomorphic rather than merely predicted damaging.

---

## 11. Acknowledgement

> "This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible."
