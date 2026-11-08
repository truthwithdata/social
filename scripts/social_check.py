#!/usr/bin/env python3
"""Validate the social media queue, and list what is due to post.

    python3 scripts/social_check.py                 # validate every file in queue/
    python3 scripts/social_check.py queue/2026-11-02.json   # validate one file
    python3 scripts/social_check.py --due           # JSON list of posts due now (Europe/London), not yet posted

Queue file format (queue/<monday YYYY-MM-DD>.json):
{
  "week": "2026-11-02",
  "posts": [
    {"id": "2026-11-03-li-rent-vs-buy", "date": "2026-11-03", "time": "08:00",
     "platform": "linkedin",            # linkedin | instagram | x | newsletter | reddit
     "kind": "carousel",                # instagram only: carousel (default) | reel | story
     "video": "img/.../x.mp4",   # instagram reel or linkedin video post: the MP4; "cover" = optional JPG (instagram)
     "subject": "...",                  # newsletter: subject line; "text" = HTML body
     "text": "...",                     # linkedin post text / instagram caption
     "first_comment": "...",            # linkedin only, optional: posted as the first comment (links go here)
     "images": ["img/..."],      # repo paths; served at https://truthwithdata.github.io/social/<path>
     "thread": ["...", "..."],          # x only: one string per post in the thread
     "subreddit": "dataisbeautiful",    # reddit: target community without "r/" (u_truthwithdata = own profile)
     "title": "...",                    # reddit: post title (max 300 characters)
     "flair": "OC",                     # reddit, optional: flair text to pick (matched case-insensitively)
     "url": "https://...",              # reddit link posts only
     "note": "..."}                     # optional, for the reviewer; never posted

Reddit kinds: "image" (exactly one image, uploaded natively; first_comment carries the explanation and links),
"self" (markdown body in "text"; optional "first_comment"), "link" ("url"). Links to truthwithdata.com in
Reddit text must carry utm_source=reddit.
  ]
}
Only files on the main branch are posted: merging the weekly pull request is the approval.
"""
import json
import os
import re
import struct
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "queue")
POSTED = os.path.join(ROOT, "posted.json")
# Media is served by GitHub Pages from this repo (truthwithdata/social), not by the website,
# so merging a week of posts never triggers a Netlify deploy.
MEDIA = "https://truthwithdata.github.io/social"
SLOTS = {"08:00", "19:00"}
VIDEO_EXT = (".mp4",)  # the poster runs at 07:55 and 18:55 UK time
TZ = ZoneInfo("Europe/London")
URL_RE = re.compile(r"https?://\S+")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", head[16:24])
    try:
        from PIL import Image
        return Image.open(path).size
    except Exception:
        return None


def x_len(text):
    # X counts every URL as 23 characters
    return len(URL_RE.sub("x" * 23, text))


def load_queue_files(paths=None):
    if not paths:
        paths = sorted(os.path.join(QUEUE_DIR, f) for f in os.listdir(QUEUE_DIR) if f.endswith(".json"))
    return [(p, json.load(open(p, encoding="utf-8"))) for p in paths]


