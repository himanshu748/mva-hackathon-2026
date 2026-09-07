"""Validate annotation coverage and provenance without disclosing variant rows."""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path

BATCH = 200
ENDPOINT = 'https://rest.ensembl.org/vep/human/region'
OPTIONS = dict(canonical=1, hgvs=1, symbol=1, mane=1, numbers=1, af=1,
               af_gnomade=1, af_gnomadg=1, sift=1, polyphen=1)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inputs_from_tsv(path):
    variants = []
    for line in Path(path).read_text().splitlines():
        f = line.split('\t')
        if len(f) < 7:
            raise ValueError('Invalid coding TSV row')
        variants.append(f'{f[0]} {f[1]} . {f[2]} {f[3]} . . .')
    if not variants or len(variants) != len(set(variants)):
        raise ValueError('Coding inputs are empty or duplicated')
    return variants

def validate_batch(rows, expected):
    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
        raise ValueError('Annotation response must be a list of records')
    actual = [r.get('input') for r in rows]
    if collections.Counter(actual) != collections.Counter(expected):
        raise ValueError('Annotation coverage mismatch: missing, duplicate or unexpected inputs')
    if any(r.get('assembly_name') not in (None, 'GRCh38') for r in rows):
        raise ValueError('Annotation assembly is not GRCh38')

def request_identity(root):
    root = Path(root)
    return {'input_sha256': digest(root/'out/coding_pass.tsv'),
            'endpoint': ENDPOINT, 'options': OPTIONS, 'batch_size': BATCH}

def validate_cache(root, require_manifest=True):
    root = Path(root); variants = inputs_from_tsv(root/'out/coding_pass.tsv')
    parts = root/'out/vep_parts'
    expected_files = {f'b{i//BATCH:04d}.json' for i in range(0,len(variants),BATCH)}
    if {p.name for p in parts.glob('*.json')} != expected_files:
        raise ValueError('Annotation batch set is incomplete or contains stale batches')
    hashes = {}
    for i in range(0,len(variants),BATCH):
        p = parts/f'b{i//BATCH:04d}.json'
        validate_batch(json.loads(p.read_text()), variants[i:i+BATCH]); hashes[p.name] = digest(p)
    manifest_path = root/'out/annotation_manifest.json'
    if require_manifest:
        m = json.loads(manifest_path.read_text())
        if m['request'] != request_identity(root) or m['batch_sha256'] != hashes:
            raise ValueError('Annotation provenance mismatch; do not reuse this cache')
    return variants, hashes

def write_manifest(root, provenance):
    root = Path(root); variants, hashes = validate_cache(root, require_manifest=False)
    refs = {n:digest(root/'ref'/n) for n in ['hp.obo','genes_to_phenotype.txt','gencode.gtf.gz','cds.bed'] if (root/'ref'/n).exists()}
    m = {'schema':1,'request':request_identity(root),'records':len(variants),
         'batch_sha256':hashes,'reference_snapshot_sha256':refs,'provenance':provenance}
    dest = root/'out/annotation_manifest.json'; tmp=dest.with_suffix('.tmp')
    tmp.write_text(json.dumps(m,indent=2)+'\n');tmp.replace(dest)
    return m
