"""Resumable VEP annotation with exact coverage checks and cache provenance.

An existing unmanifested cache needs explicit --adopt-existing-cache. Adoption
validates inputs and records present-day hashes; it cannot recover a historical
VEP release or prove the historical request options.
"""
from __future__ import annotations
import argparse
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from annotation_cache import BATCH, ENDPOINT, OPTIONS, inputs_from_tsv, request_identity, validate_batch, validate_cache, write_manifest

ROOT = Path(__file__).resolve().parent.parent

def fetch_batch(chunk, attempts=6):
    req = urllib.request.Request(ENDPOINT, data=json.dumps({'variants':chunk,**OPTIONS}).encode(),
          headers={'Content-Type':'application/json','Accept':'application/json'})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req,timeout=300) as response:
                rows=json.load(response)
            validate_batch(rows,chunk)
            return rows
        except Exception:
            if attempt==attempts-1: raise
            time.sleep(2**attempt)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--adopt-existing-cache',action='store_true')
    args=ap.parse_args(); parts=ROOT/'out/vep_parts';parts.mkdir(parents=True,exist_ok=True)
    manifest=ROOT/'out/annotation_manifest.json'; identity=ROOT/'out/annotation_request.json'
    now=datetime.now(timezone.utc).isoformat()
    if args.adopt_existing_cache:
        if manifest.exists():
            validate_cache(ROOT);print('Existing manifest and complete cache verified');return
        m=write_manifest(ROOT,{'origin':'legacy_cache_adoption','verified_at':now,
            'service_release':'not recorded at original annotation time',
            'request_options':'inferred from historical script; not server-attested'})
        identity.write_text(json.dumps(request_identity(ROOT),indent=2)+'\n')
        print(f"Adopted and verified {m['records']} cached records; no network calls");return
    if manifest.exists():
        validate_cache(ROOT);print('Complete annotation cache verified');return
    expected=request_identity(ROOT)
    if identity.exists():
        if json.loads(identity.read_text())!=expected:raise ValueError('Input/options changed; use a separate output directory')
    elif list(parts.glob('*.json')):
        raise ValueError('Unmanifested legacy cache: validate with --adopt-existing-cache first')
    else:identity.write_text(json.dumps(expected,indent=2)+'\n')
    variants=inputs_from_tsv(ROOT/'out/coding_pass.tsv');jobs=[]
    for i in range(0,len(variants),BATCH):
        p=parts/f'b{i//BATCH:04d}.json';chunk=variants[i:i+BATCH]
        if p.exists():validate_batch(json.loads(p.read_text()),chunk)
        else:jobs.append((p,chunk))
    failures=[]
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures={ex.submit(fetch_batch,chunk):p for p,chunk in jobs}
        for future in as_completed(futures):
            p=futures[future]
            try:
                rows=future.result();tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(rows));tmp.replace(p)
            except Exception as e:
                failures.append(p.name);print(f'{p.name} FAILED ({type(e).__name__})',flush=True)
    if failures:raise RuntimeError(f'{len(failures)} annotation batches failed; ranking is blocked')
    write_manifest(ROOT,{'origin':'VEP_REST','completed_at':now,
        'service_release':'live endpoint; release not pinned; retain response hashes'})
    print(f'Complete: {len(variants)} unique coding inputs validated')

if __name__=='__main__':main()
