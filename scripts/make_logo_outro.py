#!/usr/bin/env python3
"""Render the reusable Truth with Data logo outro (1080x1920, 3 s, 30 fps, H.264 + silent AAC).

    python3 scripts/make_logo_outro.py [OUT.mp4]      # default img/brand/logo-outro-1080x1920.mp4

The logo is revealed left to right (like a line being drawn), settles with a slight zoom, then
the site address fades in. Append it to any Reel with make_reel.py --outro, or add it in an editor
after a Gemini (Veo) clip. Also writes a 1080x1080 square version for LinkedIn video.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, SECS = 30, 3.0


def font(size, weight="SemiBold"):
    for p in (f"/usr/share/fonts/opentype/inter/Inter-{weight}.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def render(out, W, H):
    logo = Image.open(os.path.join(ROOT, "TWD_Logo.png")).convert("RGBA")
    bbox = logo.getbbox()                      # the PNG has a lot of white margin
    logo = logo.crop(bbox)
    lw = int(W * 0.62)
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    f_url, f_tag = font(int(W * 0.046), "SemiBold"), font(int(W * 0.034), "Regular")
    url, tag = "truthwithdata.com", "Questions people argue about, answered with data"
    n = int(FPS * SECS)
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(n):
            t = i / FPS
            bg = Image.new("RGB", (W, H), "white")
            d = ImageDraw.Draw(bg)
            for x in range(W):                 # brand gradient bar, #2563eb -> #60a5fa
                k = x / (W - 1)
                d.line([(x, 0), (x, 18)], fill=(int(0x25 + k * 0x3b), int(0x63 + k * 0x42), int(0xeb + k * 0x0f)))
            reveal = ease((t - 0.15) / 0.9)    # left-to-right wipe, 0.15-1.05 s
            scale = 0.94 + 0.06 * ease((t - 0.15) / 1.6)
            lg = logo.resize((int(logo.width * scale), int(logo.height * scale)), Image.LANCZOS)
            cut = int(lg.width * reveal)
            if cut > 0:
                part = lg.crop((0, 0, cut, lg.height))
                x0, y0 = (W - lg.width) // 2, int(H * 0.46) - lg.height // 2
                bg.paste(part, (x0, y0), part)
            a = ease((t - 1.15) / 0.6)         # address and tagline fade in
            if a > 0:
                col = tuple(int(255 - a * (255 - c)) for c in (0x0f, 0x17, 0x2a))
                col2 = tuple(int(255 - a * (255 - c)) for c in (0x64, 0x74, 0x8b))
                y = int(H * 0.46) + logo.height // 2 + int(H * 0.035)
                w_ = d.textlength(url, font=f_url)
                d.text(((W - w_) / 2, y), url, font=f_url, fill=col)
                w2 = d.textlength(tag, font=f_tag)
                d.text(((W - w2) / 2, y + int(W * 0.075)), tag, font=f_tag, fill=col2)
            bg.save(os.path.join(tmp, f"{i:04d}.png"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                        "-f", "lavfi", "-t", f"{SECS}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(os.path.relpath(out, ROOT))


if __name__ == "__main__":
    out = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "img/brand/logo-outro-1080x1920.mp4")
    render(out, 1080, 1920)
    render(out.replace("1080x1920", "1080x1080") if "1080x1920" in out else out[:-4] + "-square.mp4", 1080, 1080)
