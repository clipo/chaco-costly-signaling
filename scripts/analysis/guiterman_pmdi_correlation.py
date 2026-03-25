"""
Annual-resolution PMDI-construction correlation using Guiterman et al. (2015) timber data.

The severe test for P5 (lambda-sigma feedback).
Tests whether construction activity correlates with environmental uncertainty
at multiple temporal scales.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
PMDI_FILE = BASE / "data" / "processed" / "chaco_pmdi_simulation_input.csv"
TIMBER_FILE = BASE / "data" / "raw" / "construction_dates" / "guiterman_2015_dataset_s1.xls"
FIG_DIR = BASE / "figures" / "final"

COLORS = {
    'blue': '#0072B2', 'orange': '#D55E00', 'green': '#009E73',
    'yellow': '#E69F00', 'purple': '#CC79A7', 'cyan': '#56B4E9',
}


def load_timber_data():
    """Load and process Guiterman et al. 2015 sourced timber dates."""
    df = pd.read_excel(TIMBER_FILE, sheet_name='Specimen Table',
                       header=None, skiprows=3)
    df.columns = ['Great_House', 'TRL_ID', 'Measurement_ID', 'NPS_ID', 'Species',
                  'InnerDate', 'OuterDate', 'Series_Length', 'Source', 'Correlation',
                  't_value', 'p_value']
    # Extract numeric year from outer date
    df['year'] = df['OuterDate'].astype(str).str.extract(r'(\d+)').astype(float)
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    return df


def compute_annual_construction(timber_df, year_range=(850, 1150)):
    """Count timber cutting dates per year as construction activity proxy."""
    years = np.arange(year_range[0], year_range[1] + 1)
    counts = timber_df.groupby('year').size()
    activity = pd.DataFrame({'year': years})
    activity['timber_count'] = activity['year'].map(counts).fillna(0).astype(int)
    return activity


def main():
    pmdi = pd.read_csv(PMDI_FILE)
    timber = load_timber_data()
    construction = compute_annual_construction(timber)

    # Merge with PMDI
    merged = pd.merge(construction, pmdi[['year', 'pmdi']], on='year', how='inner')

    print("=" * 70)
    print("Guiterman et al. (2015) Timber Data - PMDI Correlation Analysis")
    print("=" * 70)
    print(f"Sourced specimens: {len(timber)}")
    print(f"Year range: {timber['year'].min()}-{timber['year'].max()}")
    print(f"Merged records: {len(merged)}")
    print()

    # Compute rolling PMDI variance at multiple windows
    windows = [10, 20, 30, 50]
    for w in windows:
        merged[f'pmdi_var_{w}'] = merged['pmdi'].rolling(w, center=True, min_periods=w//2).var()
        merged[f'pmdi_sd_{w}'] = merged['pmdi'].rolling(w, center=True, min_periods=w//2).std()

    # Also compute rolling construction activity (smoothed)
    for w in [10, 20]:
        merged[f'construction_{w}'] = merged['timber_count'].rolling(w, center=True, min_periods=w//2).sum()

    # Correlations at multiple scales
    print("--- Correlations: PMDI variance vs. construction activity ---")
    print("(Testing lambda-sigma prediction: higher variance -> more construction)")
    print()

    results = []
    for var_w in windows:
        for con_w in [10, 20]:
            var_col = f'pmdi_var_{var_w}'
            con_col = f'construction_{con_w}'
            valid = merged[[var_col, con_col]].dropna()
            if len(valid) < 10:
                continue
            r, p = stats.pearsonr(valid[var_col], valid[con_col])
            rho, p_rho = stats.spearmanr(valid[var_col], valid[con_col])
            results.append({
                'variance_window': var_w,
                'construction_window': con_w,
                'r_pearson': r, 'p_pearson': p,
                'r_spearman': rho, 'p_spearman': p_rho,
                'n': len(valid)
            })
            sig = "*" if p < 0.05 else ""
            sig_rho = "*" if p_rho < 0.05 else ""
            print(f"  PMDI var ({var_w}yr) vs construction ({con_w}yr): "
                  f"r={r:+.3f} (p={p:.4f}){sig}  "
                  f"rho={rho:+.3f} (p={p_rho:.4f}){sig_rho}  n={len(valid)}")

    # Also test: PMDI level vs construction (surplus model prediction)
    print()
    print("--- Correlations: PMDI level vs. construction activity ---")
    print("(Testing surplus model: higher PMDI (wetter) -> more construction)")
    print()
    for pmdi_w in [10, 20, 30]:
        merged[f'pmdi_mean_{pmdi_w}'] = merged['pmdi'].rolling(pmdi_w, center=True, min_periods=pmdi_w//2).mean()
        for con_w in [10, 20]:
            mean_col = f'pmdi_mean_{pmdi_w}'
            con_col = f'construction_{con_w}'
            valid = merged[[mean_col, con_col]].dropna()
            if len(valid) < 10:
                continue
            r, p = stats.pearsonr(valid[mean_col], valid[con_col])
            sig = "*" if p < 0.05 else ""
            print(f"  PMDI mean ({pmdi_w}yr) vs construction ({con_w}yr): "
                  f"r={r:+.3f} (p={p:.4f}){sig}  n={len(valid)}")

    # Save results
    pd.DataFrame(results).to_csv(
        BASE / "data" / "processed" / "guiterman_pmdi_correlations.csv", index=False
    )

    # Create figure
    create_figure(merged)


def create_figure(merged):
    """Multi-panel figure: timber dates, PMDI, and correlation."""
    fig, axes = plt.subplots(3, 1, figsize=(7, 7), sharex=True,
                              gridspec_kw={'height_ratios': [0.8, 1, 1.2], 'hspace': 0.15})

    years = merged['year']

    # Panel A: Timber cutting dates
    ax = axes[0]
    ax.bar(years, merged['timber_count'], width=1, color=COLORS['orange'],
           alpha=0.7, edgecolor='none')
    ax.plot(years, merged['construction_10'], color=COLORS['orange'],
            linewidth=1.5, label='10-yr moving sum')
    ax.set_ylabel('Timber specimens\n(annual)', fontsize=9, fontfamily='sans-serif')
    ax.legend(fontsize=8, loc='upper left', frameon=False)
    ax.text(0.02, 0.92, '(a) Construction activity (Guiterman et al. 2015)',
            transform=ax.transAxes, fontsize=9, fontfamily='sans-serif',
            fontweight='bold', va='top')

    # Panel B: PMDI and variance
    ax = axes[1]
    ax.fill_between(years, merged['pmdi'], 0,
                    where=merged['pmdi'] < 0, color=COLORS['blue'], alpha=0.2)
    ax.fill_between(years, merged['pmdi'], 0,
                    where=merged['pmdi'] >= 0, color=COLORS['cyan'], alpha=0.2)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylabel('PMDI', fontsize=9, fontfamily='sans-serif')

    ax2 = ax.twinx()
    ax2.plot(years, merged['pmdi_var_30'], color=COLORS['green'],
             linewidth=1.5, alpha=0.8)
    ax2.set_ylabel('PMDI variance\n(30-yr window)', fontsize=9,
                   fontfamily='sans-serif', color=COLORS['green'])
    ax2.tick_params(axis='y', labelcolor=COLORS['green'])
    ax.text(0.02, 0.92, '(b) PMDI and rolling variance',
            transform=ax.transAxes, fontsize=9, fontfamily='sans-serif',
            fontweight='bold', va='top')

    # Panel C: Scatter - variance vs construction
    ax = axes[2]
    w = 20  # Use 20-year windows for both
    valid = merged[['pmdi_var_30', 'construction_20']].dropna()

    scatter = ax.scatter(valid['pmdi_var_30'], valid['construction_20'],
                        c=merged.loc[valid.index, 'year'], cmap='viridis',
                        s=15, alpha=0.6, edgecolors='none')
    plt.colorbar(scatter, ax=ax, label='Year (CE)', shrink=0.8)

    # Regression line
    slope, intercept, r, p, se = stats.linregress(
        valid['pmdi_var_30'], valid['construction_20']
    )
    x_line = np.linspace(valid['pmdi_var_30'].min(), valid['pmdi_var_30'].max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color='black',
            linewidth=1, linestyle='--')
    ax.text(0.02, 0.92,
            f'(c) Variance vs. construction: r={r:.3f}, p={p:.4f}',
            transform=ax.transAxes, fontsize=9, fontfamily='sans-serif',
            fontweight='bold', va='top')
    ax.set_xlabel('PMDI variance (30-yr rolling window)', fontsize=9,
                  fontfamily='sans-serif')
    ax.set_ylabel('Construction activity\n(20-yr moving sum)', fontsize=9,
                  fontfamily='sans-serif')

    # Shade florescence and mark collapse
    for a in axes:
        a.axvspan(1020, 1130, alpha=0.06, color='orange')
        a.axvline(1130, color='red', linewidth=0.7, linestyle='--', alpha=0.4)

    axes[0].set_xlim(850, 1150)

    out = FIG_DIR / "Figure_14_guiterman_pmdi_correlation.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nFigure saved: {out}")


if __name__ == '__main__':
    main()
