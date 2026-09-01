"""Annotate a TSV of variants via the Ensembl VEP REST API (no local cache, no disk cost)."""
import json, sys, time, urllib.request

SERVER = "https://rest.ensembl.org/vep/human/region"

def vep(variants, batch=200):
    out = []
    for i in range(0, len(variants), batch):
        chunk = variants[i:i+batch]
        body = json.dumps({
            "variants": chunk,
            "canonical": 1, "hgvs": 1, "symbol": 1, "numbers": 1,
            "af": 1, "af_gnomade": 1, "af_gnomadg": 1, "sift": 1, "polyphen": 1,
        }).encode()
        req = urllib.request.Request(SERVER, data=body, headers={
            "Content-Type": "application/json", "Accept": "application/json"})
        for attempt in range(5):
            try:
                out.extend(json.load(urllib.request.urlopen(req, timeout=120)))
                break
            except Exception as e:
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)
        time.sleep(0.2)
    return out

if __name__ == "__main__":
    variants = []
    for line in open(sys.argv[1]):
        f = line.split("\t")
        variants.append(f"{f[0]} {f[1]} . {f[2]} {f[3]} . . .")
    json.dump(vep(variants), open(sys.argv[2], "w"), indent=1)
    print(f"annotated {len(variants)} variants -> {sys.argv[2]}")
