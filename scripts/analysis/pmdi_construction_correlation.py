"""
PMDI-Construction Correlation Analysis

Correlates rolling-window PMDI variance (environmental uncertainty)
with construction activity from great house chronology data.
Tests the lambda-sigma prediction (Prediction 5) at multiple temporal scales.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
BASE = Path(__file__).resolve().parents[2]
PMDI_FILE = BASE / "data" / "processed" / "chaco_pmdi_simulation_input.csv"
CHRONOLOGY_FILE = BASE / "data" / "raw" / "construction_dates" / "great_house_chronology.csv"
OUTPUT_DIR = BASE / "figures" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load PMDI and construction chronology data."""
    pmdi = pd.read_csv(PMDI_FILE)
    chrono = pd.read_csv(CHRONOLOGY_FILE)
    return pmdi, chrono


def compute_construction_activity(chrono, year_range):
    """
    Compute annual construction activity index.
    For each year, count how many great houses were under active construction.
    Weighted by peak_rooms where available.
    """
    years = np.arange(year_range[0], year_range[1] + 1)
    activity = np.zeros(len(years))
    weighted_activity = np.zeros(len(years))

    for _, row in chrono.iterrows():
        start = int(row['major_construction_start'])
        end = int(row['major_construction_end'])
        # Skip great kiva (no room count)
        try:
            rooms = int(row['peak_rooms'])
        except (ValueError, TypeError):
            rooms = 50  # default for non-numeric entries

        for i, y in enumerate(years):
            if start <= y <= end:
                activity[i] += 1
                weighted_activity[i] += rooms / (end - start + 1)

    df = pd.DataFrame({
        'year': years,
        'n_active_projects': activity,
        'weighted_construction': weighted_activity
    })
    return df


def compute_rolling_variance(pmdi, windows=[10, 20, 30, 50]):
    """Compute rolling-window PMDI variance at multiple temporal scales."""
    result = pmdi[['year', 'pmdi']].copy()
    for w in windows:
        result[f'pmdi_var_{w}yr'] = result['pmdi'].rolling(
            window=w, center=True, min_periods=w // 2
        ).var()
        result[f'pmdi_sd_{w}yr'] = result['pmdi'].rolling(
            window=w, center=True, min_periods=w // 2
        ).std()
    return result


def correlate_at_scale(merged, var_col, activity_col, window_label):
    """Compute Pearson and Spearman correlations, return summary."""
    valid = merged[[var_col, activity_col]].dropna()
    if len(valid) < 10:
        return None

    r_pearson, p_pearson = stats.pearsonr(valid[var_col], valid[activity_col])
    r_spearman, p_spearman = stats.spearmanr(valid[var_col], valid[activity_col])

    return {
        'window': window_label,
        'n': len(valid),
        'r_pearson': r_pearson,
        'p_pearson': p_pearson,
        'r_spearman': r_spearman,
        'p_spearman': p_spearman
    }


