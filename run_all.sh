#!/usr/bin/env bash
# --cached verifies existing local inputs without repeating annotation calls.
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "--cached" ]]; then
  python3 scripts/04_annotate_all.py
elif [[ -z "${1:-}" ]]; then
  : "${HF_TOKEN:?set HF_TOKEN for an account granted access to the dataset}"
  bash scripts/00_setup.sh
  python3 scripts/01_fetch.py
  bash scripts/02_extract.sh
  python3 scripts/04_annotate_all.py
else
  echo "Usage: ./run_all.sh [--cached]" >&2; exit 2
fi
python3 scripts/05_phenotype.py
python3 scripts/06_rank.py
python3 scripts/07_aneuploidy.py
python3 scripts/08_secondary.py
bash scripts/09_verify.sh
python3 scripts/12_sensitivity.py
