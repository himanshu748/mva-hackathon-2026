#!/usr/bin/env bash
# Reduce the whole-genome VCF to the two working sets used downstream.
#
#   out/coding_pass.tsv  high-confidence variants in protein-coding CDS +/-10bp
#                        (input to the annotation and ranking stages)
#   out/baf_raw.tsv      allelic depths at all high-confidence SNVs genome-wide
#                        (input to the mosaic aneuploidy screen)
#
# Requires bcftools and ref/cds.bed from 00_setup.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
VCF=data/WGS_EX2312012_HGWCNDSX7.vcf.gz

for f in "$VCF" ref/cds.bed; do
  [ -s "$f" ] || { echo "missing $f (run 00_setup.sh and 01_fetch.py first)" >&2; exit 1; }
done
command -v bcftools >/dev/null || { echo "bcftools not found (brew install bcftools)" >&2; exit 1; }

echo "Total records in VCF: $(bcftools index --nrecords "$VCF" 2>/dev/null || bcftools view -H "$VCF" | wc -l)"

echo "Extracting coding variants (PASS, DP>=10, GQ>=30)..."
bcftools view -H -f PASS -R ref/cds.bed -i 'FMT/DP>=10 && FMT/GQ>=30' "$VCF" \
  | awk -F'\t' -v OFS='\t' '{split($10,a,":"); print $1,$2,$4,$5,a[1],a[2],a[3]}' \
  > out/coding_pass.tsv
echo "  out/coding_pass.tsv: $(wc -l < out/coding_pass.tsv) variants"

echo "Extracting genome-wide allelic depths for the aneuploidy screen..."
bcftools query -f '%CHROM\t%POS\t[%GT\t%AD\t%DP]\n' \
  -i 'TYPE="snp" && FILTER="PASS" && FMT/DP>=20 && FMT/GQ>=30' "$VCF" \
  > out/baf_raw.tsv
echo "  out/baf_raw.tsv: $(wc -l < out/baf_raw.tsv) SNVs"
