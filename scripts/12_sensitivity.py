"""Post-hoc within-case sensitivity; not independent predictive validation."""
import collections
import itertools
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
rows=json.loads((ROOT/'out/ranking_pre_qc.json').read_text())
base=json.loads((ROOT/'out/ranked_top200.json').read_text());target=base[0]['gene']
het_gt={'0/1','1/0','0|1','1|0'}

def rank(weights,qc=True):
    grouped=collections.defaultdict(list)
    for r in rows:grouped[r['gene']].append(r)
    excluded={g for g,rs in grouped.items() if len(rs)>4 or (g and g.startswith(('HLA-','MUC')))} if qc else set()
    candidates=[]
    for g,rs in grouped.items():
        if g in excluded:continue
        het=[r for r in rs if r['gt'] in het_gt]
        for r in rs:
            model=1.0 if r['gt'] in {'1/1','1|1'} or (r in het and len(het)>=2) else .35
            score=sum(w*v for w,v in zip(weights,[r['impact'],r['rarity'],r['pheno'],model]))
            candidates.append((score,r))
    candidates.sort(key=lambda x:-x[0])
    return [i for i,(_,r) in enumerate(candidates,1) if r['gene']==target]

baseline=(2,1,1.5,1.5)
scenarios=[]
for qc in [True,False]:
    vals=[rank(tuple(w*m for w,m in zip(baseline,mults)),qc) for mults in itertools.product([.75,1,1.25],repeat=4)]
    scenarios.append({'qc':qc,'settings':len(vals),'first_target_rank_range':[min(r[0] for r in vals),max(r[0] for r in vals)],
       'second_target_rank_range':[min(r[1] for r in vals),max(r[1] for r in vals)],
       'both_in_top3':sum(max(r[:2])<=3 for r in vals),'both_in_top10':sum(max(r[:2])<=10 for r in vals)})
out={'scope':'post-hoc within-case sensitivity; no held-out cases','target_gene':target,
 'baseline_qc_ranks':rank(baseline),'baseline_no_qc_ranks':rank(baseline,False),'weight_grid':scenarios,
 'single_axis_ablation':{name:rank(tuple(0 if j==i else w for j,w in enumerate(baseline))) for i,name in enumerate(['impact','rarity','phenotype','inheritance'])}}
(ROOT/'report/sensitivity_summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
