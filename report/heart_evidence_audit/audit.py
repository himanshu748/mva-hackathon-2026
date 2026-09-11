#!/usr/bin/env python3
"""Audit published summary statistics; does not estimate drug efficacy."""
from pathlib import Path
import csv,gzip,json,math,hashlib
ROOT=Path(__file__).resolve().parent
PANEL=('Cdkn2a','Cdkn1a','Serpine1','Igfbp2','Il6','Ccl2','Mmp3')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_author(path):
 with gzip.open(path,'rt') as f:rows=list(csv.DictReader(f))
 if not rows or not {'gene','log2FC','pvalue','padj'} <= rows[0].keys():raise ValueError('Missing fields')
 if len({r['gene'] for r in rows})!=len(rows):raise ValueError('Duplicate gene symbols')
 for r in rows:
  if not r['gene']:raise ValueError('Empty gene')
  for k in ['log2FC','pvalue','padj']:
   if r[k] in ('NA','NaN',''):continue
   v=float(r[k])
   if not math.isfinite(v):raise ValueError('Nonfinite number')
   if k!='log2FC' and not 0<=v<=1:raise ValueError('Invalid probability')
 return rows
def direction(x):return 'higher' if x>1e-12 else ('lower' if x< -1e-12 else 'zero')
def write_csv(path,rows):
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def main():
 rows=read_author(ROOT/'inputs/GSE277997_H_v_WT.csv.gz');by={r['gene']:r for r in rows}
 results=[]
 for g in PANEL:
  r=by.get(g); present=r is not None
  usable=present and r['log2FC'] not in ('NA','NaN','')
  results.append({'gene':g,'reported':present,'author_log2FC':r['log2FC'] if present else '', 'author_pvalue':r['pvalue'] if present else '', 'author_padj':r['padj'] if present else '', 'author_padj_below_005':float(r['padj'])<.05 if present and r['padj'] not in ('NA','NaN','') else '', 'direction':direction(float(r['log2FC'])) if usable else 'unreported','interpretation':'Published summary estimate; not independently refitted'})
 write_csv(ROOT/'panel_results.csv',results)
 with (ROOT/'inputs/prior_panel_contrasts.tsv').open() as f:old=list(csv.DictReader(f,delimiter='\t'))
 old=[r for r in old if r['numerator']=='HH' and r['denominator']=='WT']; assert len(old)==14
 panel={r['gene']:r for r in results}; comparisons=[]
 for r in old:
  h=panel[r['gene']]; comparisons.append({'gene':r['gene'],'earlier_tissue':r['tissue'],'earlier_log2_contrast':r['median_ratio_log2_contrast'],'earlier_direction':r['median_ratio_direction'],'heart_author_log2FC':h['author_log2FC'],'heart_direction':h['direction'],'same_direction':r['median_ratio_direction']==h['direction'],'earlier_low_count_flag':r['low_count_tissue_mean_below_10'],'heart_author_padj':h['author_padj']})
 write_csv(ROOT/'cross_tissue_directions.csv',comparisons)
 qc={'author_table_rows':len(rows),'unique_gene_symbols':len(by),'pvalue_at_least_005':sum(float(r['pvalue'])>=.05 for r in rows if r['pvalue'] not in ('NA','NaN','')),'panel_present':sum(r['reported'] for r in results),'panel_higher':sum(r['direction']=='higher' for r in results),'panel_author_adjusted_p_below_005':sum(r['author_padj_below_005'] is True for r in results),'direction_agreement':{t:sum(r['same_direction'] for r in comparisons if r['earlier_tissue']==t) for t in sorted({r['earlier_tissue'] for r in comparisons})},'metadata_description_significant_only_is_inaccurate':True,'independent_sex_adjustment_performed':False,'drug_effect_estimated':False,'raw_counts_reanalysis':False,'input_sha256':sha(ROOT/'inputs/GSE277997_H_v_WT.csv.gz'),'previous_results_sha256':sha(ROOT/'inputs/prior_panel_contrasts.tsv')}
 (ROOT/'summary.json').write_text(json.dumps(qc,indent=2)+'\n');print(json.dumps(qc,indent=2))
if __name__=='__main__':main()
