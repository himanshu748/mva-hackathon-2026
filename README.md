# MVA Hackathon 2026, Track 1: blind variant prioritisation

A phenotype-driven, genome-wide pipeline that recovers the causal genotype for PROBAND01 from a single-sample VCF, in about 30 minutes on a laptop, at zero cost, using 762 MB of disk and no local annotation cache.

**Result.** Compound heterozygous ***BUB1B*** (MANE Select NM_001211.6):

| Allele | Variant (GRCh38) | Protein | Consequence | gnomAD |
|---|---|---|---|---|
| 1 | chr15:40209701 T>G | p.Leu737Ter | stop gained, exon 17/23 | 3.29e-05 |
| 2 | chr15:40220612 T>G | p.Asn1002Lys | missense, exon 23/23 | absent |

A null allele in trans with a hypomorph: the canonical architecture of mosaic variegated aneuploidy type 1. Both alleles rank in the **top 3 of 5,012,204** input records.

Full write-up: [`report/HIMANSHUKUMARJHA_track1_report.md`](report/HIMANSHUKUMARJHA_track1_report.md).
Submitted 1 September 2026: **100.0 rank points, F-max 1.000, full match at rank 1.**

**Track 2** proposes senolytic therapy (dasatinib plus quercetin) as a repurposing hypothesis, reasoning from the mechanism rather than from the target: [`report/HIMANSHUKUMARJHA_track2_report.md`](report/HIMANSHUKUMARJHA_track2_report.md).

---

## The pipeline is blind

No candidate gene list, no disease hypothesis, no MVA gene panel appears anywhere in the ranking code. The string `BUB1B` does not occur in `06_rank.py` at all; the only hardcoded reference to the answer is a clearly fenced post-hoc block of two coordinates that runs after the ranking has been computed, sorted and written to disk, and which has no effect on any score.

```
5,012,204   all records in the VCF
   28,071   PASS, GENCODE v44 CDS +/-10bp, DP>=10, GQ>=30
      229   rare (gnomAD < 1e-3) and protein-altering
      194   after alignment-artefact QC
        1   top-ranked: BUB1B p.Asn1002Lys
```

Ranking combines four independently computed axes:

```
score = 2.0*impact + 1.0*rarity + 1.5*phenotype + 1.5*inheritance_model
```

The phenotype axis is the interesting one. Scored on the proband's eight HPO terms alone, with **no genetic data at all**, *BUB1B* ranks **14th of 5,268 genes** genome-wide, *CEP57* 15th and *TRIP13* 62nd. The three known MVA genes cluster in the top 1.2% of the genome before a single variant is examined.

## How to run it

Requires `bcftools` (`brew install bcftools`) and Python 3. Everything else is fetched by the scripts.

```bash
export HF_TOKEN=hf_...   # an account granted access to the gated dataset
./run_all.sh             # everything, start to finish, about 30 minutes
```

`run_all.sh` runs the stages below in order. Each is also runnable on its own, from any working directory.

| Script | Function | Time |
|---|---|---|
| `00_setup.sh` | directories, GENCODE/HPO references, CDS BED | ~2 min |
| `01_fetch.py` | download VCF, index, phenotype document | ~5 min |
| `02_extract.sh` | VCF to coding working set + genome-wide BAF set | ~6 min |
| `03_vep.py` | VEP REST helper for an arbitrary variant list | library |
| `04_annotate_all.py` | parallel resumable VEP annotation of 28,071 variants | ~14 min |
| `05_phenotype.py` | Resnik phenotype similarity for 5,268 genes | ~2 min |
| `06_rank.py` | blind ranking, artefact QC, final output | ~10 s |
| `07_aneuploidy.py` | mosaic aneuploidy screen from allelic depths | ~1 min |
| `08_secondary.py` | ACMG SF v3.2 secondary findings screen | ~1 s |
| `09_verify.sh` | independent verification of the reported variants | ~10 s |

`04_annotate_all.py` writes one file per batch and skips completed batches, so it is safe to interrupt and rerun.

`09_verify.sh` is the honest-broker check. It pulls the organizers' own `evaluation.py` from the challenge Space, confirms the two reported variants against the raw VCF, re-checks both reference alleles against GRCh38 through the Ensembl sequence API, and scores the submission file, asserting 100 rank points and F-max 1.000.

## Design choices worth defending

**No local VEP cache.** Annotation runs through the Ensembl VEP REST API, trading about 14 minutes of wall clock for roughly 25 GB of disk. That is what keeps the whole analysis inside 762 MB. A diagnostic pipeline needing 100 GB and a cluster is not deployable where undiagnosed patients actually are.

**No FASTQ.** The 84 GB read set was never downloaded. Everything here, including the mosaic aneuploidy screen, is recovered from the 315 MB VCF.

**Artefact QC is stated in terms of biological implausibility.** An unfiltered pass ranked *SERPINA1* above *BUB1B* on 15 rare damaging alleles inside **119 bp**, and *HLA-DQA1* on 6 inside **60 bp**. No one carries that; it is mismapping in segmental duplications. Genes with more than four rare damaging alleles in this single sample are excluded, along with the *HLA* and *MUC* families. *BUB1B* contributes exactly two coding variants in the whole gene, 10.9 kb apart.

**Known failure modes are reported, not hidden.** A false positive sits at rank 2 (a deep intronic *PEX5* deletion that VEP mis-tags as coding) and the report explains it rather than hand-removing it. An earlier version of the aneuploidy analysis was discarded after median-depth quantisation produced spurious structure; the report documents that too.

## Limitations

**Phasing is not established.** No `PGT`/`PID` tags, the alleles are 10,911 bp apart, and there are no parental samples. The trans configuration is inferred from phenotype, not demonstrated. This is the single most important caveat.

Structural and copy number variants are not assessed. Non-coding variation is excluded by construction. The artefact filter would suppress genuine findings in highly polymorphic genes, and did exclude *SERPINA1*. Computational pathogenicity predictions are not functional evidence.

## Data handling

The challenge dataset is **gated and patient-derived**. It is not in this repository and cannot be: `data/`, `out/` and all VCF, FASTQ, BAM and derived intermediate patterns are gitignored, per the Hackathon Rules prohibition on resharing through any channel.

Variant coordinates were transmitted to the Ensembl VEP and sequence REST APIs, both public academic services, for annotation. No genomic or clinical data was sent to any commercial generative AI provider. All challenge data will be deleted from every environment within 30 days of Hackathon close, with confirmation emailed to the organizers.

Generative AI disclosure is in section 10 of the report.

## Acknowledgement

> "This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible."

Submissions and results are released under CC BY 4.0.
