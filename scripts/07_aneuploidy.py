"""Detect mosaic whole-chromosome aneuploidy from the VCF alone.

MVA is defined by mosaic aneuploidy, but the challenge ships no BAM and the
FASTQ set is 84 GB. Two signals recoverable from allelic depths in the VCF:

  1. B-allele frequency (BAF) spread at heterozygous SNVs. A disomic
     chromosome gives one band at 0.5. A cell population carrying an extra or
     missing copy pulls het sites away from 0.5, and a *mosaic* population
     produces an intermediate, chromosome-wide shift proportional to the
     fraction of aneuploid cells.
  2. Normalised median read depth, which tracks copy number directly.

Reported as a per-chromosome z-score against the genome-wide distribution.
"""
import collections, statistics as st

het = collections.defaultdict(list)
dep = collections.defaultdict(list)
for line in open("out/baf_raw.tsv"):
    c = line.rstrip("\n").split("\t")
    if len(c) < 5: continue
    chrom, gt, ad, dp = c[0], c[2], c[3], c[4]
    if chrom in ("X", "Y", "MT") or not chrom.isdigit(): continue
    try:
        ref, alt = (int(x) for x in ad.split(",")[:2]); dpi = int(dp)
    except ValueError:
        continue
    if dpi >= 20: dep[chrom].append(dpi)
    if gt in ("0/1", "0|1", "1|0") and ref + alt >= 20:
        het[chrom].append(alt / (ref + alt))

gw_dep = st.median([d for v in dep.values() for d in v])
rows = []
for chrom in sorted(het, key=int):
    b = het[chrom]
    if len(b) < 1000: continue
    spread = st.median([abs(x - 0.5) for x in b])      # 0 = clean disomy
    rows.append((chrom, len(b), st.median(b), spread,
                 st.median(dep[chrom]) / gw_dep))

sp = [r[3] for r in rows]; mu_s, sd_s = st.mean(sp), st.stdev(sp)
dr = [r[4] for r in rows]; mu_d, sd_d = st.mean(dr), st.stdev(dr)

print(f"genome-wide median depth: {gw_dep:.0f}x   het SNVs analysed: {sum(r[1] for r in rows):,}\n")
print(f"{'CHR':<5}{'HET SNVs':>10}{'medBAF':>9}{'SPREAD':>9}{'z(spread)':>11}{'REL DEPTH':>11}{'z(depth)':>10}  FLAG")
for chrom, n, medb, spread, rel in rows:
    zs, zd = (spread - mu_s) / sd_s, (rel - mu_d) / sd_d
    flag = ""
    if abs(zs) > 2.5 or abs(zd) > 2.5: flag = "<<< OUTLIER"
    elif abs(zs) > 1.5 or abs(zd) > 1.5: flag = "<  watch"
    print(f"{chrom:<5}{n:>10,}{medb:>9.3f}{spread:>9.4f}{zs:>11.2f}{rel:>11.3f}{zd:>10.2f}  {flag}")
print("\nInterpretation: a constitutional (non-mosaic) trisomy would show relative depth ~1.5")
print("and a bimodal BAF at ~0.33/0.67. A low-level mosaic shows a milder chromosome-wide")
print("shift in both axes. Blood is often the least-affected tissue in MVA, so a negative")
print("result here constrains the mosaic fraction in blood rather than excluding aneuploidy.")
