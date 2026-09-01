#!/usr/bin/env bash
# Full pipeline, start to finish. Requires bcftools, Python 3 and HF_TOKEN.
set -euo pipefail
cd "$(dirname "$0")"
: "${HF_TOKEN:?set HF_TOKEN to a Hugging Face token with access to the gated dataset}"

bash   scripts/00_setup.sh        # directories + reference data + CDS BED
python3 scripts/01_fetch.py       # challenge data (318 MB, no FASTQ)
bash   scripts/02_extract.sh      # VCF -> coding and BAF working sets
python3 scripts/04_annotate_all.py # VEP annotation (resumable, ~14 min)
python3 scripts/05_phenotype.py   # HPO Resnik similarity for all genes
python3 scripts/06_rank.py        # blind ranking -> out/ranked_top200.json
python3 scripts/07_aneuploidy.py  # mosaic aneuploidy screen
python3 scripts/08_secondary.py   # ACMG SF v3.2 screen
bash   scripts/09_verify.sh       # independent verification + scoring
