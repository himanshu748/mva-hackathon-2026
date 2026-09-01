#!/usr/bin/env bash
# Reproducible verification of the Track 1 submission. Run from the repo root.
set -euo pipefail
VCF=data/WGS_EX2312012_HGWCNDSX7.vcf.gz
CSV=out/HIMANSHUKUMARJHA_bub1b-compound-het.csv

echo "== VCF records =="
bcftools view -H -r 15:40209701,15:40220612 "$VCF"

echo "== GRCh38 reference bases (Ensembl) =="
for p in 40209701 40220612; do
  printf "  15:%s ref=%s\n" "$p" \
    "$(curl -s "https://rest.ensembl.org/sequence/region/human/15:$p..$p?coord_system_version=GRCh38;content-type=text/plain")"
done

echo "== Score against the organizers' own evaluation.py =="
curl -sL "https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/resolve/main/evaluation.py" \
  -o scripts/_organizer_evaluation.py
python3 - "$CSV" <<'PY'
import sys; sys.path.insert(0, "scripts")
from _organizer_evaluation import load_submission, score_proband
rows = load_submission(sys.argv[1])["PROBAND01"]
gt = frozenset([("chr15",40209701,"T","G"), ("chr15",40220612,"T","G")])
r = score_proband("PROBAND01", rows, gt)
print(f"  rank_points={r.rank_points}  f_max={r.f_max:.3f}  full_match_rank={r.full_match_rank}")
assert r.rank_points == 100.0 and r.f_max == 1.0, "submission does not score perfectly"
print("  OK")
PY
