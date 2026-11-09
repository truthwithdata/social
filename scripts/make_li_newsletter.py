#!/usr/bin/env python3
"""Images for the LinkedIn newsletter (posted by hand from Vishal's profile; never automatically).

    python3 scripts/make_li_newsletter.py --logo img/brand/li-newsletter-logo-300.png
    python3 scripts/make_li_newsletter.py cover OUT.png --title "..." --date "16 November 2026" \
        [--image img/<monday>/<topic>/<slide>.png]

cover: 1920x1080 edition cover. Headline on the left, an optional carousel slide (1080x1350) on the
right. Keep the headline under about 60 characters; LinkedIn crops the edges a little in the feed,
so nothing important sits near them. Paths are relative to the repo root.
--logo: 300x300 newsletter logo (LinkedIn's recommended size).
"""
import argparse
import html
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = f"file://{ROOT}/TWD_Logo.png"

BASE = """*{margin:0;box-sizing:border-box}body{font-family:Inter,sans-serif;color:#0f172a;background:#fff;overflow:hidden;position:relative}
.bar{position:absolute;top:0;left:0;right:0;background:linear-gradient(90deg,#2563eb,#60a5fa)}"""


def render(markup, w, h, out):
    out = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        tmp = out + ".render.html"   # a file:// page, so local images load
        open(tmp, "w", encoding="utf-8").write(markup)
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(300)
        if pg.evaluate("() => { const c = document.querySelector('.txt'); return c && c.scrollHeight > c.clientHeight + 2; }"):
            print("WARNING: headline overflows, shorten it", file=sys.stderr)
        pg.screenshot(path=out, type="png")
        b.close()
    os.remove(tmp)
    print(os.path.relpath(out, ROOT))


def logo(out):
    css = BASE + """body{width:300px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.bar{height:10px}img{width:200px}.t{margin-top:14px;font-size:21px;font-weight:700;color:#2563eb;letter-spacing:.3px}"""
    render(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="bar"></div>'
           f'<img src="{LOGO}"><div class="t">One chart, worked through</div></body></html>', 300, 300, out)


def cover(out, title, date, image):
    css = BASE + """body{width:1920px;height:1080px}.bar{height:16px}
.logo{position:absolute;top:110px;left:150px;height:120px}
.txt{position:absolute;left:150px;top:300px;width:{TW}px;height:560px;display:flex;flex-direction:column;justify-content:center}
.k{font-size:34px;font-weight:700;color:#2563eb;letter-spacing:1.5px;text-transform:uppercase}
h1{font-size:80px;line-height:1.05;font-weight:800;letter-spacing:-2px;margin-top:28px}
.d{font-size:34px;color:#64748b;margin-top:36px}
.foot{position:absolute;left:150px;bottom:90px;font-size:30px;color:#64748b}
.slide{position:absolute;right:150px;top:110px;height:860px;border-radius:18px;box-shadow:0 20px 60px rgba(15,23,42,.18)}
.mask{position:absolute;left:1600px;top:145px;width:170px;height:60px;background:#fff}"""
    css = css.replace("{TW}", "860" if image else "1500")
    # the slide's "n/7" counter means nothing on a cover, so it is masked
    slide = f'<img class="slide" src="file://{os.path.join(ROOT, image)}"><div class="mask"></div>' if image else ""
    render(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="bar"></div>'
           f'<img class="logo" src="{LOGO}"><div class="txt"><div class="k">Truth with Data newsletter</div>'
           f'<h1>{html.escape(title)}</h1><div class="d">{html.escape(date)}</div></div>{slide}'
           f'<div class="foot">truthwithdata.com</div></body></html>', 1920, 1080, out)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--logo":
        logo(sys.argv[2])
        sys.exit()
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["cover"])
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--image")
    a = ap.parse_args()
    cover(a.out, a.title, a.date, a.image)
