"""Local candidate/CSV self-check, distinct from the official leaderboard."""
import csv
import hashlib
import importlib.util
import json
import subprocess
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
path=ROOT/'report/HIMANSHUKUMARJHA_bub1b-compound-het.csv'
with path.open() as f:rows=list(csv.DictReader(f))
assert len(rows)==3, 'Expected curated pair and two individual rows'
pair=frozenset((rows[0]['chrom_'+s],int(rows[0]['pos_'+s]),rows[0]['ref_'+s],rows[0]['alt_'+s]) for s in ['1','2'])
ranked=json.loads((ROOT/'out/ranked_top200.json').read_text())
for chrom,pos,ref,alt in pair:
    inp=f'{chrom.removeprefix("chr")} {pos} . {ref} {alt} . . .'
    assert any(x['input']==inp for x in ranked[:3]), 'Curated candidate is not in ranked top three'
    result=subprocess.run(['bcftools','query','-r',f'{chrom.removeprefix("chr")}:{pos}-{pos}',
        '-f','%REF\t%ALT\t%FILTER[\t%GT]\n',str(ROOT/'data/WGS_EX2312012_HGWCNDSX7.vcf.gz')],
        capture_output=True,text=True,check=True)
    assert any(x.split('\t')[:4]==[ref,alt,'PASS','0/1'] for x in result.stdout.splitlines()), 'Candidate VCF mismatch'
rev=(ROOT/'scripts/evaluator_revision.txt').read_text().strip()
url=f'https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/resolve/{rev}/evaluation.py'
source=urllib.request.urlopen(url,timeout=30).read();dest=ROOT/'scripts/_organizer_evaluation.py';dest.write_bytes(source)
spec=importlib.util.spec_from_file_location('organizer_eval',dest);module=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=module;spec.loader.exec_module(module)
result=module.score_proband('PROBAND01',module.load_submission(str(path))['PROBAND01'],pair)
assert result.rank_points==100 and result.f_max==1
summary={'check':'CSV/VCF and candidate-based scoring self-check; not organizer answer-key validation',
         'candidate_count':len(pair),'rank_points':result.rank_points,'f_max':result.f_max,
         'csv_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'evaluator_revision':rev}
(ROOT/'report/local_verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
