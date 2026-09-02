"""Render the Track 2 pitch video: slides + narration -> MP4.

Fully deterministic and rerunnable. Slide stills are captured from
report/pitch_slides.html with headless Chromium at 1920x1080, narration is
synthesised per slide, and each slide is held on screen for exactly the length
of its own narration plus a short tail.

Narration engine is swappable via --engine:
  say       macOS built-in (default; free, offline, no API key)
  deepgram  Deepgram Aura (higher quality; needs DEEPGRAM_API_KEY)

Usage:
    python3 scripts/10_render_pitch.py                 # local voice
    DEEPGRAM_API_KEY=... python3 scripts/10_render_pitch.py --engine deepgram
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

# Load .env (gitignored) so DEEPGRAM_API_KEY need not be exported manually.
_envf = ROOT / ".env"
if _envf.exists():
    for _line in _envf.read_text().splitlines():
        if "=" in _line and not _line.strip().startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
BUILD = ROOT / "out" / "pitch"
SLIDES_HTML = ROOT / "report" / "pitch_slides.html"
PORT = 8749

# One entry per slide, in order. Text is what gets spoken; it must stay in sync
# with report/track2_pitch_script.md.
NARRATION = [
    "A child with rhabdomyosarcoma, growth failure, and a family history of recurrent "
    "miscarriage. Fewer than fifty people worldwide share his condition. His family opened "
    "his genome to strangers, hoping someone could help. "
    "This is what we found, and what we think can be done about it.",

    "Our pipeline is blind. No gene panel, no disease hypothesis. Five million variants, "
    "filtered to one hundred and ninety four, ranked on four independent axes. "
    "Top of that list: compound heterozygous B U B 1 B. A nonsense allele that triggers decay, "
    "so a true null. In trans with a final exon missense that escapes it, so a hypomorph. "
    "One hundred out of one hundred. F max, one point zero.",

    "Here is the part that convinced us it was real. Scored on the eight clinical terms alone, "
    "with no genetic data whatsoever, B U B 1 B ranks fourteenth out of five thousand two "
    "hundred and sixty eight genes. The phenotype pointed at the gene before we looked at a "
    "single variant.",

    "B U B R 1 runs the spindle assembly checkpoint. It holds the cell at anaphase until every "
    "chromosome is properly attached. Halve the dose and the brake slips, anaphase starts "
    "early, and chromosomes missegregate. That is the variegated aneuploidy. "
    "But the therapeutic question is what happens to those aneuploid cells. They accumulate "
    "damage and turn senescent, pumping inflammatory signals into the tissue. You cannot drug "
    "a missing allele. You can drug that.",

    "And this is not speculation. The Bub R 1 hypomorphic mouse carries a lesion in the same "
    "gene. Clear its senescent cells, and the disease slows. That is causal, and it is "
    "published in Nature. "
    "The mouse's signature phenotype is muscle wasting. So is this child's.",

    "So we propose senolytics: dasatinib plus quercetin. Dasatinib is already approved for "
    "children, with established dosing. The combination has first in human data showing "
    "senescent cells actually fall. And it is dosed three days a week, not every day.",

    "Now the problem, and we would rather say it than have you find it. Dasatinib affects growth "
    "in children, and this child's presenting problem is growth failure. We think intermittent "
    "dosing resolves that. We have not shown it. "
    "So that is the experiment. And if patient cells show no senescent burden, our hypothesis "
    "is dead. We have said exactly how to kill it.",

    "This is not really about one child. Chromosomal instability disorders converge on the same "
    "node. The pipeline runs on a laptop in thirty minutes, for zero cost. Everything is open.",
]

TAIL = 0.6
TARGET_SECONDS = 168   # aim for 2:48, leaving margin under the hard 3:00 limit          # seconds of silence held after each slide's narration
SAY_VOICE = "Samantha"
SAY_WPM = 145       # default `say` rate is ~186 wpm, too fast to follow


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def chromium() -> str:
    base = Path.home() / "Library/Caches/ms-playwright"
    for d in sorted(base.glob("chromium_headless_shell-*"), reverse=True):
        exe = d / "chrome-headless-shell-mac-arm64" / "chrome-headless-shell"
        if exe.exists():
            return str(exe)
    for name in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 shutil.which("chromium") or "", shutil.which("google-chrome") or ""):
        if name and Path(name).exists():
            return name
    sys.exit("No Chromium found. Install Chrome, or run: npx playwright install chromium")


def duration(path: Path) -> float:
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
              "-of", "csv=p=0", str(path)]).stdout.strip()
    return float(out)


def tts_say(text: str, dest: Path) -> None:
    aiff = dest.with_suffix(".aiff")
    sh(["say", "-v", SAY_VOICE, "-r", str(SAY_WPM), "-o", str(aiff), text])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff),
        "-ar", "48000", "-ac", "2", str(dest)])
    aiff.unlink()


def tts_deepgram(text: str, dest: Path) -> None:
    key = os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        sys.exit("DEEPGRAM_API_KEY is not set. Export it, or drop --engine deepgram "
                 "to use the local voice.")
    model = os.environ.get("DEEPGRAM_VOICE", "aura-2-harmonia-en")
    req = urllib.request.Request(
        f"https://api.deepgram.com/v1/speak?model={model}",
        data=json.dumps({"text": text}).encode(),
        headers={"Authorization": f"Token {key}", "Content-Type": "application/json"},
    )
    raw = dest.with_suffix(".raw.mp3")
    with urllib.request.urlopen(req, timeout=120) as r:
        raw.write_bytes(r.read())
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
        "-ar", "48000", "-ac", "2", str(dest)])
    raw.unlink()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["say", "deepgram"], default="say")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found (conda install ffmpeg, or brew install ffmpeg)")

    BUILD.mkdir(parents=True, exist_ok=True)
    shutil.copy(SLIDES_HTML, BUILD / "pitch_slides.html")

    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)],
                              cwd=BUILD, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        subprocess.run([sys.executable, "-c",
                        "import time,urllib.request;"
                        f"[time.sleep(.3) or urllib.request.urlopen('http://localhost:{PORT}/') "
                        "for _ in range(1)]"], check=False)

        cb = chromium()
        print(f"Capturing {len(NARRATION)} slides at 1920x1080")
        for n in range(1, len(NARRATION) + 1):
            png = BUILD / f"slide{n:02d}.png"
            subprocess.run([cb, "--headless", "--disable-gpu", "--hide-scrollbars",
                            f"--screenshot={png}", "--window-size=1920,1080",
                            f"http://localhost:{PORT}/pitch_slides.html?s={n}"],
                           check=True, capture_output=True)
            print(f"  slide {n}")
    finally:
        server.terminate()

    print(f"Synthesising narration with engine={args.engine}")
    synth = tts_say if args.engine == "say" else tts_deepgram
    durations = []
    for n, text in enumerate(NARRATION, 1):
        wav = BUILD / f"vo{n:02d}.wav"
        synth(text, wav)
        d = duration(wav) + TAIL
        durations.append(d)
        words = len(text.split())
        print(f"  slide {n}: {d:5.1f}s  ({words} words, {words/d*60:.0f} wpm)")

    total = sum(durations)
    print(f"\nnarration total: {int(total//60)}:{total%60:04.1f}")

    # Deepgram pacing is not deterministic between runs, so the same script can come
    # back several seconds longer or shorter. Rather than trust it, nudge the tempo
    # to guarantee we land under the hard 3:00 limit with margin.
    if total > TARGET_SECONDS:
        tempo = min(total / TARGET_SECONDS, 1.15)
        print(f"  over target, applying atempo={tempo:.4f}")
        durations = []
        for n in range(1, len(NARRATION) + 1):
            src, dst = BUILD / f"vo{n:02d}.wav", BUILD / f"sp{n:02d}.wav"
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                "-filter:a", f"atempo={tempo:.4f}", str(dst)])
            dst.replace(src)
            durations.append(duration(src) + TAIL)
        total = sum(durations)
        print(f"  adjusted total: {int(total//60)}:{total%60:04.1f}")

    # Pad each narration segment with its trailing silence so audio and video agree exactly.
    for n, d in enumerate(durations, 1):
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(BUILD / f"vo{n:02d}.wav"),
            "-af", f"apad=whole_dur={d}", str(BUILD / f"pad{n:02d}.wav")])

    (BUILD / "audio.txt").write_text(
        "".join(f"file 'pad{n:02d}.wav'\n" for n in range(1, len(durations) + 1)))
    (BUILD / "video.txt").write_text(
        "".join(f"file 'slide{n:02d}.png'\nduration {d}\n"
                for n, d in enumerate(durations, 1))
        + f"file 'slide{len(durations):02d}.png'\n")   # concat demuxer needs the last frame twice

    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", "audio.txt", "-c", "copy", "narration.wav"], cwd=BUILD)
    audio_len = duration(BUILD / "narration.wav")

    out = ROOT / "report" / "HIMANSHUKUMARJHA_track2_pitch.mp4"
    # -t pins the output to the narration length. Without it the concat demuxer's
    # duplicated final image leaves a long silent tail on the video stream.
    sh(["ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", "video.txt",
        "-i", "narration.wav",
        "-t", f"{audio_len:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", str(out)], cwd=BUILD)

    final = duration(out)
    v = sh(["ffprobe", "-v", "error", "-select_streams", "v",
            "-show_entries", "stream=duration", "-of", "csv=p=0", str(out)]).stdout.strip()
    print(f"  video stream {float(v):.1f}s / audio {audio_len:.1f}s / container {final:.1f}s")
    if final > 180:
        sys.exit(f"FAIL: {final:.1f}s exceeds the 3:00 limit")
    print(f"  OK: {int(final//60)}:{final%60:04.1f} is under the 3:00 limit")

    print(f"\nwrote {out.relative_to(ROOT)}  ({out.stat().st_size/1e6:.1f} MB, "
          f"{duration(out):.1f}s)")


if __name__ == "__main__":
    main()
