"""Resnik phenotype similarity: score every gene against the proband's HPO profile.

Ontology-aware, so a gene annotated with a parent term (e.g. "Embryonal neoplasm")
still gets credit for the proband's "Rhabdomyosarcoma".
"""
import os, sys as _s; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))  # run from repo root
import collections, json, math, pickle

PROBAND_HPO = {
    "HP:0002859": "Rhabdomyosarcoma",
    "HP:0000121": "Nephrocalcinosis",
    "HP:0004322": "Short stature",
    "HP:0001508": "Failure to thrive",
    "HP:0003202": "Skeletal muscle atrophy",
    "HP:0001622": "Premature birth",
    "HP:0001518": "Small for gestational age",
    "HP:0200067": "Recurrent spontaneous abortion",
}

# --- parse ontology ---
parents, obsolete = collections.defaultdict(set), set()
tid = None
for line in open("ref/hp.obo"):
    line = line.rstrip("\n")
    if line == "[Term]": tid = None
    elif line.startswith("id: HP:"): tid = line[4:]
    elif line.startswith("is_a: ") and tid: parents[tid].add(line[6:16])
    elif line.startswith("is_obsolete: true") and tid: obsolete.add(tid)

def ancestors(t, _cache={}):
    if t in _cache: return _cache[t]
    seen, stack = {t}, [t]
    while stack:
        for p in parents.get(stack.pop(), ()):
            if p not in seen: seen.add(p); stack.append(p)
    _cache[t] = seen
    return seen

# --- gene -> HPO annotations ---
gene_terms = collections.defaultdict(set)
with open("ref/genes_to_phenotype.txt") as f:
    next(f)
    for line in f:
        c = line.split("\t")
        if len(c) > 2 and c[2].startswith("HP:") and c[2] not in obsolete:
            gene_terms[c[1]].add(c[2])
print(f"genes with HPO annotations: {len(gene_terms):,}")

# --- information content from gene annotation frequency ---
freq = collections.Counter()
for terms in gene_terms.values():
    closure = set()
    for t in terms: closure |= ancestors(t)
    freq.update(closure)
N = len(gene_terms)
IC = {t: -math.log(c / N) for t, c in freq.items() if c > 0}

def resnik(pt, gene):
    """Best-match-average Resnik: for each proband term, the most informative
    common ancestor shared with any of the gene's annotated terms."""
    ga = set()
    for t in gene_terms[gene]: ga |= ancestors(t)
    total = 0.0
    for p in pt:
        pa = ancestors(p)
        common = pa & ga
        total += max((IC.get(c, 0.0) for c in common), default=0.0)
    return total / len(pt)

scores = {g: resnik(list(PROBAND_HPO), g) for g in gene_terms}
pickle.dump(scores, open("out/pheno_scores.pkl", "wb"))

ranked = sorted(scores.items(), key=lambda x: -x[1])
print(f"\nTop 15 genes in the genome by phenotype match to the proband's 8 HPO terms:")
for i, (g, s) in enumerate(ranked[:15], 1):
    print(f"  {i:2d}. {g:<12} {s:.3f}")
bub = [i for i, (g, _) in enumerate(ranked, 1) if g == "BUB1B"]
print(f"\nBUB1B phenotype rank: {bub[0]} of {len(ranked):,}  (score {scores['BUB1B']:.3f})")
for g in ("CEP57", "TRIP13"):
    r = [i for i, (x, _) in enumerate(ranked, 1) if x == g]
    print(f"{g} phenotype rank: {r[0] if r else 'n/a'}  (score {scores.get(g, 0):.3f})")
