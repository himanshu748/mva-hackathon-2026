#!/usr/bin/env python3
"""Descriptive GSE134780 audit; no hypothesis tests or treatment inference.

Requires Python 3 and NumPy. Run --test for integrity/formula tests, then provide
--counts, --metadata, --plan, --receipt, and --out (see README for an example).
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
import math
import platform
from pathlib import Path
import sys
import numpy as np

PANEL = ('Cdkn2a', 'Cdkn1a', 'Serpine1', 'Igfbp2', 'Il6', 'Ccl2', 'Mmp3')
CONTRASTS = (('HH', 'WT'), ('HL1002P', 'WT'), ('HL1002P', 'HH'))
TISSUES = ('gastrocnemius muscle', 'fat (IAT)')
EXPECTED_N = {'gastrocnemius muscle': {'WT': 4, 'HL1002P': 4, 'HH': 3},
              'fat (IAT)': {'WT': 4, 'HL1002P': 4, 'HH': 4}}
ZERO_TOL = 1e-12
EXPECTED_COUNT_SHA256 = 'f12a73805eb3aaf95d666e78756def647a11e95e37bd007dda580bc08ec77cba'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_labels(labels, name):
    if not labels or any(not x or not x.strip() for x in labels):
        raise ValueError(f'{name}: empty label(s)')
    if len(set(labels)) != len(labels):
        raise ValueError(f'{name}: duplicate labels')


def validate_counts(counts):
    a = np.asarray(counts, dtype=float)
    if a.ndim != 2 or not a.size:
        raise ValueError('Counts must be a nonempty 2D matrix')
    if not np.isfinite(a).all():
        raise ValueError('Counts contain missing/nonfinite values')
    if (a < 0).any() or not np.equal(a, np.floor(a)).all():
        raise ValueError('Counts must be integer and nonnegative')
    if (a >= 2**53).any():
        raise ValueError('Count exceeds exact integer representation')
    if not (a.sum(axis=0) > 0).all():
        raise ValueError('A sample has zero library total')
    return a


def align_metadata(labels, records):
    unique_labels(labels, 'count sample labels')
    unique_labels([r['title'] for r in records], 'metadata sample labels')
    lookup = {r['title']: r for r in records}
    if set(labels) != set(lookup):
        raise ValueError(f'Metadata mismatch: missing={set(labels)-set(lookup)}, extra={set(lookup)-set(labels)}')
    return [lookup[label] for label in labels]


def load_inputs(count_path, metadata_path):
    with gzip.open(count_path, 'rt', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        if header[0] != 'gene_symbol':
            raise ValueError('Expected gene_symbol first column')
        genes, values = [], []
        for row in reader:
            if len(row) != len(header):
                raise ValueError('Ragged/missing count row')
            genes.append(row[0])
            values.append([float(x) for x in row[1:]])
    unique_labels(genes, 'gene symbols')
    labels = header[1:]
    with open(metadata_path, newline='') as f:
        metadata = [r for r in csv.DictReader(f, delimiter='\t') if r['series'] == 'GSE134780']
    aligned = align_metadata(labels, metadata)
    counts = validate_counts(values)
    if counts.shape != (len(genes), 23):
        raise ValueError(f'Expected 23 samples; received {counts.shape}')
    if set(r['tissue'] for r in aligned) != set(TISSUES):
        raise ValueError('Unexpected tissue annotations')
    for tissue in TISSUES:
        for geno, n in EXPECTED_N[tissue].items():
            if sum(r['tissue'] == tissue and r['genotype'] == geno for r in aligned) != n:
                raise ValueError(f'Unexpected group n for {tissue}/{geno}')
    return genes, labels, counts, aligned


def median_ratio(counts):
    """Within-tissue classic positive-in-every-sample geometric mean ratios."""
    eligible = np.all(counts > 0, axis=1)
    if not eligible.any():
        raise ValueError('No genes positive in every included sample')
    c = counts[eligible]
    geom = np.exp(np.mean(np.log(c), axis=1))
    factors = np.median(c / geom[:, None], axis=0)
    if not np.isfinite(factors).all() or not (factors > 0).all():
        raise ValueError('Invalid median-ratio factors')
    return counts / factors, factors, int(eligible.sum())


def cpm_normalize(counts):
    return counts / counts.sum(axis=0) * 1e6


def log_contrast(values, group_labels, numerator, denominator):
    labels = np.asarray(group_labels)
    num = values[labels == numerator]
    den = values[labels == denominator]
    if not len(num) or not len(den):
        raise ValueError('A contrast group is empty')
    return float(np.log2((np.mean(num) + 1.0) / (np.mean(den) + 1.0)))


def direction(x):
    return 'higher' if x > ZERO_TOL else 'lower' if x < -ZERO_TOL else 'zero'


def write_tsv(path, rows):
    if not rows:
        raise ValueError('Refusing empty result table')
    with Path(path).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def run_tests():
    tests = []
    def passed(name):
        tests.append(name)
    def rejects(name, fn):
        try:
            fn()
        except ValueError:
            passed(name)
        else:
            raise AssertionError(f'{name}: did not reject')
    toy = np.array([[10., 20., 40.], [20., 40., 80.], [0., 4., 8.]])
    normalized, factors, n = median_ratio(toy)
    np.testing.assert_allclose(factors, [.5, 1., 2.], rtol=1e-12)
    np.testing.assert_allclose(normalized, [[20.,20.,20.],[40.,40.,40.],[0.,4.,4.]], rtol=1e-12)
    assert n == 2
    passed('hand-calculated median-ratio factors, normalized counts and zero exclusion')
    cm = cpm_normalize(toy)
    np.testing.assert_allclose(cm.sum(axis=0), [1e6]*3, rtol=1e-12)
    assert math.isclose(cm[0,0], 1e6/3, rel_tol=1e-12)
    passed('CPM library sums and hand-calculated individual value')
    assert math.isclose(log_contrast(np.array([2.,4.,4.,6.]), ['a','a','b','b'], 'b','a'), math.log2(1.5), rel_tol=1e-12)
    passed('arithmetic group means and +1 log2 contrast formula')
    records = [{'title':'a','genotype':'WT'}, {'title':'b','genotype':'HH'}]
    assert align_metadata(['b','a'], records)[0]['genotype'] == 'HH'
    passed('sample metadata aligns by exact label rather than row position')
    rejects('reject mismatched labels', lambda: align_metadata(['b','c'], records))
    rejects('reject duplicate labels', lambda: align_metadata(['a','a'], records))
    rejects('reject duplicate genes', lambda: unique_labels(['A','A'], 'genes'))
    rejects('reject fractional counts', lambda: validate_counts([[1.5,2]]))
    rejects('reject negative counts', lambda: validate_counts([[-1,2]]))
    rejects('reject nonfinite counts', lambda: validate_counts([[float('nan'),2]]))
    rejects('reject zero library', lambda: validate_counts([[0,2]]))
    rejects('reject no positive-in-every-sample normalization genes', lambda: median_ratio(np.array([[0.,1.],[1.,0.]])))
    return {'passed':len(tests), 'tests':tests}


def analyze(genes, labels, counts, meta):
    gene_index = {g:i for i,g in enumerate(genes)}
    effects, sample_rows, qc_rows, norm_rows, loo_rows = [], [], [], [], []
    for tissue in TISSUES:
        idx = np.array([i for i,r in enumerate(meta) if r['tissue'] == tissue])
        c = counts[:,idx]
        m = [meta[i] for i in idx]
        groups = np.array([r['genotype'] for r in m])
        normalized, factors, n_positive = median_ratio(c)
        cpm = cpm_normalize(c)
        norm_rows.append({'tissue':tissue, 'samples':len(idx), 'total_gene_rows':len(genes),
            'all_zero_genes':int(np.all(c == 0, axis=1).sum()),
            'positive_in_every_sample_genes':n_positive,
            'size_factor_min':float(factors.min()), 'size_factor_max':float(factors.max())})
        for j,r in enumerate(m):
            qc_rows.append({'sample':r['title'], 'gsm':r['gsm'], 'tissue':tissue,
                'genotype':r['genotype'], 'age':r['age'], 'background_strain':r['background strain'],
                'total_gene_counts':int(c[:,j].sum()), 'nonzero_gene_rows':int((c[:,j]>0).sum()),
                'median_ratio_size_factor':float(factors[j]),
                'sex_available':False, 'exact_age_available':False, 'batch_litter_available':False,
                'cross_tissue_animal_pairing_available':False})
        # Recompute factors for each leave-one-sample-out matrix from all retained genes.
        loo = []
        for omit in range(len(idx)):
            keep = np.arange(len(idx)) != omit
            ln, lf, lg = median_ratio(c[:,keep])
            loo.append((omit, groups[keep], ln, lg))
        for gene in PANEL:
            present = gene in gene_index
            gi = gene_index.get(gene)
            raw = c[gi] if present else None
            low = bool(raw.mean() < 10) if present else None
            for j,r in enumerate(m):
                sample_rows.append({'tissue':tissue,'sample':r['title'],'gsm':r['gsm'],
                    'genotype':r['genotype'],'gene':gene,'gene_present':present,
                    'low_count_tissue_mean_below_10':low,
                    'raw_count':int(raw[j]) if present else None,
                    'median_ratio_normalized_count':float(normalized[gi,j]) if present else None,
                    'cpm':float(cpm[gi,j]) if present else None})
            for numerator, denominator in CONTRASTS:
                nm, dm = groups == numerator, groups == denominator
                effect = log_contrast(normalized[gi], groups,numerator,denominator) if present else None
                cp_effect = log_contrast(cpm[gi], groups,numerator,denominator) if present else None
                omitted_effects = []
                for omit, lgroups, ln, lng in loo:
                    le = log_contrast(ln[gi],lgroups,numerator,denominator) if present else None
                    loo_rows.append({'tissue':tissue,'gene':gene,'numerator':numerator,'denominator':denominator,
                        'omitted_sample':m[omit]['title'], 'omitted_genotype':m[omit]['genotype'],
                        'omitted_sample_in_contrast':m[omit]['genotype'] in (numerator,denominator),
                        'positive_in_every_remaining_sample_genes':lng,
                        'median_ratio_log2_contrast':le, 'direction':direction(le) if present else None,
                        'matches_full_effect_direction':direction(le)==direction(effect) if present else None})
                    if present:
                        omitted_effects.append(le)
                effects.append({'tissue':tissue,'gene':gene,'numerator':numerator,'denominator':denominator,
                    'n_numerator':int(nm.sum()),'n_denominator':int(dm.sum()),'gene_present':present,
                    'low_count_tissue_mean_below_10':low,
                    'tissue_raw_count_mean':float(raw.mean()) if present else None,
                    'tissue_zero_count_samples':int((raw == 0).sum()) if present else None,
                    'numerator_raw_count_mean':float(raw[nm].mean()) if present else None,
                    'denominator_raw_count_mean':float(raw[dm].mean()) if present else None,
                    'numerator_normalized_count_mean':float(normalized[gi,nm].mean()) if present else None,
                    'denominator_normalized_count_mean':float(normalized[gi,dm].mean()) if present else None,
                    'numerator_cpm_mean':float(cpm[gi,nm].mean()) if present else None,
                    'denominator_cpm_mean':float(cpm[gi,dm].mean()) if present else None,
                    'median_ratio_log2_contrast':effect,'cpm_log2_contrast':cp_effect,
                    'median_ratio_direction':direction(effect) if present else None,
                    'cpm_direction':direction(cp_effect) if present else None,
                    'normalization_direction_agrees':direction(effect)==direction(cp_effect) if present else None,
                    'loo_total':len(loo),'loo_min_log2_contrast':min(omitted_effects) if present else None,
                    'loo_max_log2_contrast':max(omitted_effects) if present else None,
                    'loo_matching_directions':sum(direction(x)==direction(effect) for x in omitted_effects) if present else None,
                    'loo_reversed_directions':sum(direction(x)!=direction(effect) and direction(x)!='zero' for x in omitted_effects) if present else None})
    return {'panel_contrasts.tsv':effects, 'panel_sample_expression.tsv':sample_rows,
        'sample_qc.tsv':qc_rows, 'normalization_qc.tsv':norm_rows, 'leave_one_out.tsv':loo_rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--test',action='store_true')
    ap.add_argument('--counts',type=Path)
    ap.add_argument('--metadata',type=Path)
    ap.add_argument('--plan',type=Path)
    ap.add_argument('--receipt',type=Path)
    ap.add_argument('--out',type=Path)
    args = ap.parse_args()
    test_result = run_tests()
    if args.test and not args.counts:
        print(json.dumps(test_result,indent=2)); return
    for k in ('counts','metadata','plan','receipt','out'):
        if getattr(args,k) is None:
            ap.error(f'--{k} is required for analysis')
    receipt = json.loads(args.receipt.read_text())
    if sha(args.counts) != EXPECTED_COUNT_SHA256 or sha(args.counts) != receipt['sha256']:
        raise ValueError('Public count file SHA-256 does not match frozen input')
    if sha(args.plan) != receipt['analysis_plan_sha256_before_download']:
        raise ValueError('Analysis plan differs from pre-download plan')
    genes, labels, counts, meta = load_inputs(args.counts,args.metadata)
    results = analyze(genes, labels, counts, meta)
    if len(results['panel_contrasts.tsv']) != 42 or len(results['leave_one_out.tsv']) != 483:
        raise AssertionError('Missing panel/contrast/leave-one-out rows')
    args.out.mkdir(parents=True,exist_ok=True)
    for file, rows in results.items():
        write_tsv(args.out/file,rows)
    (args.out/'test_results.json').write_text(json.dumps(test_result,indent=2)+'\n')
    manifest = {'dataset':'GSE134780','analysis':'literature-informed exploratory descriptive public mouse audit',
        'no_p_values':True,'panel':list(PANEL),'contrasts':list(CONTRASTS),
        'tissues_normalized_separately':True,'normalization':'unrescaled median ratios; geometric means of genes positive in all included tissue samples',
        'log2_formula':'log2((arithmetic numerator group mean + 1)/(arithmetic denominator group mean + 1))',
        'secondary_normalization':'CPM using all-feature library totals, +1 CPM pseudocount',
        'zero_direction_tolerance':ZERO_TOL,'low_count_flag':'tissue mean raw count < 10; not excluded',
        'loo_scope':'each sample of a tissue omitted in turn; size factors recomputed on all remaining genes/samples',
        'input_download_receipt':receipt,'inputs':{p.name:sha(p) for p in [args.counts,args.metadata,args.plan,args.receipt]},
        'script_sha256':sha(Path(__file__)),
        'python_version':platform.python_version(),'numpy_version':np.__version__,
        'integrity':{'gene_rows':len(genes),'samples':len(labels),'unique_gene_ids':True,'unique_sample_labels':True,
            'integer_nonnegative_finite_counts':True,'exact_metadata_label_match':True,'expected_group_n_match':True},
        'row_counts':{name:len(rows) for name,rows in results.items()},
        'output_sha256':{name:sha(args.out/name) for name in [*results,'test_results.json']}}
    (args.out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'integrity':manifest['integrity'],'row_counts':manifest['row_counts'],
        'tests_passed':test_result['passed'],'output_dir':str(args.out)},indent=2))

if __name__ == '__main__':
    main()
