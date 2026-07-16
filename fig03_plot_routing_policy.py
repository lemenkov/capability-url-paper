#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Polina Lemenkova
# SPDX-License-Identifier: CC-BY-4.0
"""
Output Routing Policy flowchart.

Recreates the "Tool output -> textual AND <= 4 KB?" routing diagram:
decision diamond, inline branch, return-by-reference metadata box, the
bounded-cost annotation, and the three URI-scheme delivery boxes.

    pip install matplotlib
    python plot_routing_policy.py            # writes routing_policy.png
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

# ----------------------------------------------------------------------
# Canvas: work in pixel-like coords with y increasing downward (top-left
# origin), so the numbers match the layout directly.
W, H = 1360, 800
FONT = "DejaVu Sans"          # swap for "Helvetica"/"Arial" if installed

COL = {
    "gray":   ("#4d4d4d", "#f0f0f0"),
    "green":  ("#2e9e33", "#e9f6ea"),
    "blue":   ("#2f6fb0", "#e7eef7"),
    "purple": ("#7c3fb4", "#ece3f6"),
    "orange": ("#f57c00", "#fdefe0"),
}

fig, ax = plt.subplots(figsize=(W / 100, H / 100), dpi=300)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)             # invert y -> top-left origin
ax.axis("off")


def box(x, y, w, h, key, lines, bold=False, fs=15, rad=12):
    edge, face = COL[key]
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={rad}",
        linewidth=2.2, edgecolor=edge, facecolor=face, mutation_aspect=1))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines),
            ha="center", va="center", fontsize=fs, family=FONT,
            fontweight="bold" if bold else "normal",
            color="#1a1a1a", linespacing=1.35)


def arrow(x1, y1, x2, y2, color, dashed=False, lw=2.2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=18, linewidth=lw,
        color=color, linestyle="--" if dashed else "-",
        shrinkA=0, shrinkB=0))


def line(x1, y1, x2, y2, color="#4d4d4d", lw=2.2):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, solid_capstyle="round")


# ---- decision diamond -------------------------------------------------
ax.add_patch(Polygon(
    [(620, 70), (785, 150), (620, 230), (455, 150)],
    closed=True, linewidth=2.2,
    edgecolor=COL["orange"][0], facecolor=COL["orange"][1]))
ax.text(620, 150, "textual AND\n\u2264 4 KB ?", ha="center", va="center",
        fontsize=16, family=FONT, color="#1a1a1a", linespacing=1.3)

# ---- boxes ------------------------------------------------------------
box(40, 100, 200, 100, "gray", ["Tool", "output"], bold=True, fs=17)
box(1030, 83, 290, 134, "green",
    ["Inline in tool result", "legible to the model", "(\u22480.6 tokens/byte)"])
box(360, 333, 520, 152, "blue",
    ["Return by reference \u2014 metadata record,",
     "\u224890\u2013100 tokens:  {name, bytes,",
     "sha256, mime, url, expires_in}"])
box(945, 333, 395, 152, "blue",
    ["Bounded Output Context Cost", "cost O(1) in payload size;",
     "bytes fetched only on demand"], bold=True)
box(40, 598, 360, 158, "purple",
    ["https://  capability URL", "cross-host, out-of-band store",
     "bearer token (256-bit CSPRNG)", "TTL + GC \u00b7 measured herein"])
box(480, 598, 360, 158, "green",
    ["file:///  co-located", "shared filesystem (stdio",
     "subprocess server)", "trust = file permissions"])
box(925, 598, 360, 158, "orange",
    ["MCP resource link", "fetched via resources/read",
     "over the existing session", "trust = session auth"])

# ---- arrows -----------------------------------------------------------
arrow(242, 150, 453, 150, COL["gray"][0])                 # tool -> diamond
arrow(787, 150, 1028, 150, COL["green"][0])               # diamond -> inline (yes)
arrow(620, 232, 620, 333, COL["blue"][0])                 # diamond -> metadata (no)
arrow(948, 410, 884, 410, COL["blue"][0])                 # bounded -> metadata

# distribution bus + three coloured branches
line(620, 487, 620, 555)
line(220, 555, 1105, 555)
arrow(220, 555, 220, 597, COL["purple"][0])
arrow(660, 555, 660, 597, COL["green"][0])
arrow(1105, 555, 1105, 597, COL["orange"][0])

# ---- edge labels + caption -------------------------------------------
ax.text(905, 128, "yes", ha="center", va="center",
        fontsize=15, family=FONT, color=COL["green"][0])
ax.text(660, 290, "no", ha="center", va="center",
        fontsize=15, family=FONT, color=COL["blue"][0])
ax.text(680, 784,
        "The URI scheme selects the delivery and trust model; "
        "the metadata record is identical across all three.",
        ha="center", va="center", fontsize=15, family=FONT,
        style="italic", color="#4d4d4d")

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig("fig03_routing_policy.pdf", facecolor="white", bbox_inches="tight", pad_inches=0.12); fig.savefig("fig03_routing_policy.png", dpi=150, facecolor="white", bbox_inches="tight", pad_inches=0.12)
print("wrote fig03_routing_policy.pdf/.png")
