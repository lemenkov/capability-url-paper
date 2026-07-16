#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Polina Lemenkova
# SPDX-License-Identifier: CC-BY-4.0
"""
MCP output-publishing workflow (fig02).

Recreates the 7-stage diagram: sandboxed execution -> _publish_outputs ->
staging store -> nginx serve, the metadata-record branch to the MCP client,
consumers, and the GC-timer / sweep loop, plus a legend of arrow styles
and numbered steps.

    pip install matplotlib
    python plot_output_publishing.py         # writes output_publishing.png
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

W, H = 1320, 740
FONT = "DejaVu Sans"          # swap for "Helvetica"/"Arial" if installed
BADGE = "#3a3a3a"

fig, ax = plt.subplots(figsize=(W / 100, H / 100), dpi=300)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)             # invert y -> top-left origin
ax.axis("off")


def box(x, y, w, h, edge, face, lines, bold=False, fs=15, rad=16, lh=1.3):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
        linewidth=2.2, edgecolor=edge, facecolor=face, mutation_aspect=1))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center",
            fontsize=fs, family=FONT, color="#1a1a1a",
            fontweight="bold" if bold else "normal", linespacing=lh)


def badge(cx, cy, num, r=23):
    ax.add_patch(Circle((cx, cy), r, facecolor=BADGE, edgecolor="none", zorder=5))
    ax.text(cx, cy, num, ha="center", va="center", color="white",
            fontsize=16, fontweight="bold", family=FONT, zorder=6)


def arrow(x1, y1, x2, y2, color, dashed=False, lw=2.2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=18,
        linewidth=lw, color=color, shrinkA=0, shrinkB=0,
        linestyle="--" if dashed else "-"))


def line(pts, color, dashed=False, lw=2.2):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, linewidth=lw,
            linestyle="--" if dashed else "-", solid_capstyle="round")


C = {"gray": "#4d4d4d", "green": "#2e9e33", "blue": "#1f6db5",
     "purple": "#9b4fca", "red": "#e02b20", "cyan": "#0898a8",
     "orange": "#f57c00", "magenta": "#c0207f"}

# ---- arrows -----------------------------------------------------------
arrow(290, 102, 372, 102, C["gray"])                       # 1 -> 2  files
arrow(725, 100, 827, 100, C["green"])                      # 2 -> 3  bytes
arrow(420, 197, 420, 216, C["blue"])                       # 2 -> 4
arrow(960, 177, 960, 296, C["purple"])                     # 3 -> 5  serve
arrow(458, 382, 458, 583, C["blue"], dashed=True)          # 4 -> 6  dereference
line([(880, 477), (880, 632)], C["purple"], dashed=True)   # 5 -> 6 (elbow)
arrow(880, 632, 782, 632, C["purple"], dashed=True)
arrow(950, 588, 950, 479, C["red"], dashed=True)           # 7 -> 5  after TTL
line([(1172, 660), (1245, 660), (1245, 118)], C["red"], dashed=True)   # 7 -> 3
arrow(1245, 118, 1190, 118, C["red"], dashed=True)

# ---- boxes + badges ---------------------------------------------------
box(40, 40, 250, 135, C["cyan"], "#e2f6f8",
    ["Sandboxed", "execution", "(MCP tool call)"])
box(375, 35, 350, 162, C["orange"], "#fdefe0",
    ["_publish_outputs", "size \u00b7 SHA-256 \u00b7 MIME",
     "token = CSPRNG, 256 bit", "move to staging"])
box(830, 40, 355, 135, C["green"], "#e9f6ea",
    ["Staging store (tmpfs)", "/outputs/<token>/figure.png",
     "mode 0755 \u00b7 SELinux label"])
box(55, 220, 410, 160, C["blue"], "#e7eef6",
    ["MCP client \u2192 model context", "metadata record only",
     "\u224890\u2013100 tokens, O(1)"])
box(760, 300, 410, 175, C["purple"], "#f1e9f8",
    ["nginx  /sandbox-out/", "autoindex off \u00b7 access_log off",
     "TLS \u00b7 noindex \u00b7 no auth", "(token = authorization)"], lh=1.35)
box(425, 590, 355, 140, C["magenta"], "#f9e6f1",
    ["Consumers (on demand)", "human browser \u00b7 agent fetch",
     "\u00b7 later multimodal step"])
box(815, 590, 355, 140, C["red"], "#fbeceb",
    ["GC timer (15 min)", "delete <token>/ older",
     "than TTL = 60 min \u2192 404"])

for cx, cy, n in [(40, 40, "1"), (375, 35, "2"), (830, 40, "3"),
                  (55, 220, "4"), (760, 300, "5"), (425, 590, "6"),
                  (815, 590, "7")]:
    badge(cx, cy, n)

# ---- edge labels ------------------------------------------------------
def lbl(x, top, color, lines, fs=15):
    for i, t in enumerate(lines):
        ax.text(x, top + 12 + i * 31, t, ha="left", va="center",
                fontsize=fs, family=FONT, color=color)

lbl(300, 66, C["gray"], ["files"])
lbl(748, 62, C["green"], ["bytes"])
lbl(985, 205, C["purple"], ["serve"])
lbl(505, 200, C["blue"],
    ["tool result:", "{name, bytes, sha256,", "mime, url, expires_in}"])
lbl(480, 486, C["blue"], ["dereference URI", "only if needed"])
lbl(690, 486, C["purple"], ["HTTPS GET", "capability URL"])
lbl(990, 505, C["red"], ["after TTL:", "404"])
ax.text(1258, 340, "sweep staging tree", rotation=-90, rotation_mode="anchor",
        ha="left", va="center", fontsize=15, family=FONT, color=C["red"])

# ---- legend -----------------------------------------------------------
ax.add_patch(FancyBboxPatch(
    (40, 386), 335, 344, boxstyle="round,pad=0,rounding_size=12",
    linewidth=2, edgecolor="#c9a300", facecolor="#fdf6db"))
lx = 56
ax.text(lx, 409, "Legend:", ha="left", va="center", fontsize=14,
        fontweight="bold", family=FONT, color="#1a1a1a")
ax.text(lx, 437, "Arrow styles", ha="left", va="center", fontsize=14,
        fontweight="bold", family=FONT, color="#1a1a1a")
ax.plot([lx, lx + 48], [467, 467], color="#4d4d4d", linewidth=2.2)
ax.text(lx + 60, 467, "solid \u2014 eager transfer", ha="left", va="center",
        fontsize=14, family=FONT, color="#1a1a1a")
ax.plot([lx, lx + 48], [497, 497], color="#4d4d4d", linewidth=2.2,
        linestyle=(0, (4, 3)))
ax.text(lx + 60, 497, "dashed \u2014 on-demand", ha="left", va="center",
        fontsize=14, family=FONT, color="#1a1a1a")
ax.text(lx, 528, "Steps", ha="left", va="center", fontsize=14,
        fontweight="bold", family=FONT, color="#1a1a1a")

steps = ["Sandboxed execution", "_publish_outputs", "Staging store (tmpfs)",
         "MCP client \u2192 model context", "nginx serve", "Consumers",
         "GC timer"]
for i, t in enumerate(steps):
    cy = 560 + i * 25
    ax.add_patch(Circle((lx + 11, cy), 11, facecolor=BADGE, edgecolor="none"))
    ax.text(lx + 11, cy, str(i + 1), ha="center", va="center", color="white",
            fontsize=8, fontweight="bold", family=FONT)
    ax.text(lx + 30, cy, t, ha="left", va="center", fontsize=14,
            family=FONT, color="#1a1a1a")

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig("fig02_reference_workflow.pdf", facecolor="white", bbox_inches="tight", pad_inches=0.12); fig.savefig("fig02_reference_workflow.png", dpi=150, facecolor="white", bbox_inches="tight", pad_inches=0.12)
print("wrote fig02_reference_workflow.pdf/.png")
