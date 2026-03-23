"""
Figure 6: Environmental Uncertainty Decomposition (2x2 multi-panel)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ---------- style setup ----------
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 9,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
})

# Okabe-Ito palette
OI_BLUE = '#0072B2'
OI_ORANGE = '#E69F00'
OI_RED = '#D55E00'
OI_SKY = '#56B4E9'
OI_GREEN = '#009E73'
OI_VERMILLION = '#D55E00'
OI_YELLOW = '#F0E442'

# ---------- load PMDI data ----------
pmdi = pd.read_csv(
    '/Users/clipo/PycharmProjects/chaco-signaling/data/processed/chaco_pmdi_averaged.csv'
)

# ---------- figure ----------
fig, axes = plt.subplots(2, 2, figsize=(7, 5.5))

# ========== Panel (a): 50-year running mean, 500-1500 CE ==========
ax = axes[0, 0]
pmdi_full = pmdi[(pmdi['year'] >= 500) & (pmdi['year'] <= 1500)].copy()
pmdi_full = pmdi_full.sort_values('year')
pmdi_full['smooth50'] = pmdi_full['pmdi'].rolling(window=50, center=True, min_periods=25).mean()

ax.plot(pmdi_full['year'], pmdi_full['smooth50'], color=OI_BLUE, linewidth=1.3)
ax.axhline(0, color='black', linewidth=0.4)
# Shade Chaco florescence
ax.axvspan(1020, 1130, color=OI_ORANGE, alpha=0.2, zorder=0)
ax.text(1075, ax.get_ylim()[0] if ax.get_ylim()[0] != 0 else -0.5, 'Chaco\nflorescence',
        fontsize=7, ha='center', va='bottom', color=OI_ORANGE, style='italic')
ax.set_xlabel('Year (CE)', fontsize=9)
ax.set_ylabel('PMDI (50-yr running mean)', fontsize=9)
ax.set_xlim(500, 1500)
ax.grid(False)
# Re-draw after data is plotted to position text properly
ylims_a = ax.get_ylim()
ax.texts[0].set_position((1075, ylims_a[1] * 0.75))
ax.text(0.03, 0.95, '(a)', transform=ax.transAxes, fontsize=11,
        fontweight='bold', va='top', ha='left')

# ========== Panel (b): Period-specific variability (std dev) ==========
ax = axes[0, 1]
periods_b = ['Pueblo I\n(750\u2013850)', 'Early Bonito\n(850\u20131020)',
             'Classic Bonito\n(1020\u20131130)', 'Late Bonito\n(1130\u20131200)']
stds = [1.51, 1.59, 1.94, 1.73]
bar_colors_b = [OI_SKY, OI_GREEN, OI_ORANGE, OI_RED]

bars = ax.bar(range(len(periods_b)), stds, color=bar_colors_b, width=0.65,
              edgecolor='white', linewidth=0.5)
ax.set_xticks(range(len(periods_b)))
ax.set_xticklabels(periods_b, fontsize=7.5)
ax.set_ylabel('Precipitation std. dev. (s)', fontsize=9)
ax.set_ylim(0, 2.3)
ax.grid(False)
# Add value labels on bars
for bar, val in zip(bars, stds):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.04,
            f'{val:.2f}', ha='center', va='bottom', fontsize=7.5)
ax.text(0.03, 0.95, '(b)', transform=ax.transAxes, fontsize=11,
        fontweight='bold', va='top', ha='left')

# ========== Panel (c): Period-specific autocorrelation (r1) ==========
ax = axes[1, 0]
periods_c = ['Pueblo I\n(750\u2013850)', 'Early Bonito\n(850\u20131020)',
             'Classic Bonito\n(1020\u20131130)', 'Late Bonito\n(1130\u20131200)']
r1_vals = [0.146, 0.305, 0.275, 0.231]
bar_colors_c = [OI_SKY, OI_GREEN, OI_ORANGE, OI_RED]

bars = ax.bar(range(len(periods_c)), r1_vals, color=bar_colors_c, width=0.65,
              edgecolor='white', linewidth=0.5)
ax.set_xticks(range(len(periods_c)))
ax.set_xticklabels(periods_c, fontsize=7.5)
ax.set_ylabel('Lag-1 autocorrelation (r$_1$)', fontsize=9)
ax.set_ylim(0, 0.40)
ax.grid(False)
for bar, val in zip(bars, r1_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.008,
            f'{val:.3f}', ha='center', va='bottom', fontsize=7.5)
ax.text(0.03, 0.95, '(c)', transform=ax.transAxes, fontsize=11,
        fontweight='bold', va='top', ha='left')

# ========== Panel (d): Derived sigma values by period ==========
ax = axes[1, 1]
periods_d = ['Pre-Chaco\n(800\u2013900)', 'Early Chaco\n(900\u20131000)',
             'Florescence\n(1000\u20131130)', 'Megadrought\n(1130\u20131150)']
sigma_vals = [0.135, 0.142, 0.168, 0.195]
bar_colors_d = [OI_SKY, OI_GREEN, OI_ORANGE, OI_RED]

bars = ax.bar(range(len(periods_d)), sigma_vals, color=bar_colors_d, width=0.65,
              edgecolor='white', linewidth=0.5)
ax.set_xticks(range(len(periods_d)))
ax.set_xticklabels(periods_d, fontsize=7.5)
ax.set_ylabel('Environmental uncertainty (\u03c3)', fontsize=9)
ax.set_ylim(0, 0.24)
ax.grid(False)
# Critical threshold line
ax.axhline(0.15, color='black', linewidth=1.0, linestyle='--', zorder=3)
ax.text(3.4, 0.153, '\u03c3* \u2248 0.15', fontsize=7.5, ha='right', va='bottom',
        color='black')
for bar, val in zip(bars, sigma_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
            f'{val:.3f}', ha='center', va='bottom', fontsize=7.5)
ax.text(0.03, 0.95, '(d)', transform=ax.transAxes, fontsize=11,
        fontweight='bold', va='top', ha='left')

# ---------- cleanup ----------
for a in axes.flat:
    for spine in ['top', 'right']:
        a.spines[spine].set_visible(False)
    a.tick_params(axis='both', direction='out', length=3)

fig.tight_layout(h_pad=1.2, w_pad=1.5)

outpath = '/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_6_environmental_uncertainty.png'
fig.savefig(outpath, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'Saved: {outpath}')
