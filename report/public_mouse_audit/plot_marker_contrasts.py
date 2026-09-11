from pathlib import Path
import os,sys,csv
HERE=Path(__file__).resolve().parent
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=HERE
rows=list(csv.DictReader((P/'results/panel_contrasts.tsv').open(),delimiter='\t'))
genes=['Cdkn2a','Cdkn1a','Serpine1','Igfbp2','Il6','Ccl2','Mmp3']
tissues=['gastrocnemius muscle','inguinal adipose tissue']
print(sorted(set(x['tissue'] for x in rows)))
# Use exact exported tissue labels; there must be precisely two.
tissues=['gastrocnemius muscle']+[x for x in sorted(set(r['tissue'] for r in rows)) if x!='gastrocnemius muscle']
cons=[('HH','WT'),('HL1002P','WT'),('HL1002P','HH')]
arr=np.zeros((7,6)); annotations=[]
for i,g in enumerate(genes):
 line=[]
 for j,(t,(n,d)) in enumerate([(t,c) for t in tissues for c in cons]):
  hit=[x for x in rows if x['tissue']==t and x['gene']==g and x['numerator']==n and x['denominator']==d]
  assert len(hit)==1
  r=hit[0];arr[i,j]=float(r['median_ratio_log2_contrast'])
  line.append(f'{arr[i,j]:+.2f}'+(' †' if int(r['loo_matching_directions'])<int(r['loo_total']) else ''))
 annotations.append(line)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,ax=plt.subplots(figsize=(12,7.8),facecolor='white')
fig.subplots_adjust(left=.14,right=.91,top=.78,bottom=.26)
im=ax.imshow(arr,cmap='PuOr_r',vmin=-4,vmax=4,aspect='auto')
ax.set_yticks(range(7),genes)
ax.set_xticks(range(6),['H/H / WT','H/L1002P / WT','H/L1002P / H/H']*2)
ax.tick_params(axis='both',length=0,pad=10)
ax.xaxis.tick_top()
for i in range(7):
 for j in range(6):ax.text(j,i,annotations[i][j],ha='center',va='center',color='white' if abs(arr[i,j])>2.6 else '#18212b',fontsize=11)
ax.axvline(2.5,color='white',lw=8)
for edge in ax.spines.values():edge.set_visible(False)
ax.set_xticks(np.arange(-.5,6,1),minor=True);ax.set_yticks(np.arange(-.5,7,1),minor=True);ax.grid(which='minor',color='white',lw=1);ax.tick_params(which='minor',bottom=False,left=False)
cbar=fig.colorbar(im,ax=ax,fraction=.025,pad=.03);cbar.set_label('Descriptive log₂ contrast')
fig.text(.14,.96,'Marker expression differs by tissue and allele',fontsize=20,weight='bold',color='#13253b')
fig.text(.14,.918,'Public mouse RNA-seq · GSE134780 · 23 samples · no drug-treated arms',fontsize=12,color='#44556a')
fig.text(.32,.84,'Muscle: WT 4 · H/H 3 · H/L1002P 4',ha='center',fontsize=11,weight='bold')
fig.text(.697,.84,'Adipose: 4 per genotype',ha='center',fontsize=11,weight='bold')
notes=[
'Values: log₂[(mean median-ratio normalized count + 1) / (comparison mean + 1)]. Each tissue normalized separately.',
'† Direction changed after at least one single-sample omission with normalization recomputed; not a significance test.',
'Cdkn2a does not distinguish p16/p19. WT muscle Cdkn2a mean = 3 raw counts; muscle Il6 is sparse.',
'Literature-informed exploratory panel. Bulk composition, missing covariates and small groups limit interpretation.',
'Mouse L1002P corresponds to human L1012P, not the child’s Asn1002Lys. No patient or drug-response inference.',
'Data: Sieben et al., JCI 2020 / GEO GSE134780. Full sample values, all contrasts and code accompany this figure.'
]
for i,line in enumerate(notes):fig.text(.08,.195-i*.026,line,fontsize=9.1,color='#354457')
fig.savefig(P/'marker_contrasts.png',dpi=180,facecolor='white')
print('Rendered',P/'marker_contrasts.png')
