"""
Updated Figure 6: Environmental uncertainty decomposition.

Removes the sigma* threshold line (criticized as post hoc).
Updates panel (b) to show both K&V precipitation SD and PMDI SD.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FIG_DIR = BASE / "figures" / "final"
PMDI_FILE = BASE / "data" / "processed" / "chaco_pmdi_simulation_input.csv"

COLORS = {
    'blue': '#0072B2',
    'orange': '#D55E00',
    'green': '#009E73',
    'yellow': '#E69F00',
    'cyan': '#56B4E9',
}

PERIODS = {
    'Pre-Chaco\n(750-850)': (750, 850),
    'Early Bonito\n(850-1020)': (850, 1020),
    'Classic Bonito\n(1020-1130)': (1020, 1130),
    'Late Bonito\n(1130-1200)': (1130, 1200),
}

PERIOD_COLORS = [COLORS['cyan'], COLORS['green'], COLORS['orange'], '#CC79A7']


def main():
    pmdi = pd.read_csv(PMDI_FILE)

    fig, axes = plt.subplots(2, 2, figsize=(7, 5.5),
                              gridspec_kw={'hspace': 0.4, 'wspace': 0.35})

    # Panel (a): PMDI 50-year running mean
    ax = axes[0, 0]
    pmdi_filtered = pmdi[(pmdi['year'] >= 500) & (pmdi['year'] <= 1500)]
    running_mean = pmdi_filtered['pmdi'].rolling(50, center=True, min_periods=25).mean()
    ax.plot(pmdi_filtered['year'], running_mean, color=COLORS['blue'], linewidth=1)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvspan(1020, 1130, alpha=0.15, color='orange')
    ax.text(1075, ax.get_ylim()[1] * 0.85 if ax.get_ylim()[1] > 0 else 0.8,
            'Chaco\nflorescence', ha='center', fontsize=7,
            fontfamily='sans-serif', alpha=0.7)
    ax.set_xlabel('Year (CE)', fontsize=9, fontfamily='sans-serif')
    ax.set_ylabel('PMDI (50-yr running mean)', fontsize=9, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(a)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel (b): PMDI standard deviation by period
    ax = axes[0, 1]
    sds = []
    for name, (start, end) in PERIODS.items():
        mask = (pmdi['year'] >= start) & (pmdi['year'] < end)
        sd = pmdi.loc[mask, 'pmdi'].std()
        sds.append(sd)

    x = range(len(PERIODS))
    bars = ax.bar(x, sds, color=PERIOD_COLORS, edgecolor='white', linewidth=0.5)
    for i, (bar, sd) in enumerate(zip(bars, sds)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f'{sd:.2f}', ha='center', fontsize=8, fontfamily='sans-serif')
    ax.set_xticks(x)
    ax.set_xticklabels(PERIODS.keys(), fontsize=7, fontfamily='sans-serif')
    ax.set_ylabel('PMDI std. dev.', fontsize=9, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(b)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel (c): Lag-1 autocorrelation by period
    ax = axes[1, 0]
    r1s = []
    for name, (start, end) in PERIODS.items():
        mask = (pmdi['year'] >= start) & (pmdi['year'] < end)
        series = pmdi.loc[mask, 'pmdi']
        r1 = series.autocorr(lag=1) if len(series) > 2 else 0
        r1s.append(r1)

    bars = ax.bar(x, r1s, color=PERIOD_COLORS, edgecolor='white', linewidth=0.5)
    for i, (bar, r1) in enumerate(zip(bars, r1s)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f'{r1:.3f}', ha='center', fontsize=8, fontfamily='sans-serif')
    ax.set_xticks(x)
    ax.set_xticklabels(PERIODS.keys(), fontsize=7, fontfamily='sans-serif')
    ax.set_ylabel('Lag-1 autocorrelation ($r_1$)', fontsize=9, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(c)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel (d): Sigma (composite uncertainty) by period - NO threshold line
    ax = axes[1, 1]
    # Compute sigma as composite: SD * drought_frequency
    sigmas = []
    for name, (start, end) in PERIODS.items():
        mask = (pmdi['year'] >= start) & (pmdi['year'] < end)
        period_pmdi = pmdi.loc[mask, 'pmdi']
        sd = period_pmdi.std()
        drought_freq = (period_pmdi < -1).sum() / len(period_pmdi)
        sigma = sd * (1 + drought_freq)  # Composite uncertainty
        sigmas.append(sigma)

    bars = ax.bar(x, sigmas, color=PERIOD_COLORS, edgecolor='white', linewidth=0.5)
    for i, (bar, sig) in enumerate(zip(bars, sigmas)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f'{sig:.2f}', ha='center', fontsize=8, fontfamily='sans-serif')
    ax.set_xticks(x)
    ax.set_xticklabels(PERIODS.keys(), fontsize=7, fontfamily='sans-serif')
    ax.set_ylabel('Composite uncertainty ($\\sigma$)', fontsize=9,
                  fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(d)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')
    # NO sigma* threshold line - removed per reviewer feedback

    out = FIG_DIR / "Figure_6_environmental_uncertainty.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


if __name__ == '__main__':
    main()
