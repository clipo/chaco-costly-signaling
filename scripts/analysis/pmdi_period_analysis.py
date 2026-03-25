"""
Period-level PMDI variance vs. construction intensity analysis.

Tests Prediction 5 at the temporal scale the model specifies:
decadal-to-century periods, not annual resolution.
The construction chronology data provides broad construction spans,
not annual timber counts (which would require the Guiterman et al. 2015
240,000-timber dataset not yet integrated).
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
CHRONOLOGY_FILE = BASE / "data" / "raw" / "construction_dates" / "great_house_chronology.csv"
OUTPUT_DIR = BASE / "figures" / "final"

# Archaeological periods following Kantner and Vaughn (2012)
PERIODS = {
    'Pre-Chaco (750-850)': (750, 850),
    'Early Bonito (850-1020)': (850, 1020),
    'Classic Bonito (1020-1130)': (1020, 1130),
    'Late/Post-Chaco (1130-1250)': (1130, 1250),
}


def main():
    pmdi = pd.read_csv(PMDI_FILE)
    chrono = pd.read_csv(CHRONOLOGY_FILE)

    print("=" * 70)
    print("Period-Level PMDI Variance vs. Construction Activity")
    print("=" * 70)

    results = []
    for name, (start, end) in PERIODS.items():
        mask = (pmdi['year'] >= start) & (pmdi['year'] < end)
        period_pmdi = pmdi.loc[mask, 'pmdi']

        # PMDI statistics
        pmdi_mean = period_pmdi.mean()
        pmdi_sd = period_pmdi.std()
        pmdi_var = period_pmdi.var()
        n_drought_years = (period_pmdi < -1).sum()
        n_years = len(period_pmdi)

        # Autocorrelation (lag-1) as measure of predictability
        if len(period_pmdi) > 2:
            r1 = period_pmdi.autocorr(lag=1)
        else:
            r1 = np.nan

        # Construction activity: count structures under construction
        active_houses = 0
        total_rooms_built = 0
        new_starts = 0
        for _, row in chrono.iterrows():
            cs = int(row['major_construction_start'])
            ce = int(row['major_construction_end'])
            try:
                rooms = int(row['peak_rooms'])
            except (ValueError, TypeError):
                rooms = 50

            # Was this house under construction during this period?
            overlap_start = max(cs, start)
            overlap_end = min(ce, end)
            if overlap_start < overlap_end:
                active_houses += 1
                # Proportion of rooms built during this period
                total_span = ce - cs + 1
                period_span = overlap_end - overlap_start
                total_rooms_built += rooms * (period_span / total_span)

            # Did construction start during this period?
            if start <= cs < end:
                new_starts += 1

        results.append({
            'period': name,
            'start': start,
            'end': end,
            'n_years': n_years,
            'pmdi_mean': pmdi_mean,
            'pmdi_sd': pmdi_sd,
            'pmdi_var': pmdi_var,
            'pmdi_r1': r1,
            'n_drought_years': n_drought_years,
            'drought_frequency': n_drought_years / n_years,
            'active_houses': active_houses,
            'rooms_built': total_rooms_built,
            'rooms_per_decade': total_rooms_built / (n_years / 10),
            'new_starts': new_starts,
        })

    df = pd.DataFrame(results)

    print("\nPeriod Statistics:")
    print("-" * 70)
    for _, row in df.iterrows():
        print(f"\n{row['period']}:")
        print(f"  PMDI: mean={row['pmdi_mean']:.2f}, "
              f"SD={row['pmdi_sd']:.2f}, "
              f"var={row['pmdi_var']:.3f}, "
              f"r1={row['pmdi_r1']:.3f}")
        print(f"  Drought: {row['n_drought_years']}/{row['n_years']} years "
              f"({row['drought_frequency']:.1%})")
        print(f"  Construction: {row['active_houses']} active houses, "
              f"{row['rooms_built']:.0f} rooms built, "
              f"{row['rooms_per_decade']:.1f} rooms/decade, "
              f"{row['new_starts']} new starts")

    # Key test: does the period with highest construction (Classic Bonito)
    # also have the highest PMDI variance?
    print("\n" + "=" * 70)
    print("Key Comparison: Classic Bonito vs. Other Periods")
    print("=" * 70)

    classic = df[df['period'].str.contains('Classic')].iloc[0]
    early = df[df['period'].str.contains('Early')].iloc[0]

    print(f"\nClassic Bonito: SD={classic['pmdi_sd']:.3f}, "
          f"r1={classic['pmdi_r1']:.3f}, "
          f"rooms/decade={classic['rooms_per_decade']:.1f}")
    print(f"Early Bonito:   SD={early['pmdi_sd']:.3f}, "
          f"r1={early['pmdi_r1']:.3f}, "
          f"rooms/decade={early['rooms_per_decade']:.1f}")
    print(f"\nSD ratio (Classic/Early): {classic['pmdi_sd']/early['pmdi_sd']:.2f}")
    print(f"Construction ratio (Classic/Early): "
          f"{classic['rooms_per_decade']/early['rooms_per_decade']:.2f}")

    # Bootstrap test: is Classic Bonito variance significantly different?
    classic_mask = (pmdi['year'] >= 1020) & (pmdi['year'] < 1130)
    early_mask = (pmdi['year'] >= 850) & (pmdi['year'] < 1020)
    classic_pmdi = pmdi.loc[classic_mask, 'pmdi'].values
    early_pmdi = pmdi.loc[early_mask, 'pmdi'].values

    # Levene's test for equality of variances
    stat, p = stats.levene(classic_pmdi, early_pmdi)
    print(f"\nLevene's test (Classic vs Early variance): "
          f"F={stat:.3f}, p={p:.4f}")

    # F-test for variance ratio
    f_stat = classic_pmdi.var(ddof=1) / early_pmdi.var(ddof=1)
    df1 = len(classic_pmdi) - 1
    df2 = len(early_pmdi) - 1
    p_f = 1 - stats.f.cdf(f_stat, df1, df2)
    print(f"F-test (variance ratio): F={f_stat:.3f}, "
          f"df=({df1},{df2}), p={p_f:.4f} (one-sided)")

    # Save
    out_path = BASE / "data" / "processed" / "pmdi_period_statistics.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")

    # Create figure
    create_figure(df, pmdi)


def create_figure(df, pmdi):
    """Period-level comparison figure."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))

    colors = ['#56B4E9', '#009E73', '#D55E00', '#CC79A7']

    # Panel A: PMDI variance by period
    ax = axes[0]
    x = range(len(df))
    bars = ax.bar(x, df['pmdi_var'], color=colors, edgecolor='white',
                  linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels([p.split('(')[0].strip() for p in df['period']],
                        rotation=30, ha='right', fontsize=8,
                        fontfamily='sans-serif')
    ax.set_ylabel('PMDI variance', fontsize=10, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(a)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel B: Construction vs variance scatter
    ax = axes[1]
    for i, (_, row) in enumerate(df.iterrows()):
        ax.scatter(row['pmdi_var'], row['rooms_per_decade'],
                   color=colors[i], s=80, edgecolors='black',
                   linewidth=0.5, zorder=5)
        ax.annotate(row['period'].split('(')[0].strip(),
                    (row['pmdi_var'], row['rooms_per_decade']),
                    textcoords="offset points", xytext=(5, 5),
                    fontsize=7, fontfamily='sans-serif')

    ax.set_xlabel('PMDI variance', fontsize=10, fontfamily='sans-serif')
    ax.set_ylabel('Construction\n(rooms/decade)', fontsize=10,
                  fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(b)', transform=ax.transAxes, fontsize=11,
            fontweight='bold', va='top', fontfamily='sans-serif')

    plt.tight_layout()
    out = OUTPUT_DIR / "Figure_12_period_variance_construction.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {out}")
    plt.close()


if __name__ == '__main__':
    main()
