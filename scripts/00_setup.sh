#!/usr/bin/env bash
# Create the working directories and build the reference files the pipeline needs.
# All sources are public. Total download roughly 64 MB. Safe to rerun: existing
# files are left alone.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data out ref out/vep_parts

fetch () {  # url, destination
  if [ -s "$2" ]; then echo "  have $(basename "$2")"; else
    echo "  fetching $(basename "$2")"; curl -sL -o "$2" "$1"
  fi
}

echo "Reference data:"
fetch "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_44/gencode.v44.basic.annotation.gtf.gz" ref/gencode.gtf.gz
fetch "https://purl.obolibrary.org/obo/hp.obo" ref/hp.obo
fetch "https://purl.obolibrary.org/obo/hp/hpoa/genes_to_phenotype.txt" ref/genes_to_phenotype.txt

if [ -s ref/cds.bed ]; then
  echo "  have cds.bed"
else
  echo "Building protein-coding CDS BED (+/-10bp for splice sites)..."
  python3 - <<'PY'
import gzip, re, collections
pat = re.compile(r'gene_name "([^"]+)"')
iv, n = collections.defaultdict(list), 0
with gzip.open("ref/gencode.gtf.gz", "rt") as f:
    for line in f:
        if line[0] == "#": continue
        c = line.split("\t")
        if c[2] != "CDS" or 'gene_type "protein_coding"' not in c[8]: continue
        m = pat.search(c[8])
        if not m: continue
        # The challenge VCF uses unprefixed contig names, so strip "chr".
        chrom = c[0][3:] if c[0].startswith("chr") else c[0]
        iv[chrom].append((max(0, int(c[3]) - 11), int(c[4]) + 10, m.group(1)))
        n += 1
print(f"  CDS features read: {n:,}")
total = 0
with open("ref/cds.bed", "w") as out:
    for chrom in iv:
        rows = sorted(iv[chrom])
        cs, ce, genes = rows[0][0], rows[0][1], {rows[0][2]}
        for s, e, g in rows[1:]:
            if s <= ce:
                ce = max(ce, e); genes.add(g)
            else:
                out.write(f"{chrom}\t{cs}\t{ce}\t{','.join(sorted(genes))}\n"); total += 1
                cs, ce, genes = s, e, {g}
        out.write(f"{chrom}\t{cs}\t{ce}\t{','.join(sorted(genes))}\n"); total += 1
print(f"  merged regions: {total:,}")
PY
  sort -k1,1 -k2,2n ref/cds.bed -o ref/cds.bed
  awk '{b+=$3-$2} END{printf "  bases covered: %.1f Mb\n", b/1e6}' ref/cds.bed
fi
echo "Setup complete."
