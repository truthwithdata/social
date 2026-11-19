#!/usr/bin/env python3
"""Simple social version of Figure 2 (left panel) of the Black Friday article.

Reads ../webstie/data/black-friday-price-index-2025-2026.csv (published with the article) and draws
the average best price of the 33 products as a % of each one's usual price. No new numbers: the
annotated low (86.1, i.e. 14% below usual on 1 Dec 2025) is the article's figure.

    python3 analysis/bf_price_index_chart.py img/2026-11-23/bf/price-index.png
"""
import os, sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("TWD_SITE", os.path.join(os.path.dirname(ROOT), "webstie"))
d = pd.read_csv(os.path.join(SITE, "data", "black-friday-price-index-2025-2026.csv"), parse_dates=["date"])
d["idx"] = d.avg_price_vs_usual * 100
low = d.loc[d.idx.idxmin()]
print(f"Lowest point: {low.date:%d %b %Y}, {low.idx:.1f}% of usual ({100 - low.idx:.0f}% below)")

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22})
fig, ax = plt.subplots(figsize=(9.2, 6.0), dpi=200)
ax.axvspan(pd.Timestamp("2025-11-21"), pd.Timestamp("2025-12-01"), color="#fde68a", alpha=0.8, lw=0)
ax.axhline(100, color="#94a3b8", lw=1.5, ls="--")
ax.plot(d.date, d.idx, color="#2563eb", lw=3)
ax.annotate("Black Friday to\nCyber Monday 2025:\n14% below usual", xy=(low.date, low.idx), xytext=(pd.Timestamp("2026-02-10"), 88.0),
            fontsize=20, color="#0f172a", arrowprops=dict(arrowstyle="-", color="#0f172a", lw=1.2), va="center")
ax.text(pd.Timestamp("2026-08-10"), 98.4, "usual price", fontsize=18, color="#64748b")
ax.set_ylabel("Average price, % of usual", fontsize=20, color="#334155")
ax.set_ylim(84, 114)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors="#334155", labelsize=18)
fig.tight_layout()
out = sys.argv[1] if len(sys.argv) > 1 else "price-index.png"
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
fig.savefig(out, facecolor="white")
