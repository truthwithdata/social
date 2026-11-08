#!/usr/bin/env python3
"""Turn carousel slides into a 9:16 Instagram Reel (1080x1920 MP4, H.264 + silent AAC, 30 fps).

    python3 scripts/make_reel.py OUT.mp4 SLIDE1.png SLIDE2.png ... [--seconds 2.8] [--first 2.2] [--outro VIDEO.mp4]
    python3 scripts/make_reel.py --story OUT.jpg SLIDE.png      # one 1080x1920 Instagram story image

Each slide sits on a white 1080x1920 canvas under the brand bar, with a slow zoom and a
0.4 s crossfade between slides. --outro appends a 1080x1920 clip (e.g. the logo outro from
make_logo_outro.py) with the same crossfade. Paths are relative to the repo root. Also writes
OUT-cover.jpg (first slide) for use as the Reel cover. Instagram adds no music via the API;
add trending audio in the app only if you post the Reel by hand.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS, FADE = 1080, 1920, 30, 0.4


def canvas(slide_path, out_path):
    bg = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(bg)
    for x in range(W):  # brand gradient bar, #2563eb -> #60a5fa
        t = x / (W - 1)
        c = (int(0x25 + t * (0x60 - 0x25)), int(0x63 + t * (0xa5 - 0x63)), int(0xeb + t * (0xfa - 0xeb)))
        d.line([(x, 0), (x, 18)], fill=c)
    s = Image.open(os.path.join(ROOT, slide_path)).convert("RGB").resize((W, 1350), Image.LANCZOS)
    sd = ImageDraw.Draw(s)
    sd.rectangle([0, 0, W, 16], fill="white")        # the slide's own brand bar (the canvas has one)
    sd.rectangle([820, 60, W, 150], fill="white")     # the "n/8" counter, meaningless in a video
    bg.paste(s, (0, (H - 1350) // 2 - 60))
    bg.save(out_path, quality=95)


def main(argv):
    if argv and argv[0] == "--story":
        out = os.path.join(ROOT, argv[1])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        canvas(argv[2], out)
        print(os.path.relpath(out, ROOT))
        return
    secs, first, args, outro = 2.8, 2.2, [], None
    i = 0
    while i < len(argv):
        if argv[i] == "--seconds":
            secs = float(argv[i + 1]); i += 2
        elif argv[i] == "--outro":
            outro = os.path.join(ROOT, argv[i + 1]); i += 2
        elif argv[i] == "--first":
            first = float(argv[i + 1]); i += 2
        else:
            args.append(argv[i]); i += 1
    out, slides = os.path.join(ROOT, args[0]), args[1:]
    if len(slides) < 2:
        sys.exit("need at least 2 slides")
    durs = [first] + [secs] * (len(slides) - 1)
    durs[-1] += 1.0  # hold the final call to action
    with tempfile.TemporaryDirectory() as tmp:
        clips = []
        for k, (sp, dur) in enumerate(zip(slides, durs)):
            frame = os.path.join(tmp, f"f{k}.jpg")
            canvas(sp, frame)
            clip = os.path.join(tmp, f"c{k}.mp4")
            n = int((dur + FADE) * FPS)
            zoom = f"zoompan=z='1+0.04*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", frame, "-vf",
                            f"scale={W * 2}:{H * 2},{zoom},format=yuv420p", "-frames:v", str(n),
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", clip], check=True)
            clips.append(clip)
        if outro:   # treat the outro as one more clip; its own length minus the crossfade is its "duration"
            od = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outro],
                                      capture_output=True, text=True, check=True).stdout)
            durs[-1] -= 1.0          # the outro is the final hold
            clips.append(outro)
            durs.append(od - FADE)
        inputs, chain, offset, last = [], [], 0.0, "0:v"
        for k, c in enumerate(clips):
            inputs += ["-i", c]
        for k in range(1, len(clips)):
            offset += durs[k - 1]
            lab = f"v{k}"
            chain.append(f"[{last}][{k}:v]xfade=transition=fade:duration={FADE}:offset={offset:.3f}[{lab}]")
            last = lab
        total = sum(durs) + FADE
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs,
                        "-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                        "-filter_complex", ";".join(chain + [f"[{last}]settb=AVTB,fps={FPS}[vout]"]), "-map", "[vout]", "-map", f"{len(clips)}:a",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], check=True)
        canvas(slides[0], out[:-4] + "-cover.jpg")
    print(os.path.relpath(out, ROOT), f"{total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1:])
