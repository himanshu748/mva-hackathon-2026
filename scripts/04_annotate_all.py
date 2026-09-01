"""Annotate the coding variant set via Ensembl VEP REST, in parallel.

Writes one JSON file per batch so the run is resumable: rerunning skips
any batch whose part file already exists.
"""
import json, os, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC, PARTS, BATCH, WORKERS = "out/coding_pass.tsv", "out/vep_parts", 200, 6

variants = []
for line in open(SRC):
    f = line.rstrip("\n").split("\t")
    variants.append(f"{f[0]} {f[1]} . {f[2]} {f[3]} . . .")
batches = [(i // BATCH, variants[i:i+BATCH]) for i in range(0, len(variants), BATCH)]
todo = [b for b in batches if not os.path.exists(f"{PARTS}/b{b[0]:04d}.json")]
print(f"{len(variants):,} variants in {len(batches)} batches; {len(todo)} still to do", flush=True)

def run(job):
    idx, chunk = job
    body = json.dumps({"variants": chunk, "canonical": 1, "hgvs": 1, "symbol": 1,
                       "mane": 1, "numbers": 1, "af": 1, "af_gnomade": 1,
                       "af_gnomadg": 1, "sift": 1, "polyphen": 1}).encode()
    req = urllib.request.Request("https://rest.ensembl.org/vep/human/region", data=body,
          headers={"Content-Type": "application/json", "Accept": "application/json"})
    for attempt in range(6):
        try:
            res = json.load(urllib.request.urlopen(req, timeout=300))
            tmp = f"{PARTS}/b{idx:04d}.json.tmp"
            with open(tmp, "w") as fh: json.dump(res, fh)
            os.replace(tmp, f"{PARTS}/b{idx:04d}.json")   # atomic, so partial files never look done
            return idx, len(res), None
        except Exception as e:
            if attempt == 5: return idx, 0, str(e)
            time.sleep(2 ** attempt)

t0, n = time.time(), 0
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = [ex.submit(run, j) for j in todo]
    for f in as_completed(futs):
        idx, cnt, err = f.result(); n += 1
        if err: print(f"  batch {idx} FAILED: {err}", flush=True)
        if n % 10 == 0 or n == len(todo):
            el = time.time() - t0
            print(f"  {n}/{len(todo)} batches  {el:.0f}s elapsed  eta {el/n*(len(todo)-n):.0f}s", flush=True)
print("done", flush=True)
