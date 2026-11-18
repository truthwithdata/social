#!/usr/bin/env python3
"""Build a 9:16 Reel (1080x1920, 30 fps) from Gemini (Veo) clips, text cards and a voiceover.

    python3 scripts/make_veo_reel.py SPEC.json

SPEC.json:
{
  "out": "img/<week>/reel/<name>-reel.mp4",          # repo-relative; also writes <name>-reel-cover.jpg
  "clips": [{"src": "path.mp4", "start": 0, "end": 10}, ...],   # source paths absolute or repo-relative
  "xfade": 0.3,                                         # crossfade between clips (s)
  "outro": "img/brand/logo-outro-1080x1920.mp4",        # optional, crossfaded on at the end
  "delogo": [570, 1128, 60, 64],                       # optional x,y,w,h box (source pixels) to paint out the Gemini sparkle
  "ambient": 0.25,                                      # volume of the clips' own sound under the voice
  "cards": [{"t0": 0.5, "t1": 4.4, "lines": [{"text": "...", "style": "main|accent|small"}]}],
  "voice": [{"wav": "path.wav", "at": 0.5}],
  "cover": {"src": "clip.mp4", "t": 3.0,                # optional designed cover: background frame from a clip,
            "lines": [{"text": "Is renting really"}, {"text": "'dead money'?", "style": "accent"}],
            "sub": "We ran the numbers for every UK region"}
}
With "cover", the script writes <name>-reel-cover.jpg (Instagram cover; the headline sits in the middle 3:4 area
that the profile grid shows) and <name>-reel-tiktok.mp4: the same reel opening on the cover for half a second, so
TikTok's default thumbnail (the first frame) is the cover. TikTok's API can't take a separate cover image.
    python3 scripts/make_veo_reel.py --tiktok-only COVER.jpg REEL.mp4   # TikTok variant for an existing reel
Cards are white with the brand blue bar on the left, near the top of the frame, and fade in and out.
Text never goes into the Veo prompts; every number in a Reel comes from these cards.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
BLUE, INK, ORANGE, MUTED = (37, 99, 235), (15, 23, 42), (234, 88, 12), (71, 85, 105)
STYLES = {"main": ("SemiBold", 50, INK), "accent": ("Bold", 54, ORANGE), "small": ("Medium", 32, MUTED)}


def font(weight, size):
    for p in (f"/usr/share/fonts/opentype/inter/Inter-{weight}.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def card_png(lines, path, maxw=960, x=60, y=150):
    pad, bar, gap = 34, 10, 10
    rows = []
    for ln in lines:
        weight, size, colour = STYLES[ln.get("style", "main")]
        f = font(weight, size)
        for i, t in enumerate(wrap(ln["text"], f, maxw - 2 * pad - bar)):
            rows.append((t, f, colour, size))
    widths = [r[1].getlength(r[0]) for r in rows]
    cw = int(max(widths) + 2 * pad + bar)
    ch = int(sum(r[3] * 1.22 for r in rows) + gap * (len(rows) - 1) + 2 * pad - 6)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x + 4, y + 10, x + cw + 4, y + ch + 10], 18, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill=(255, 255, 255, 245))
    d.rounded_rectangle([x, y, x + bar + 8, y + ch], 18, fill=BLUE + (255,))
    d.rectangle([x + bar, y, x + bar + 10, y + ch], fill=(255, 255, 255, 245))
    ty = y + pad - 4
    for t, f, colour, size in rows:
        d.text((x + bar + pad, ty), t, font=f, fill=colour)
        ty += size * 1.22 + gap
    img.save(path)


COVER_STYLES = {"main": ("Bold", 92, (255, 255, 255)), "accent": ("ExtraBold", 100, (251, 146, 60))}


def cover_jpg(bg, lines, sub, path, logo=os.path.join(ROOT, "TWD_Logo.png")):
    img = Image.open(bg).convert("RGB").resize((W, H), Image.LANCZOS)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for y in range(H):  # darker in the middle band where the headline sits
        a = int(110 + 90 * max(0.0, 1 - abs(y - H * 0.5) / (H * 0.32)))
        d.line([(0, y), (W, y)], fill=(8, 15, 30, a))
    img = Image.alpha_composite(img.convert("RGBA"), shade)
    d = ImageDraw.Draw(img)
    rows = []
    for ln in lines:
        weight, size, colour = COVER_STYLES[ln.get("style", "main")]
        f = font(weight, size)
        for t in wrap(ln["text"], f, W - 2 * 100):
            rows.append((t, f, colour, size))
    sf = font("Medium", 44)
    subrows = wrap(sub, sf, W - 2 * 120) if sub else []
    total = sum(r[3] * 1.15 for r in rows) + (40 + len(subrows) * 58 if subrows else 0)
    y = int(H * 0.5 - total / 2)
    for t, f, colour, size in rows:
        d.text(((W - f.getlength(t)) / 2, y), t, font=f, fill=colour)
        y += int(size * 1.15)
    if subrows:
        y += 40
        d.rounded_rectangle([W / 2 - 60, y - 22, W / 2 + 60, y - 16], 3, fill=(37, 99, 235))
        for t in subrows:
            d.text(((W - sf.getlength(t)) / 2, y), t, font=sf, fill=(226, 232, 240))
            y += 58
    if os.path.exists(logo):  # logo on a white pill, inside the 3:4 grid area
        lg = Image.open(logo).convert("RGBA")
        lg.thumbnail((210, 120))
        px, py = (W - lg.width) // 2, 300
        d.rounded_rectangle([px - 30, py - 18, px + lg.width + 30, py + lg.height + 18], 28, fill=(255, 255, 255, 240))
        img.alpha_composite(lg, (px, py))
    img.convert("RGB").save(path, quality=92)


def tiktok_variant(cover, reel, out, hold=0.5, xf=0.25):
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(hold + xf), "-i", cover,
         "-f", "lavfi", "-t", str(hold + xf), "-i", "anullsrc=r=48000:cl=stereo", "-i", reel,
         "-filter_complex",
         f"[0:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[c];[2:v]fps={FPS},format=yuv420p,setsar=1[r];"
         f"[c][r]xfade=transition=fade:duration={xf}:offset={hold},format=yuv420p[v];"
         f"[1:a][2:a]acrossfade=d={xf}[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac",
         "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", out])


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def has_audio(p):
    return bool(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", p]).strip())


def rel(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def main(spec_path):
    s = json.load(open(spec_path))
    out = rel(s["out"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = tempfile.mkdtemp()
    xf = s.get("xfade", 0.3)
    parts = []
    for i, c in enumerate(s["clips"]):
        src, p = rel(c["src"]), os.path.join(tmp, f"c{i}.mp4")
        vf = ""
        if s.get("delogo"):
            x, y, w, h = s["delogo"]
            vf += f"delogo=x={x}:y={y}:w={w}:h={h},"
        vf += f"scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,setsar=1"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(c.get("start", 0)), "-to", str(c["end"]), "-i", src]
        if not has_audio(src):
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest"]
        cmd += ["-vf", vf, "-af", "aresample=48000,aformat=channel_layouts=stereo", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "16", "-c:a", "aac", "-b:a", "192k", p]
        run(cmd)
        parts.append(p)
    if s.get("outro"):
        parts.append(rel(s["outro"]))
    # crossfade chain
    inputs, fv, fa = [], [], []
    for p in parts:
        inputs += ["-i", p]
    lv, la, t = "[0:v]", "[0:a]", dur(parts[0])
    for i in range(1, len(parts)):
        off = t - xf
        fv.append(f"{lv}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.3f}[v{i}]")
        fa.append(f"{la}[{i}:a]acrossfade=d={xf}[a{i}]")
        lv, la, t = f"[v{i}]", f"[a{i}]", off + dur(parts[i])
    total = t
    n = len(parts)
    # cards
    for j, c in enumerate(s.get("cards", [])):
        png = os.path.join(tmp, f"card{j}.png")
        card_png(c["lines"], png)
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", png]
        k = n + j
        fv.append(f"[{k}:v]format=rgba,fade=in:st={c['t0']}:d=0.25:alpha=1,fade=out:st={c['t1'] - 0.25}:d=0.25:alpha=1[k{j}]")
        fv.append(f"{lv}[k{j}]overlay=0:0:enable='between(t,{c['t0']},{c['t1']})'[o{j}]")
        lv = f"[o{j}]"
    # voice
    m = n + len(s.get("cards", []))
    vlabels = []
    for j, v in enumerate(s.get("voice", [])):
        inputs += ["-i", rel(v["wav"])]
        ms = int(v["at"] * 1000)
        fa.append(f"[{m + j}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[vo{j}]")
        vlabels.append(f"[vo{j}]")
    fa.append(f"{la}volume={s.get('ambient', 0.25)}[amb]")
    if vlabels:
        fa.append(f"{''.join(vlabels)}amix=inputs={len(vlabels)}:normalize=0[vo]")
        fa.append("[amb][vo]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    else:
        fa.append("[amb]loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    fv.append(f"{lv}format=yuv420p[vout]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fv + fa), "-map", "[vout]", "-map", "[aout]",
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS), "-c:a", "aac",
         "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", out])
    cover = out[:-4] + "-cover.jpg"
    if s.get("cover"):
        c = s["cover"]
        frame = os.path.join(tmp, "coverbg.png")
        vf = ""
        if s.get("delogo"):
            x, y, w, h = s["delogo"]
            vf = f"delogo=x={x}:y={y}:w={w}:h={h},"
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(c.get("t", 1)), "-i", rel(c["src"]), "-frames:v", "1",
             "-vf", vf + f"scale={W}:{H}:flags=lanczos", frame])
        cover_jpg(frame, c["lines"], c.get("sub", ""), cover)
        tiktok_variant(cover, out, out[:-4] + "-tiktok.mp4")
    else:
        first = s.get("cards", [{"t0": 0.5, "t1": 1}])[0]
        run(["ffmpeg", "-v", "error", "-y", "-ss", str((first["t0"] + first["t1"]) / 2), "-i", out, "-frames:v", "1", "-q:v", "3", cover])
    print(os.path.relpath(out, ROOT), f"{dur(out):.2f}s")


if __name__ == "__main__":
    if sys.argv[1] == "--tiktok-only":
        tiktok_variant(rel(sys.argv[2]), rel(sys.argv[3]), rel(sys.argv[3])[:-4] + "-tiktok.mp4")
    else:
        main(sys.argv[1])
