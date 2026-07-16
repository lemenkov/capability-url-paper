#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Polina Lemenkova
# SPDX-License-Identifier: CC-BY-4.0
"""
Inline base64 vs. output-by-reference (fig01).

Two stacked panels:
  (a) status quo  -- inline base64, context cost linear in payload size
  (b) this work   -- output by reference, context cost O(1)
with a "301x reduction" marker linking the two LLM-context boxes.

    pip install matplotlib
    python plot_inline_vs_reference.py       # writes inline_vs_reference.png
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

W, H = 1360, 845
FONT = "DejaVu Sans"          # swap for "Helvetica"/"Arial" if installed

C = {"gray": "#4d4d4d", "green": "#2e9e33", "blue": "#2f6fb0",
     "red": "#c02b20", "orange": "#f57c00", "blue_title": "#1f6db5"}
FACE = {"gray": "#f0f0f0", "green": "#e9f6ea", "blue": "#e7eef7",
        "red": "#fbeceb", "orange": "#fdefe0"}

fig, ax = plt.subplots(figsize=(W / 100, H / 100), dpi=300)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)             # invert y -> top-left origin
ax.axis("off")


def box(x, y, w, h, key, lines, bold=False, fs=17, rad=14):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
        linewidth=2.4, edgecolor=C[key], facecolor=FACE[key], mutation_aspect=1))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center",
            fontsize=fs, family=FONT, color="#1a1a1a",
            fontweight="bold" if bold else "normal", linespacing=1.3)


def arrow(x1, y1, x2, y2, color, lw=2.6, double=False):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="<|-|>" if double else "-|>",
        mutation_scale=20, linewidth=lw, color=color, shrinkA=0, shrinkB=0))


# ======================================================================
# (a) Inline base64  --  top panel
# ======================================================================
ax.text(40, 55, "(a)", ha="left", va="center", fontsize=25,
        fontweight="bold", family=FONT, color="#1a1a1a")
ax.text(120, 55, "Inline base64 (status quo): context cost linear in payload size",
        ha="left", va="center", fontsize=24, fontweight="bold",
        family=FONT, color=C["red"])

box(40, 150, 200, 115, "gray", ["Tool", "execution"], bold=True)
box(330, 150, 200, 115, "gray", ["figure.png", "31 KB"])
box(620, 150, 265, 115, "orange", ["base64 encode", "(+33%)"])
box(965, 150, 355, 115, "red", ["LLM context", "27,702 tokens resident"], bold=True)

arrow(240, 207, 328, 207, C["gray"])
arrow(530, 207, 618, 207, C["gray"])
arrow(885, 207, 963, 207, C["gray"])

ax.text(680, 330,
        "re-processed every turn \u2022 survives summarization "
        "\u2022 persists in transcripts",
        ha="center", va="center", fontsize=19, style="italic",
        family=FONT, color=C["red"])

# ======================================================================
# (b) Output by reference  --  bottom panel
# ======================================================================
ax.text(40, 470, "(b)", ha="left", va="center", fontsize=25,
        fontweight="bold", family=FONT, color="#1a1a1a")
ax.text(120, 470, "Output by reference (this work): context cost O(1)",
        ha="left", va="center", fontsize=24, fontweight="bold",
        family=FONT, color=C["blue_title"])

box(40, 560, 200, 115, "gray", ["Tool", "execution"], bold=True)
box(330, 560, 200, 115, "gray", ["figure.png", "31 KB"])
box(560, 520, 375, 130, "blue",
    ["metadata record", "name \u00b7 bytes \u00b7 sha256",
     "mime \u00b7 url \u00b7 expires_in"])
box(985, 520, 335, 130, "blue",
    ["LLM context", "\u224892 tokens (fixed)"], bold=True)
box(575, 665, 285, 120, "green", ["out-of-band", "store (TTL)"])
box(905, 665, 415, 120, "gray",
    ["Consumer", "human viewer \u00b7 vision step"])

arrow(240, 617, 328, 617, C["gray"])                 # tool -> figure
arrow(520, 585, 556, 565, C["blue"])                 # figure -> metadata (up)
arrow(937, 585, 983, 585, C["blue"])                 # metadata -> LLM
arrow(515, 665, 600, 675, C["green"])                # figure -> store (bytes)
arrow(862, 725, 903, 725, C["green"])                # store -> consumer

ax.text(545, 695, "bytes", ha="center", va="center", fontsize=19,
        fontweight="bold", family=FONT, color=C["green"])
ax.text(717, 815, "fetch on demand", ha="center", va="center", fontsize=19,
        fontweight="bold", family=FONT, color=C["green"])

# ---- 301x reduction marker (links the two LLM-context boxes) ----------
arrow(1250, 440, 1250, 495, "#1a1a1a", lw=2.6, double=True)
ax.text(1290, 445, "301\u00d7", ha="left", va="center", fontsize=22,
        fontweight="bold", family=FONT, color="#1a1a1a")
ax.text(1290, 480, "reduction", ha="left", va="center", fontsize=22,
        family=FONT, color=C["gray"])

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig("fig01_inline_vs_reference.pdf", facecolor="white", bbox_inches="tight", pad_inches=0.12); fig.savefig("fig01_inline_vs_reference.png", dpi=150, facecolor="white", bbox_inches="tight", pad_inches=0.12)
print("wrote fig01_inline_vs_reference.pdf/.png")