def validate(files):
    errors, seen = [], {}
    for path, q in files:
        rel = os.path.relpath(path, ROOT)
        for i, p in enumerate(q.get("posts", [])):
            where = f"{rel} post {i} ({p.get('id', '?')})"
            for k in ("id", "date", "time", "platform"):
                if not p.get(k):
                    errors.append(f"{where}: missing {k}")
            if p.get("id") in seen:
                errors.append(f"{where}: duplicate id (also in {seen[p['id']]})")
            seen[p.get("id")] = rel
            try:
                datetime.strptime(p.get("date", ""), "%Y-%m-%d")
            except ValueError:
                errors.append(f"{where}: date must be YYYY-MM-DD")
            if p.get("time") not in SLOTS:
                errors.append(f"{where}: time must be one of {sorted(SLOTS)}")
            plat = p.get("platform")
            imgs = p.get("images", [])
            for im in imgs:
                fp = os.path.join(ROOT, im)
                if not os.path.exists(fp):
                    errors.append(f"{where}: image not found {im}")
                elif plat == "instagram" and p.get("kind", "carousel") == "carousel":
                    size = png_size(fp)
                    if size:
                        w, h = size
                        if not (0.8 - 1e-3 <= w / h <= 1.91 + 1e-3):
                            errors.append(f"{where}: {im} is {w}x{h}; Instagram needs an aspect ratio between 4:5 and 1.91:1")
            if plat == "linkedin":
                if not p.get("text") or len(p["text"]) > 3000:
                    errors.append(f"{where}: LinkedIn text required, max 3,000 characters")
                if len(p.get("first_comment", "")) > 1250:
                    errors.append(f"{where}: first_comment max 1,250 characters")
                if len(imgs) > 20:
                    errors.append(f"{where}: LinkedIn allows at most 20 images")
                if p.get("video"):
                    v = p["video"]
                    if imgs:
                        errors.append(f"{where}: a LinkedIn post has either images or a video, not both")
                    if not v.endswith(VIDEO_EXT) or not os.path.exists(os.path.join(ROOT, v)):
                        errors.append(f"{where}: LinkedIn video needs an existing .mp4 in 'video'")
                    elif os.path.getsize(os.path.join(ROOT, v)) > 200 * 1024 * 1024:
                        errors.append(f"{where}: LinkedIn video over 200 MB")
            elif plat == "instagram":
                cap = p.get("text", "")
                kind = p.get("kind", "carousel")
                if len(cap) > 2200:
                    errors.append(f"{where}: Instagram caption max 2,200 characters")
                if cap.count("#") > 30:
                    errors.append(f"{where}: Instagram allows at most 30 hashtags")
                if kind == "carousel" and not 1 <= len(imgs) <= 10:
                    errors.append(f"{where}: Instagram carousel needs 1 to 10 images")
                elif kind == "reel":
                    v = p.get("video", "")
                    if not v.endswith(VIDEO_EXT) or not os.path.exists(os.path.join(ROOT, v)):
                        errors.append(f"{where}: reel needs an existing .mp4 in 'video'")
                    elif os.path.getsize(os.path.join(ROOT, v)) > 100 * 1024 * 1024:
                        errors.append(f"{where}: reel video over 100 MB")
                    if p.get("cover") and not os.path.exists(os.path.join(ROOT, p["cover"])):
                        errors.append(f"{where}: cover not found {p['cover']}")
                elif kind == "story":
                    if len(imgs) != 1:
                        errors.append(f"{where}: a story needs exactly 1 image")
                    elif (size := png_size(os.path.join(ROOT, imgs[0]))) and abs(size[0] / size[1] - 9 / 16) > 0.02:
                        errors.append(f"{where}: story image should be 9:16 (1080x1920)")
                elif kind not in ("carousel", "reel", "story"):
                    errors.append(f"{where}: kind must be carousel, reel or story")
            elif plat == "x":
                th = p.get("thread") or ([p["text"]] if p.get("text") else [])
                if not th:
                    errors.append(f"{where}: X post needs text or thread")
                for j, t in enumerate(th):
                    if x_len(t) > 280:
                        errors.append(f"{where}: X post {j + 1} is {x_len(t)} characters (max 280)")
                if len(imgs) > 4:
                    errors.append(f"{where}: X allows at most 4 images (attached to the first post)")
            elif plat == "reddit":
                kind = p.get("kind", "self")
                sub = p.get("subreddit", "")
                if not sub or sub.startswith(("r/", "/")):
                    errors.append(f"{where}: reddit needs 'subreddit' without the r/ prefix")
                if not p.get("title") or len(p["title"]) > 300:
                    errors.append(f"{where}: reddit title required, max 300 characters")
                if len(p.get("first_comment", "")) > 10000:
                    errors.append(f"{where}: reddit first_comment max 10,000 characters")
                if kind == "image":
                    if len(imgs) != 1:
                        errors.append(f"{where}: a reddit image post needs exactly 1 image")
                    elif not imgs[0].lower().endswith((".png", ".jpg", ".jpeg")):
                        errors.append(f"{where}: reddit image must be PNG or JPG")
                    elif os.path.exists(os.path.join(ROOT, imgs[0])) and os.path.getsize(os.path.join(ROOT, imgs[0])) > 20 * 1024 * 1024:
                        errors.append(f"{where}: reddit image over 20 MB")
                    if p.get("text"):
                        errors.append(f"{where}: reddit image posts have no body; put the explanation in first_comment")
                elif kind == "self":
                    if not p.get("text") or len(p["text"]) > 40000:
                        errors.append(f"{where}: reddit self post needs text, max 40,000 characters")
                    if imgs:
                        errors.append(f"{where}: reddit self posts take no images; link the chart in the text")
                elif kind == "link":
                    if not str(p.get("url", "")).startswith("https://"):
                        errors.append(f"{where}: reddit link post needs an https url")
                else:
                    errors.append(f"{where}: reddit kind must be image, self or link")
                for field in ("text", "first_comment", "url"):
                    for u in URL_RE.findall(p.get(field, "") or ""):
                        if "truthwithdata.com" in u and "utm_source=reddit" not in u and "/social/img/" not in u:
                            errors.append(f"{where}: link in {field} needs utm_source=reddit: {u}")
            elif plat == "newsletter":
                if not p.get("subject") or not p.get("text"):
                    errors.append(f"{where}: newsletter needs subject and text (HTML)")
            else:
                errors.append(f"{where}: platform must be linkedin, instagram, x, newsletter or reddit")
    return errors


def posted_ids():
    if not os.path.exists(POSTED):
        return set()
    return {r["id"] for r in json.load(open(POSTED, encoding="utf-8")).get("posted", [])}


def due(now=None):
    now = now or datetime.now(TZ)
    done = posted_ids()
    out = []
    for _, q in load_queue_files():
        for p in q.get("posts", []):
            if p["id"] in done:
                continue
            at = datetime.strptime(f'{p["date"]} {p["time"]}', "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
            # due if its slot is within the next 20 minutes or passed earlier today
            if at.date() == now.date() and at <= now + timedelta(minutes=20):
                item = dict(p)
                item["image_urls"] = [f"{MEDIA}/{im}" for im in p.get("images", [])]
                for k in ("video", "cover"):
                    if p.get(k):
                        item[k + "_url"] = f"{MEDIA}/{p[k]}"
                item["slot_iso"] = at.isoformat()
                out.append(item)
    return out


def main():
    args = sys.argv[1:]
    if args and args[0] == "--due":
        errs = validate(load_queue_files())
        if errs:
            print(json.dumps({"errors": errs}, indent=2))
            sys.exit(1)
        print(json.dumps(due(), indent=2, ensure_ascii=False))
        return
    errs = validate(load_queue_files([os.path.abspath(a) for a in args] or None))
    for e in errs:
        print("ERROR", e)
    print(f"social queue: {len(errs)} error(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
