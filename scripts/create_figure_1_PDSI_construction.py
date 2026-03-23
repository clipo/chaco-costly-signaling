"""
Figure 1: PDSI Time Series with Construction Overlay (800-1200 CE)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------- style setup ----------
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
})

# Okabe-Ito palette selections
OI_BLUE = '#0072B2'
OI_ORANGE = '#E69F00'
OI_RED = '#D55E00'
OI_SKY = '#56B4E9'
OI_GRAY = '#999999'

# ---------- load data ----------
pmdi = pd.read_csv(
    '/Users/clipo/PycharmProjects/chaco-signaling/data/processed/chaco_pmdi_averaged.csv'
)
constr = pd.read_csv(
    '/Users/clipo/PycharmProjects/chaco-signaling/data/raw/construction_dates/construction_episodes.csv'
)

# Filter to 800-1200
pmdi_sub = pmdi[(pmdi['year'] >= 800) & (pmdi['year'] <= 1200)].copy()
constr_sub = constr[(constr['year'] >= 800) & (constr['year'] <= 1200)].copy()

# ---------- figure ----------
fig, ax1 = plt.subplots(figsize=(7, 4))

# Period shading
periods = [
    (850, 1020, 'Early Bonito\n(850\u20131020)', '#F0E442', 0.12),
    (1020, 1130, 'Classic Bonito\n(1020\u20131130)', '#56B4E9', 0.12),
    (1130, 1200, 'Late Bonito\n(1130\u20131200)', '#D55E00', 0.10),
]
for start, end, label, color, alpha in periods:
    ax1.axvspan(start, end, color=color, alpha=alpha, zorder=0)
    mid = (start + end) / 2
    ax1.text(mid, ax1.get_ylim()[0] if ax1.get_ylim()[0] != 0 else -7.5,
             '', fontsize=7, ha='center', va='bottom', color='#555555')

# PMDI bars: wet (blue) vs. dry (red-orange)
colors_pmdi = [OI_BLUE if v >= 0 else OI_RED for v in pmdi_sub['pmdi'].values]
ax1.bar(pmdi_sub['year'], pmdi_sub['pmdi'], width=1.0, color=colors_pmdi,
        alpha=0.55, zorder=2, linewidth=0)
ax1.set_ylabel('PMDI (Palmer Modified Drought Index)', fontsize=10)
ax1.set_xlabel('Year (CE)', fontsize=10)
ax1.set_xlim(800, 1200)
ax1.axhline(0, color='black', linewidth=0.5, zorder=1)

# Mark 1130 megadrought onset
ax1.axvline(1130, color=OI_RED, linewidth=1.2, linestyle='--', zorder=3, alpha=0.8)
ax1.annotate('1130 CE\nmegadrought\nonset', xy=(1130, ax1.get_ylim()[1] if ax1.get_ylim()[1] != 0 else 6),
             xytext=(1155, 6.5), fontsize=7.5, ha='left', va='top',
             arrowprops=dict(arrowstyle='->', color=OI_RED, lw=1.0),
             color=OI_RED)

# Period labels at top
for start, end, label, color, alpha in periods:
    mid = (start + end) / 2
    ax1.text(mid, 8.8, label, fontsize=7, ha='center', va='top',
             color='#444444', style='italic')

# Construction overlay on secondary y-axis
ax2 = ax1.twinx()
ax2.fill_between(constr_sub['year'], 0, constr_sub['timber_count'],
                 color=OI_ORANGE, alpha=0.35, step='mid', zorder=1,
                 label='Timber count')
ax2.plot(constr_sub['year'], constr_sub['timber_count'],
         color=OI_ORANGE, linewidth=1.3, zorder=2, drawstyle='steps-mid')
ax2.set_ylabel('Timber count (construction proxy)', fontsize=10, color=OI_ORANGE)
ax2.tick_params(axis='y', labelcolor=OI_ORANGE)
ax2.set_ylim(0, 300)

# Clean up gridlines
ax1.grid(False)
ax2.grid(False)
ax1.set_ylim(-8, 9)

# Tick formatting
ax1.tick_params(axis='both', which='both', direction='out', length=4)
ax2.tick_params(axis='y', which='both', direction='out', length=4)

# Spines
for spine in ['top']:
    ax1.spines[spine].set_visible(False)
    ax2.spines[spine].set_visible(False)

fig.tight_layout()

outpath = '/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_1_PDSI_construction.png'
fig.savefig(outpath, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'Saved: {outpath}')
