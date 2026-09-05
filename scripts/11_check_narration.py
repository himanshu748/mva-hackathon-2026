"""Round-trip QA for the pitch narration.

Text to speech mangles domain vocabulary silently: Deepgram rendered "BUB1B" as
"bub one byte" and dropped "senolytics" altogether. Rather than trust the audio,
transcribe it back with Deepgram speech to text and assert that the terms a judge
must hear actually survived.
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

AUDIO = ROOT / "out" / "pitch" / "narration.wav"
# Phrases a judge has to come away with, as they should sound in the transcript.
MUST_HEAR = [
    ("bub1b", "bub one b"), # the gene; STT writes the spoken form either way
    "compound heterozygous",
    "nonsense allele",
    "hypomorph",
    "spindle assembly checkpoint",
    "senescent",
    "quercetin" ,
    "growth failure",
    "hypothesis is dead",
    "fourteenth",
    "tinib",                # dasatinib must at least land as a -tinib drug
    "lytic",                # senolytic must survive
]
# Mispronunciations seen in earlier renders. Any of these means a regression.
MUST_NOT_HEAR = ["one byte", "anaplasm", "feta type", "break slabs", "dasenib",
                 "sat ninety", "day is that", "mildomyo", "fnax", "acetolytic"]

# The raw WAV is ~32 MB and reliably breaks the upload, so send a compressed copy.
mp3 = AUDIO.with_suffix(".mp3")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(AUDIO),
                "-b:a", "96k", str(mp3)], check=True)
res = subprocess.run([
    "curl", "-sS", "-X", "POST",
    "https://api.deepgram.com/v1/listen?model=nova-3&punctuate=true&smart_format=true",
    "-H", f"Authorization: Token {os.environ['DEEPGRAM_API_KEY']}",
    "-H", "Content-Type: audio/mpeg",
    "--data-binary", f"@{mp3}"], capture_output=True, text=True, check=True)
d = json.loads(res.stdout)
alt = d["results"]["channels"][0]["alternatives"][0]
text = alt["transcript"].lower()

print(f"transcription confidence: {alt['confidence']:.3f}\n")
ok = True
for phrase in MUST_HEAR:
    opts = phrase if isinstance(phrase, tuple) else (phrase,)
    hit = any(o.lower() in text for o in opts)
    phrase = " / ".join(opts)
    ok &= hit
    print(f"  {'OK  ' if hit else 'MISS'}  heard: {phrase}")
print()
for phrase in MUST_NOT_HEAR:
    bad = phrase.lower() in text
    ok &= not bad
    print(f"  {'BAD ' if bad else 'OK  '}  absent: {phrase}")

Path("out/pitch/transcript.txt").write_text(alt["transcript"])
print("\ntranscript written to out/pitch/transcript.txt")
sys.exit(0 if ok else "FAIL: narration does not say what it must")
