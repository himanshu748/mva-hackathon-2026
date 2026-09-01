"""Fetch only the small files from the gated hackathon dataset.

Skips the 8 FASTQ files (~84 GB). VCF + index + phenotype doc is ~318 MB
and is sufficient for Track 1 and for mechanism work in Track 2.

Requires the HF_TOKEN environment variable (a Hugging Face access token for
an account that has been granted access to SageBio/mva-hackathon-2026-data).
"""
import os
import sys
from huggingface_hub import hf_hub_download

REPO = "SageBio/mva-hackathon-2026-data"
SMALL_FILES = [
    "WGS_EX2312012_HGWCNDSX7.vcf.gz",
    "WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi",
    "Challenge_Clinical_Phenotype_1.docx",
]

token = os.environ.get("HF_TOKEN")
if not token:
    sys.exit("HF_TOKEN is not set. Put your Hugging Face token in it, e.g. "
             "export HF_TOKEN=hf_xxx  (token from https://huggingface.co/settings/tokens)")

dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
for name in SMALL_FILES:
    path = hf_hub_download(repo_id=REPO, filename=name, repo_type="dataset",
                           local_dir=dest, token=token)
    print(f"{name}: {os.path.getsize(path) / 1e6:.1f} MB -> {path}")
