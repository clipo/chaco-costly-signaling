#!/usr/bin/env python3
"""
Create Figure 11: Predictions Across Alternative Frameworks.

A table-style figure comparing what four theoretical frameworks predict
for each of eight observables relevant to Chaco Canyon.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

row_labels = [
    "Investment\ndistribution",
    "Exotic goods\ndistribution",
    "Great house\nplacement",
    "Violence\npatterns",
    "Construction\ntiming",
    "Network\nconnectivity",
    "Renovation\npatterns",
    "Collapse\nmechanism",
]

col_labels = [
    "Observable",
    "Signaling Model",
    "Hierarchy Model",
    "Ritual Model",
    "Ecological Model",
]

# Each inner list: [Signaling, Hierarchy, Ritual, Ecological]
cell_text = [
    [
        "Quality-dependent,\ncontinuous gradient",
        "Elite-controlled,\nbinary division",
        "Cosmologically\ndetermined",
        "Proportional to\nlocal surplus",
    ],
    [
        "Concentrated by\ncost-capacity",
        "Monopolized by\nruling elite",
        "Distributed by\nceremonial role",
        "Redistributed for\nsubsistence needs",
    ],
    [
        "Maximize landscape\nvisibility",
        "Near elite\nresidences",
        "Astronomical or\ncosmological alignment",
        "Near productive\nland and water",
    ],
    [
        "Low during signaling,\nhigh after collapse",
        "Low under strong\nauthority",
        "Low during\nshared belief",
        "Tracks resource\nscarcity directly",
    ],
    [
        "Tracks uncertainty,\nnot surplus",
        "Tracks political\nconsolidation",
        "Tracks ceremonial\ncalendar",
        "Tracks favorable\nconditions",
    ],
    [
        "Co-evolves with\nconstruction",
        "Radiates from\npolitical center",
        "Follows pilgrimage\nroutes",
        "Follows trade and\nsubsistence needs",
    ],
    [
        "Continuous (signal\ndepreciation)",
        "As needed\nfor function",
        "Timed to renewal\nceremonies",
        "As resources\nallow",
    ],
    [
        "Sigma exceeds\nbuffering capacity",
        "Loss of political\nauthority",
        "Loss of faith\nor ideology",
        "Carrying capacity\nexceeded",
    ],
]

n_rows = len(row_labels)
n_cols = 4  # framework columns (excluding Observable label column)

# ---------------------------------------------------------------------------
# Colours  (colorblind-friendly, muted)
# ---------------------------------------------------------------------------

header_color = "#4A4A4A"          # dark grey header
header_text_color = "white"

# Column background colours (very light, pastel)
col_colors = [
    "#D6EAF8",  # Signaling: light blue (highlighted)
    "#FAE5D3",  # Hierarchy: light orange
    "#D5F5E3",  # Ritual: light green
    "#F5EEF8",  # Ecological: light lavender
]

row_alt_light = 1.0   # multiplier for even rows
row_alt_dark  = 0.92  # multiplier for odd rows (subtle zebra)

observable_bg = "#F2F2F2"

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------

fig_width = 7.0
fig_height = 5.0

fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Try to use Arial; fall back to DejaVu Sans
try:
    fm.findfont("Arial", fallback_to_default=False)
    font_family = "Arial"
except Exception:
    font_family = "DejaVu Sans"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [font_family, "DejaVu Sans", "Helvetica"]

# ---------------------------------------------------------------------------
# Layout parameters
# ---------------------------------------------------------------------------

left_margin = 0.005
right_margin = 0.005
top_margin = 0.02
bottom_margin = 0.02

table_left = left_margin
table_right = 1.0 - right_margin
table_top = 1.0 - top_margin
table_bottom = bottom_margin

table_width = table_right - table_left
table_height = table_top - table_bottom

# Column widths (fractions of table_width)
obs_col_frac = 0.145
framework_frac = (1.0 - obs_col_frac) / n_cols

# Row heights
header_frac = 0.07
row_frac = (1.0 - header_frac) / n_rows

# Convert fractions to absolute coordinates
def col_x(col_idx):
    """Return (x_left, x_right) for a column index.
       col_idx 0 = Observable; 1-4 = framework columns."""
    if col_idx == 0:
        x_left = table_left
        x_right = table_left + obs_col_frac * table_width
    else:
        x_left = table_left + (obs_col_frac + (col_idx - 1) * framework_frac) * table_width
        x_right = x_left + framework_frac * table_width
    return x_left, x_right


def row_y(row_idx):
    """Return (y_bottom, y_top) for a row index.
       row_idx -1 = header; 0..n_rows-1 = data rows (top to bottom)."""
    if row_idx == -1:
        y_top = table_top
        y_bottom = table_top - header_frac * table_height
    else:
        y_top = table_top - header_frac * table_height - row_idx * row_frac * table_height
        y_bottom = y_top - row_frac * table_height
    return y_bottom, y_top


def draw_cell(ax, x_left, x_right, y_bottom, y_top, facecolor, text,
              fontsize=7, fontweight="normal", text_color="black",
              ha="center", va="center"):
    """Draw a filled rectangle with centred text."""
    from matplotlib.patches import FancyBboxPatch
    width = x_right - x_left
    height = y_top - y_bottom
    rect = plt.Rectangle((x_left, y_bottom), width, height,
                          facecolor=facecolor, edgecolor="#CCCCCC",
                          linewidth=0.5, clip_on=False)
    ax.add_patch(rect)
    cx = (x_left + x_right) / 2
    cy = (y_bottom + y_top) / 2
    ax.text(cx, cy, text, fontsize=fontsize, fontweight=fontweight,
            color=text_color, ha=ha, va=va, linespacing=1.25,
            clip_on=False, fontfamily=font_family)

# ---------------------------------------------------------------------------
# Draw header row
# ---------------------------------------------------------------------------

for ci in range(5):
    xl, xr = col_x(ci)
    yb, yt = row_y(-1)
    draw_cell(ax, xl, xr, yb, yt,
              facecolor=header_color,
              text=col_labels[ci],
              fontsize=7.5, fontweight="bold",
              text_color=header_text_color)

# ---------------------------------------------------------------------------
# Draw data rows
# ---------------------------------------------------------------------------

for ri in range(n_rows):
    yb, yt = row_y(ri)
    # Zebra-stripe multiplier
    shade = row_alt_dark if ri % 2 == 1 else row_alt_light

    # Observable column
    xl, xr = col_x(0)
    bg = tuple(c * shade for c in matplotlib.colors.to_rgb(observable_bg))
    draw_cell(ax, xl, xr, yb, yt,
              facecolor=bg,
              text=row_labels[ri],
              fontsize=7, fontweight="bold",
              text_color="#333333")

    # Framework columns
    for ci in range(n_cols):
        xl, xr = col_x(ci + 1)
        base_rgb = matplotlib.colors.to_rgb(col_colors[ci])
        bg = tuple(c * shade for c in base_rgb)
        fw = "bold" if ci == 0 else "normal"
        tc = "#1A3A5C" if ci == 0 else "#333333"
        draw_cell(ax, xl, xr, yb, yt,
                  facecolor=bg,
                  text=cell_text[ri][ci],
                  fontsize=6.8, fontweight=fw,
                  text_color=tc)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

out_path = "/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_11_model_comparison.png"
fig.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0.05,
            facecolor="white")
plt.close(fig)
print(f"Saved: {out_path}")
