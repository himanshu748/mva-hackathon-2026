# MVA Hackathon 2026

This repository contains retrospective variant prioritisation for Track 1 and a preclinical dasatinib-plus-quercetin research proposal for Track 2.

The original analysis checked known MVA genes before building a genome-wide ranking. The ranking is therefore an unblinded retrospective analysis. It places two BUB1B candidates first and third among 194 retained variants. The organizer's live leaderboard, checked 7 September 2026, records the original Track 1 submission at **100.0 rank points and F-max 1.000**. That score does not establish phase or functional effects.

| Candidate | GRCh38 | Interpretation |
|---|---|---|
| BUB1B p.Leu737Ter | chr15:40209701 T>G | Predicted loss of function; no patient RNA or protein assay |
| BUB1B p.Asn1002Lys | chr15:40220612 T>G | Missense candidate; residual activity unmeasured |

Both variants are heterozygous. Their trans configuration remains unproven. Both remain in the top three across 162 retrospective sensitivity runs: 81 weight combinations with gene exclusions enabled and disabled. This measures stability within this case, not performance on independent cases.

## Reports

- [Track 1 methods and limitations](report/HIMANSHUKUMARJHA_track1_report.md)
- [Track 2 preclinical proposal](report/HIMANSHUKUMARJHA_track2_report.md)
- [Pitch narration](report/track2_pitch_script.md)
- [AI and external-service disclosure](report/data_handling_disclosure.md)
- [Sensitivity results](report/sensitivity_summary.json)

Track 2 proposes testing selective senescent-cell clearance. Genetic mouse experiments and small adult drug studies motivate the work. They do not establish safety or efficacy in this child. No pediatric treatment schedule is proposed.

## Reproduction

Requires Python 3.10+, bcftools, curl, and the Python dependency below. Access to the gated challenge dataset is required.

```bash
python3 -m pip install -r requirements.txt
export HF_TOKEN=...  # your authorized Hugging Face access token
./run_all.sh
```

To validate and reuse an existing complete local annotation cache:

```bash
./run_all.sh --cached
python3 -m unittest discover -s tests -v
```

The annotation cache is bound to exact variant inputs, request options, and batch hashes. Missing, duplicate, unexpected, or altered responses fail validation. Exhausted annotation requests stop the run. A legacy cache can be adopted explicitly with `python3 scripts/04_annotate_all.py --adopt-existing-cache`; this validates its contents but cannot reconstruct its historical service release.

The phenotype profile can be supplied as a JSON list of HPO identifiers using `python3 scripts/05_phenotype.py --hpo-file profile.json`. The default profile is the challenge profile. The scoring formula is `2*impact + rarity + 1.5*phenotype + 1.5*inheritance`. Phenotype similarity uses directional patient-to-gene best-match mean Resnik similarity.

Reference sources and API outputs can change. Local manifests record hashes; the historical annotation release is unknown. The gated input and annotation cache are not distributed, so this repository alone cannot recreate every historical byte.

`09_verify.sh` checks the submitted candidates against the local VCF and ranking, then runs a pinned copy of the organizer scoring function using the proposed pair as its comparison set. This is a format and consistency self-check, not independent answer-key validation. The organizer leaderboard is the separate source for the submitted score.

## Limits

The coding-region filter excludes most noncoding variation. Structural and copy-number variants are not assessed. Gene exclusions are heuristics that can remove real findings. The PEX5 candidate at rank two has conflicting transcript/consequence evidence and requires review. Allele-depth exploration does not establish a mosaic fraction. The secondary-variant lookup is incomplete and does not establish a negative clinical secondary-findings result.

The gated data, intermediate tables, and annotation cache must not be committed or redistributed. Dataset handling and AI use are described in the linked disclosure. Tool outputs containing candidate and phenotype information were available to AI assistants; the earlier statement that no data reached a commercial AI provider has been withdrawn.

## Acknowledgement

> This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.

Submissions and results are released under CC BY 4.0.
