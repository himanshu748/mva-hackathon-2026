"""Screen for mosaic whole-chromosome aneuploidy using the VCF alone.

Mosaic variegated aneuploidy is defined by its cellular phenotype, but the
challenge ships no BAM and the FASTQ set is 84 GB. Two signals are recoverable
from allelic depths in the VCF:

  1. B-allele frequency at heterozygous SNVs. A disomic chromosome gives one
     band at 0.5. A population of cells carrying an extra copy splits het sites
     into two bands, and a *mosaic* population present in a fraction f of cells
     shifts them to 1/(2+f) and (1+f)/(2+f), an intermediate, chromosome-wide
     displacement proportional to f.
  2. Normalised read depth, which tracks copy number directly: a mosaic gain in
     a fraction f of cells raises relative depth to 1 + f/2.

Because the two axes respond to the same underlying f through different
arithmetic, agreement between them is meaningful and disagreement is diagnostic
of technical bias.

NOTE ON THE DEPTH STATISTIC. An earlier version of this analysis used the
*median* depth per chromosome. Read depths are integers, so the median is
heavily quantised: chromosome-level ratios collapsed onto a handful of discrete
values (44/44, 45/44, 46/44, 47/44) and manufactured structure that was not in
the data. This version uses the mean, which is continuous. The lesson
generalises: do not use a median of a low-cardinality integer distribution as a
continuous summary statistic.

CAVEAT. This is a single sample with no matched control cohort. GC content and
mappability vary systematically across chromosomes and produce depth and BAF
deviations that mimic low-level mosaicism, particularly on the GC-rich and
acrocentric chromosomes. Nothing here should be read as a positive finding
without GC correction against a reference panel, or confirmation by karyotype.
"""
import collections
import os
import statistics as st

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

MIN_DEPTH = 30      # per-site depth floor for a BAF estimate to be meaningful
MIN_SITES = 1000    # minimum het sites before a chromosome is summarised

het = collections.defaultdict(list)
dep = collections.defaultdict(list)

for line in open("out/baf_raw.tsv"):
    c = line.rstrip("\n").split("\t")
    if len(c) < 5 or not c[0].isdigit():   # autosomes only
        continue
    try:
        ref, alt = (int(x) for x in c[3].split(",")[:2])
        dp = int(c[4])
    except ValueError:
        continue
    dep[c[0]].append(dp)
    if c[2] in ("0/1", "0|1", "1|0") and ref + alt >= MIN_DEPTH:
        het[c[0]].append(alt / (ref + alt))

genome_mean = st.mean([d for v in dep.values() for d in v])

rows = []
for chrom in sorted(het, key=int):
    b = het[chrom]
    if len(b) < MIN_SITES:
        continue
    # Fraction of het sites displaced from the diploid band. A mosaic gain
    # pushes sites symmetrically outward, so this is direction-agnostic.
    off = sum(1 for x in b if x < 0.40 or x > 0.60) / len(b)
    rows.append((chrom, len(b), st.mean(dep[chrom]) / genome_mean, off))

mu_d, sd_d = st.mean([r[2] for r in rows]), st.stdev([r[2] for r in rows])
mu_o, sd_o = st.mean([r[3] for r in rows]), st.stdev([r[3] for r in rows])

print(f"genome-wide mean depth: {genome_mean:.1f}x")
print(f"heterozygous SNVs analysed: {sum(r[1] for r in rows):,}\n")
print(f"{'CHR':<5}{'HET SNVs':>10}{'REL DEPTH':>11}{'z':>8}{'BAF OFF-BAND':>14}{'z':>8}   FLAG")

flagged = []
for chrom, n, rel, off in rows:
    zd, zo = (rel - mu_d) / sd_d, (off - mu_o) / sd_o
    flag = ""
    if zd > 2.5 or zo > 2.5:
        flag = "<<< OUTLIER"
        flagged.append((chrom, rel, off))
    elif zd > 1.5 or zo > 1.5:
        flag = "<   watch"
        flagged.append((chrom, rel, off))
    print(f"{chrom:<5}{n:>10,}{rel:>11.4f}{zd:>8.2f}{off:>14.4f}{zo:>8.2f}   {flag}")

print(f"\nbaseline: relative depth {mu_d:.3f}, off-band fraction {mu_o:.3f}")
print(f"a constitutional (non-mosaic) trisomy would show relative depth 1.500; "
      f"observed maximum is {max(r[2] for r in rows):.4f}")

if flagged:
    print("\nImplied mosaic fraction if the depth signal were biological (f = 2*(rel-1)):")
    for chrom, rel, off in flagged:
        f = 2 * (rel - 1)
        if f <= 0:
            continue
        print(f"  chr{chrom}: f = {f:.2f} -> predicted BAF bands at "
              f"{1/(2+f):.2f} and {(1+f)/(2+f):.2f} (observed off-band fraction {off:.3f})")

print("\nInterpretation: concordance between the two axes is necessary but not")
print("sufficient. GC content and mappability covary with both, and the flagged")
print("chromosomes here are GC-rich and/or acrocentric. Treat any signal as a")
print("candidate requiring GC-corrected depth against a reference panel, or")
print("confirmation by karyotype or FISH. Blood is frequently among the least")
print("affected tissues in MVA, so a null result constrains the mosaic fraction")
print("in this sample rather than excluding aneuploidy in the individual.")
