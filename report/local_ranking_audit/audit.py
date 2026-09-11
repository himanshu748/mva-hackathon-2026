"""Offline transcript-selection audit. No remote annotations or clinical classification."""
from pathlib import Path
import argparse, collections, hashlib, json, math, pickle, sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True, help='Existing private analysis checkout')
ROOT=parser.parse_args().root.resolve()
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from annotation_cache import validate_cache, digest
inputs, hashes=validate_cache(ROOT)
meta=json.loads((ROOT/'out/pheno_manifest.json').read_text())
assert digest(ROOT/'out/pheno_scores.pkl')==meta['scores_sha256']
for name,expected in meta['references'].items(): assert digest(ROOT/'ref'/name)==expected
PHENO=pickle.loads((ROOT/'out/pheno_scores.pkl').read_bytes())
GT={}
for line in (ROOT/'out/coding_pass.tsv').read_text().splitlines():
    f=line.split('\t');GT[f'{f[0]} {f[1]} . {f[2]} {f[3]} . . .']=f[4]
HIGH={'transcript_ablation','splice_acceptor_variant','splice_donor_variant','stop_gained','frameshift_variant','stop_lost','start_lost'}
MOD={'missense_variant','inframe_insertion','inframe_deletion','protein_altering_variant'}
def tier(ts):
    return [t for t in ts if t.get('mane_select')] or [t for t in ts if t.get('canonical')] or ts
def impact(t):
    c=set(t.get('consequence_terms',[]))
    if c&HIGH:return 1.0
    if c&MOD:return .55+.15*(t.get('sift_prediction')=='deleterious')+.15*(t.get('polyphen_prediction')=='probably_damaging')
    return 0
def af(v):
    alt=v.get('allele_string','/').split('/')[-1];vals=[]
    for cv in v.get('colocated_variants',[]):
        f=(cv.get('frequencies') or {}).get(alt) or {}
        vals.extend(f[k] for k in ('gnomadg','gnomade') if f.get(k) is not None)
    return max(vals) if vals else None
def row(v,t,a):
    i=impact(t)
    if not i or (a is not None and a>1e-3):return None
    return {'key':v['input'],'gene':t.get('gene_symbol'),'transcript':t.get('transcript_id'),
            'consequence':t.get('consequence_terms',[]),'impact':i,'af':a,
            'rarity':1 if a is None else min(1,math.log10(1e-3/max(a,1e-7))/4),
            'pheno':PHENO.get(t.get('gene_symbol'),0),'gt':GT[v['input']]}
branches={x:[] for x in ['original','per_gene','per_gene_consequence']}
counts=collections.Counter();conflicts=[]
for file in sorted((ROOT/'out/vep_parts').glob('*.json')):
 for v in json.loads(file.read_text()):
    if v['input'] not in GT:continue
    counts['cached_inputs']+=1
    counts['multiallelic_inputs']+=(',' in v['input'].split()[4])
    ts=v.get('transcript_consequences',[]);sel=tier(ts)
    if not sel:continue
    a=af(v);r=row(v,sel[0],a)
    if r:branches['original'].append(r)
    genes=collections.defaultdict(list)
    for t in ts:
        if t.get('gene_symbol'):genes[t['gene_symbol']].append(t)
    counts['multiple_gene_inputs']+=len(genes)>1
    for gene,gts in genes.items():
        pref=tier(gts)
        for branch,t in [('per_gene',pref[0]),('per_gene_consequence',max(pref,key=impact))]:
            r=row(v,t,a)
            if r:branches[branch].append(r)
        if gene=='PEX5' and any(impact(t) for t in pref):
            conflicts.append({'key_hash':hashlib.sha256(v['input'].encode()).hexdigest()[:12],
                'preferred_transcripts':[{'id':t.get('transcript_id'),'mane':t.get('mane_select'),
                 'consequence':t.get('consequence_terms'),'impact':impact(t)} for t in pref]})
def rank(rows,qc):
    grouped=collections.defaultdict(list)
    for r in rows:grouped[r['gene']].append(r)
    excluded={g for g,rs in grouped.items() if len(rs)>4 or (g and g.startswith(('HLA-','MUC')))} if qc else set()
    results=[]
    for g,rs in grouped.items():
        if g in excluded:continue
        het=[r for r in rs if r['gt'] in {'0/1','1/0','0|1','1|0'}]
        for r in rs:
            model=1 if r['gt'] in {'1/1','1|1'} or (r in het and len(het)>=2) else .35
            results.append(dict(r,score=2*r['impact']+r['rarity']+1.5*r['pheno']+1.5*model))
    # Original input order breaks ties, as in 06_rank.py.
    positions={(r['key'],r['gene']):i for i,r in enumerate(rows)}
    results.sort(key=lambda r:(-r['score'],positions[(r['key'],r['gene'])]))
    return results
baseline=rank(branches['original'],True)
saved=json.loads((ROOT/'out/ranked_top200.json').read_text())
assert len(baseline)==len(saved)
assert all(a['key']==b['input'] and a['gene']==b['gene'] and abs(a['score']-b['score'])<1e-10 for a,b in zip(baseline,saved))
summaries={}
original_keys={(r['key'],r['gene']) for r in branches['original']}
for name,rs in branches.items():
    summaries[name]={}
    for qc in (True,False):
        ranked=rank(rs,qc)
        summaries[name][str(qc)]={'retained':len(ranked),'bub1b_ranks':[i for i,r in enumerate(ranked,1) if r['gene']=='BUB1B'],
          'top10':[{'rank':i,'gene':r['gene'],'score':r['score'],'consequence':r['consequence']} for i,r in enumerate(ranked[:10],1)],
          'added_gene_candidates':sum((r['key'],r['gene']) not in original_keys for r in ranked),
          'added_details':[dict(rank=i,gene=r['gene'],transcript=r['transcript'],consequence=r['consequence'],
              gt=r['gt'],af=r['af'],score=r['score'],key_hash=hashlib.sha256(r['key'].encode()).hexdigest()[:12])
              for i,r in enumerate(ranked,1) if (r['key'],r['gene']) not in original_keys]}
out={'cache_inputs':len(inputs),'cache_batches':len(hashes),'counts':dict(counts),
     'baseline_exactly_reproduced':len(baseline),'branches':summaries,'pex5_transcript_review':conflicts,
     'interpretation':'Post-hoc local method audit; not new pathogenicity evidence or independent validation.'}
(OUT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