def run_analysis():
    """Main analysis pipeline."""
    pmdi, chrono = load_data()

    # Focus on the Chaco period with buffer
    year_range = (750, 1250)

    # Compute construction activity
    construction = compute_construction_activity(chrono, year_range)

    # Compute rolling PMDI variance
    windows = [10, 20, 30, 50]
    pmdi_stats = compute_rolling_variance(pmdi, windows)

    # Merge datasets
    merged = pd.merge(construction, pmdi_stats, on='year', how='inner')

    # Also compute decadal aggregates for a cleaner signal
    merged['decade'] = (merged['year'] // 10) * 10
    decadal = merged.groupby('decade').agg({
        'n_active_projects': 'mean',
        'weighted_construction': 'sum',
        'pmdi': 'var',
        **{f'pmdi_var_{w}yr': 'mean' for w in windows},
        **{f'pmdi_sd_{w}yr': 'mean' for w in windows}
    }).reset_index()
    decadal.rename(columns={'pmdi': 'pmdi_var_decadal'}, inplace=True)

    # Run correlations at multiple scales
    print("=" * 70)
    print("PMDI Variance - Construction Activity Correlations")
    print("=" * 70)
    print(f"\nAnalysis period: {year_range[0]}-{year_range[1]} CE")
    print(f"Data: PMDI from LBDA v2 (Gille et al. 2017)")
    print(f"Construction: Great house chronology (n={len(chrono)} structures)")
    print()

    results = []

    # Annual-resolution correlations with rolling windows
    print("--- Annual resolution, rolling-window PMDI variance ---")
    for w in windows:
        var_col = f'pmdi_var_{w}yr'
        res = correlate_at_scale(merged, var_col, 'n_active_projects', f'{w}-year')
        if res:
            results.append(res)
            print(f"  {w}-year window: r={res['r_pearson']:.3f} (p={res['p_pearson']:.4f}), "
                  f"rho={res['r_spearman']:.3f} (p={res['p_spearman']:.4f}), n={res['n']}")

    # Decadal correlations
    print("\n--- Decadal aggregates ---")
    for w in windows:
        var_col = f'pmdi_var_{w}yr'
        res = correlate_at_scale(decadal, var_col, 'weighted_construction', f'{w}-year (decadal)')
        if res:
            results.append(res)
            print(f"  {w}-year window: r={res['r_pearson']:.3f} (p={res['p_pearson']:.4f}), "
                  f"rho={res['r_spearman']:.3f} (p={res['p_spearman']:.4f}), n={res['n']}")

    # Save results
    results_df = pd.DataFrame(results)
    results_path = BASE / "data" / "processed" / "pmdi_construction_correlations.csv"
    results_df.to_csv(results_path, index=False)
    print(f"\nResults saved to {results_path}")

    # Create figure
    create_figure(merged, decadal, windows, year_range)

    return results


def create_figure(merged, decadal, windows, year_range):
    """Create multi-panel figure showing PMDI variance and construction co-evolution."""
    fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True,
                              gridspec_kw={'height_ratios': [1.2, 1, 1.2]})

    # Color palette (Okabe-Ito derived)
    colors = {
        'pmdi': '#0072B2',
        'construction': '#D55E00',
        'variance': '#009E73',
        'scatter': '#CC79A7'
    }

    # Panel A: PMDI time series
    ax = axes[0]
    ax.fill_between(merged['year'], merged['pmdi'], 0,
                    where=merged['pmdi'] < 0, color=colors['pmdi'],
                    alpha=0.3, label='Drought (PMDI < 0)')
    ax.fill_between(merged['year'], merged['pmdi'], 0,
                    where=merged['pmdi'] >= 0, color='#56B4E9',
                    alpha=0.3, label='Wet (PMDI >= 0)')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylabel('PMDI', fontsize=10, fontfamily='sans-serif')
    ax.legend(fontsize=8, loc='upper left', frameon=False)
    ax.text(0.02, 0.95, '(a)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    # Shade Chaco florescence
    for a in axes:
        a.axvspan(1020, 1130, alpha=0.08, color='orange')
        a.axvline(1130, color='red', linewidth=0.8, linestyle='--', alpha=0.5)

    # Panel B: Rolling PMDI variance + construction activity
    ax = axes[1]
    w = 30  # Use 30-year window as primary
    ax.plot(merged['year'], merged[f'pmdi_var_{w}yr'],
            color=colors['variance'], linewidth=1.5,
            label=f'PMDI variance ({w}-yr window)')
    ax.set_ylabel(f'PMDI variance\n({w}-yr window)', fontsize=10,
                  fontfamily='sans-serif', color=colors['variance'])
    ax.tick_params(axis='y', labelcolor=colors['variance'])

    ax2 = ax.twinx()
    ax2.bar(decadal['decade'] + 5, decadal['weighted_construction'],
            width=8, color=colors['construction'], alpha=0.6,
            label='Construction activity')
    ax2.set_ylabel('Construction\n(weighted rooms/decade)', fontsize=10,
                   fontfamily='sans-serif', color=colors['construction'])
    ax2.tick_params(axis='y', labelcolor=colors['construction'])

    ax.text(0.02, 0.95, '(b)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel C: Scatter plot of decadal variance vs construction
    ax = axes[2]
    valid = decadal[[f'pmdi_var_{w}yr', 'weighted_construction']].dropna()
    # Color by time period
    decades_valid = decadal.loc[valid.index, 'decade']
    scatter = ax.scatter(valid[f'pmdi_var_{w}yr'],
                        valid['weighted_construction'],
                        c=decades_valid, cmap='viridis',
                        s=40, edgecolors='white', linewidth=0.5,
                        alpha=0.8)
    cbar = plt.colorbar(scatter, ax=ax, label='Decade (CE)', shrink=0.8)

    # Add regression line
    slope, intercept, r, p, se = stats.linregress(
        valid[f'pmdi_var_{w}yr'], valid['weighted_construction']
    )
    x_line = np.linspace(valid[f'pmdi_var_{w}yr'].min(),
                         valid[f'pmdi_var_{w}yr'].max(), 100)
    ax.plot(x_line, slope * x_line + intercept,
            color='black', linewidth=1, linestyle='--',
            label=f'r = {r:.3f}, p = {p:.4f}')
    ax.legend(fontsize=9, loc='upper left', frameon=False)

    ax.set_xlabel(f'PMDI variance ({w}-yr rolling window)', fontsize=10,
                  fontfamily='sans-serif')
    ax.set_ylabel('Construction activity\n(weighted rooms/decade)', fontsize=10,
                  fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(c)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    axes[0].set_xlim(year_range)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "Figure_12_pmdi_construction_correlation.png"
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"\nFigure saved to {out_path}")
    plt.close()


if __name__ == '__main__':
    run_analysis()
