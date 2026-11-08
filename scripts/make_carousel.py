#!/usr/bin/env python3
"""Render a social carousel (1080x1350 PNG slides) from a JSON spec.

    python3 scripts/make_carousel.py specs/<name>.json

Spec format:
{
  "out_dir": "img/2026-11-02/ai-jobs",   # relative to repo root
  "prefix": "ai-jobs",                           # files: <prefix>-1.png ...
  "source": "Source: BLS OEWS; Anthropic Economic Index",
  "slides": [
    {"type": "title", "h1": "...", "p": "...", "kicker": "Swipe ->"},
    {"type": "stat",  "h2": "...", "big": "r = 0.01", "tone": "blue|amber", "p": "...", "small": "...", "chart": "blog/charts/x.svg"},
    {"type": "list",  "h2": "...", "items": ["<b>A</b> - 1 year", ...], "p": "...", "chart": "..."},
    {"type": "bars",  "h2": "...", "bars": [{"label": "...", "value": 5.1, "text": "5%"}], "highlight": 3, "p": "..."},
    {"type": "cta",   "h2": "...", "p": "...", "cta": "Check your area: link in bio", "small": "..."}
  ]
}
Text fields may contain simple inline HTML (<b>, <br>, &ndash;). Every number on a slide must
come from a published article, a data file in the repo, or a script in analysis/.
"""
import html as _html
import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#fff;font-family:Inter,sans-serif;color:#0f172a;position:relative;overflow:hidden}
.bar{position:absolute;top:0;left:0;right:0;height:14px;background:linear-gradient(90deg,#2563eb,#60a5fa)}
.logo{position:absolute;top:56px;left:80px;height:96px}
.n{position:absolute;top:84px;right:80px;font-size:30px;color:#94a3b8;font-weight:600}
.c{position:absolute;left:80px;right:80px;top:200px;bottom:130px;display:flex;flex-direction:column;justify-content:center}
h1{font-size:88px;line-height:1.05;font-weight:800;letter-spacing:-1.5px}
h2{font-size:62px;line-height:1.1;font-weight:800;letter-spacing:-1px}
p{font-size:38px;line-height:1.4;color:#334155;margin-top:28px}
.small{font-size:30px;color:#64748b}
.big{font-size:130px;font-weight:800;color:#2563eb;letter-spacing:-2.5px;line-height:1;margin-top:36px}
.amber{color:#d97706}
.kicker{font-size:44px;color:#2563eb;font-weight:700;margin-top:72px}
ul{margin-top:32px;padding-left:40px}li{font-size:40px;line-height:1.35;margin:16px 0 0;color:#334155}
b{color:#0f172a}
.chart{flex:0 1 auto;min-height:0;max-width:100%;max-height:560px;margin-top:32px;object-fit:contain;align-self:center}
.cta{display:inline-block;margin-top:52px;background:#2563eb;color:#fff;font-size:42px;font-weight:700;padding:28px 44px;border-radius:999px;align-self:flex-start}
.foot{position:absolute;left:80px;right:80px;bottom:64px;font-size:26px;color:#64748b;display:flex;justify-content:space-between;gap:24px}
.bars{margin-top:44px;display:flex;flex-direction:column;gap:26px}
.row .lab{font-size:32px;color:#334155;margin-bottom:10px}
.row .track{display:flex;align-items:center;gap:20px}
.row .fill{height:56px;border-radius:10px;background:#bfdbfe}
.row.hi .fill{background:#d97706}.row.hi .lab{color:#0f172a;font-weight:700}
.row .val{font-size:40px;font-weight:800;color:#0f172a}
"""


# Charts usually come from the website repo (e.g. blog/charts/x.svg). Clone truthwithdata/webstie next to
# this repo (../webstie), or set TWD_SITE to its path. A path that exists in this repo is used first.
SITE_DIR = os.environ.get("TWD_SITE", os.path.join(os.path.dirname(ROOT), "webstie"))


def chart_img(path):
    if not path:
        return ""
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        full = os.path.join(SITE_DIR, path)
    if not os.path.exists(full):
        sys.exit(f"chart not found: {path} (looked in this repo and {SITE_DIR}; clone truthwithdata/webstie there or set TWD_SITE)")
    return f'<img class="chart" src="file://{full}">'


def slide_body(s):
    t = s["type"]
    if t == "title":
        return f'<h1>{s["h1"]}</h1>' + (f'<p>{s["p"]}</p>' if s.get("p") else "") + \
            (f'<div class="kicker">{s["kicker"]}</div>' if s.get("kicker") else "")
    if t == "stat":
        tone = " amber" if s.get("tone") == "amber" else ""
        return (f'<h2>{s["h2"]}</h2>' if s.get("h2") else "") + f'<div class="big{tone}">{s["big"]}</div>' + \
            (f'<p>{s["p"]}</p>' if s.get("p") else "") + (f'<p class="small">{s["small"]}</p>' if s.get("small") else "") + \
            chart_img(s.get("chart"))
    if t == "list":
        items = "".join(f"<li>{i}</li>" for i in s["items"])
        return f'<h2>{s["h2"]}</h2><ul>{items}</ul>' + (f'<p>{s["p"]}</p>' if s.get("p") else "") + chart_img(s.get("chart"))
    if t == "bars":
        mx = max(b["value"] for b in s["bars"])
        rows = ""
        for i, b in enumerate(s["bars"]):
            w = max(4, 640 * b["value"] / mx)
            hi = " hi" if i == s.get("highlight") else ""
            rows += f'<div class="row{hi}"><div class="lab">{b["label"]}</div><div class="track"><div class="fill" style="width:{w:.0f}px"></div><div class="val">{b["text"]}</div></div></div>'
        return f'<h2>{s["h2"]}</h2><div class="bars">{rows}</div>' + (f'<p>{s["p"]}</p>' if s.get("p") else "")
    if t == "cta":
        return f'<h2>{s["h2"]}</h2>' + (f'<p>{s["p"]}</p>' if s.get("p") else "") + \
            f'<div class="cta">{s["cta"]}</div>' + (f'<p class="small">{s["small"]}</p>' if s.get("small") else "")
    raise ValueError(f"unknown slide type {t}")


def page(i, n, s, source):
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bar"></div>'
            f'<img class="logo" src="file://{ROOT}/TWD_Logo.png?v=3"><div class="n">{i}/{n}</div>'
            f'<div class="c">{slide_body(s)}</div>'
            f'<div class="foot"><span>truthwithdata.com</span><span>{source}</span></div></body></html>')


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    out_dir = os.path.join(ROOT, spec["out_dir"])
    os.makedirs(out_dir, exist_ok=True)
    slides = spec["slides"]
    tmp = os.path.join(out_dir, ".render.html")
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(slides, 1):
            open(tmp, "w", encoding="utf-8").write(page(i, len(slides), s, spec.get("source", "")))
            pg.goto("file://" + tmp)
            pg.wait_for_timeout(250)
            # catch text running off the slide
            overflow = pg.evaluate("() => { const c = document.querySelector('.c'); return c.scrollHeight > c.clientHeight + 2; }")
            if overflow:
                print(f"WARNING slide {i}: content overflows the slide, shorten it", file=sys.stderr)
            out = os.path.join(out_dir, f'{spec["prefix"]}-{i}.png')
            pg.screenshot(path=out, type="png")
            paths.append(os.path.relpath(out, ROOT))
        b.close()
    os.remove(tmp)
    print("\n".join(paths))


if __name__ == "__main__":
    main(sys.argv[1])
