"""Render the Track 2 pitch video: slides + narration -> MP4.

Rerunnable; remote speech output can vary between requests. Slide stills are captured from
report/pitch_slides.html with headless Chromium at 1920x1080, narration is
synthesised per slide, and each slide is held on screen for exactly the length
of its own narration plus a short tail.

Narration engine is swappable via --engine:
  none      silent reading-time slides (default; no API key)
  say       macOS built-in (free, offline, no API key)
  deepgram  Deepgram Aura (higher quality; needs DEEPGRAM_API_KEY)

Usage:
    python3 scripts/10_render_pitch.py                 # silent pitch
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
    "Our proposal concerns a child with mosaic variegated aneuploidy and a family who shared their data for research. We identified two candidate variants in bub one bee. We propose testing whether selective removal of senescent cells can improve tissue function without adding harm.",
    "The original analysis checked known disease genes first. A later genome wide ranking placed both candidates in the top three. Track one received one hundred rank points. The stop variant predicts loss of function. The missense variant needs functional testing, and their phase remains unknown.",
    "Both candidates stayed in the top three across one hundred and sixty two scoring and gene exclusion settings. This supports stability within this case. It is not independent validation. Our next question is whether the proposed drug combination deserves further investigation.",
    "Bub are one helps the spindle assembly checkpoint restrain chromosome separation. Its dysfunction can cause errors in chromosome separation. Our therapeutic hypothesis concerns a possible downstream consequence: persistent senescent cells and their inflammatory signals. Whether this patient has a harmful senescent cell burden still needs measurement.",
    "The strongest supporting experiment is a mouse study. Genetic removal of senescent cells delayed selected aging related problems in bub are one deficient mice. That establishes a mechanism worth testing. It does not establish that drugs reproduce the result, or that the result transfers to this child.",
    "We propose testing dasatinib and quercetin to remove senescent cells. Adult studies provide early evidence, but a randomized bone study missed its primary endpoint. Dasatinib has specific pediatric leukemia approvals. Neither those approvals nor the adult studies establish safety or efficacy in this disease.",
    "A twenty twenty six study found myelin damage in mice without obvious cell death. That changes our test plan. We would compare each drug and the combination, measuring tissue function and neural differentiation as well as selective killing. We must also check whether surviving cells become more unstable.",
    "We would stop if target burden is absent, healthy tissue function worsens, or chromosome instability increases. The combination must offer an advantage over its components. This is a preclinical proposal with open methods and explicit failure criteria. Thank you to the child, family, and organizers.",
    ""
]

TAIL = 0.6          # seconds of silence held after each slide's narration
TARGET_SECONDS = 176   # aim for 2:56. Higher than it needs to be on purpose: forcing
                       # a large atempo speed-up measurably degrades intelligibility of
                       # the long clinical terms, so take the runtime over the clarity.
# Deepgram voice: thalia. Chosen by measurement, not taste. vesta (119 wpm) is the most
# natural-sounding of the set but runs the script to 3:39, which needs a >1.15 atempo to
# fit the 3:00 limit and reintroduces exactly the artifacts we were trying to remove.
# The previous pitch used Thalia without tempo correction; measure each new render.
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
    model = os.environ.get("DEEPGRAM_VOICE", "aura-2-thalia-en")
    req = urllib.request.Request(
        f"https://api.deepgram.com/v1/speak?model={model}&mip_opt_out=true",
        data=json.dumps({"text": text}).encode(),
        headers={"Authorization": f"Token {key}", "Content-Type": "application/json"},
    )
    raw = dest.with_suffix(".raw.mp3")
    with urllib.request.urlopen(req, timeout=120) as r:
        raw.write_bytes(r.read())
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
        "-ar", "48000", "-ac", "2", str(dest)])
    raw.unlink()


def render_silent() -> None:
    """Encode fixed frame counts per slide, then concatenate without an audio track."""
    durations = [12, 18, 15, 16, 18, 20, 22, 16, 24]
    for n, seconds in enumerate(durations, 1):
        sh(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30",
            "-i", str(BUILD / f"slide{n:02d}.png"), "-frames:v", str(seconds * 30),
            "-vf", "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0d1117,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-tune", "stillimage", "-crf", "20",
            "-an", str(BUILD / f"silent{n:02d}.mp4")])
    (BUILD / "silent.txt").write_text("".join(f"file 'silent{n:02d}.mp4'\n" for n in range(1, 10)))
    out = ROOT / "report" / "HIMANSHUKUMARJHA_track2_pitch.mp4"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i",
        "silent.txt", "-c", "copy", "-movflags", "+faststart", str(out)], cwd=BUILD)
    final = duration(out)
    if abs(final - sum(durations)) > 0.1 or final > 180:
        sys.exit(f"FAIL: silent pitch duration {final}")
    (BUILD / "render_metadata.json").write_text(json.dumps({"engine": "none", "external_speech_request": False,
        "durations": durations, "spoken_words": 0, "audio_track": False}, indent=2))
    print(f"Silent pitch verified: {final:.3f}s; no audio track.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["none", "say", "deepgram"], default="none")
    ap.add_argument("--skip-capture", action="store_true", help="Use previously captured slide PNGs")
    ap.add_argument("--reuse-audio", action="store_true", help="Reuse audio only when saved text matches")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found (conda install ffmpeg, or brew install ffmpeg)")

    BUILD.mkdir(parents=True, exist_ok=True)
    shutil.copy(SLIDES_HTML, BUILD / "pitch_slides.html")

    if not args.skip_capture:
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

    else:
        for n in range(1, len(NARRATION) + 1):
            if not (BUILD / f"slide{n:02d}.png").is_file():
                sys.exit(f"Missing slide {n}")

    if args.engine == "none":
        render_silent()
        return

    print(f"Synthesising narration with engine={args.engine}")
    synth = tts_say if args.engine == "say" else tts_deepgram
    durations = []
    for n, text in enumerate(NARRATION, 1):
        wav = BUILD / f"vo{n:02d}.wav"
        if not text:
            sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "12", str(wav)])
            durations.append(12.0)
            continue
        text_path = wav.with_suffix(".text")
        if not (args.reuse_audio and wav.exists() and text_path.exists() and text_path.read_text() == text):
            synth(text, wav)
            text_path.write_text(text)
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
        "-vf", "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0d1117,tpad=stop_mode=clone:stop_duration=5",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", str(out)], cwd=BUILD)

    (BUILD / "render_metadata.json").write_text(json.dumps({"engine": args.engine, "mip_opt_out": args.engine == "deepgram", "durations": durations, "spoken_words": 0 if args.engine == "none" else sum(len(t.split()) for t in NARRATION)}, indent=2))
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
