#!/usr/bin/env python3
"""
Create comprehensive validation figure comparing model predictions to archaeological data.

This figure shows:
1. Archaeological construction chronology vs PMDI
2. Model predictions for construction-climate correlation
3. Exotic goods chronology vs environmental stress
4. Population dynamics and system collapse
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from pathlib import Path
from scipy import stats


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def load_all_data():
    """Load all necessary datasets."""
    root = get_project_root()

    data = {}

    # PMDI data
    data['pmdi'] = pd.read_csv(root / 'data' / 'processed' / 'chaco_pmdi_averaged.csv')

    # Construction episodes
    data['construction'] = pd.read_csv(root / 'data' / 'raw' / 'construction_dates' / 'construction_episodes.csv')

    # Exotic goods chronology
    data['exotics'] = pd.read_csv(root / 'data' / 'raw' / 'exotic_goods_dates' / 'exotic_goods_chronology.csv')

    # Simulation results
    data['simulation'] = pd.read_csv(root / 'data' / 'processed' / 'simulation_history_baseline.csv')

    return data


def create_comprehensive_validation_figure(save_path=None):
    """Create comprehensive 6-panel validation figure."""

    data = load_all_data()

    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

    # Panel A: Archaeological Construction vs PMDI
    ax1 = fig.add_subplot(gs[0, 0])

    # Merge construction and PMDI
    merged = pd.merge(data['construction'], data['pmdi'], on='year', how='inner')

    # Dual axis plot
    ax1_twin = ax1.twinx()

    bars = ax1.bar(merged['year'], merged['timber_count'], color='#8B4513', alpha=0.7, width=5)
    line = ax1_twin.plot(merged['year'], merged['pmdi'], color='#2E86AB', linewidth=2)

    ax1_twin.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax1_twin.fill_between(merged['year'], merged['pmdi'], 0,
                          where=merged['pmdi'] < 0, color='red', alpha=0.1)

    ax1.set_xlabel('Year (CE)')
    ax1.set_ylabel('Timber Count', color='#8B4513')
    ax1_twin.set_ylabel('PMDI', color='#2E86AB')
    ax1.set_title('A. Archaeological Construction Record vs Climate')

    # Add key events
    ax1.axvline(x=1050, color='green', linestyle='--', alpha=0.5)
    ax1.axvline(x=1130, color='red', linestyle='--', alpha=0.5)

    # Panel B: Construction-Climate Scatter
    ax2 = fig.add_subplot(gs[0, 1])

    ax2.scatter(merged['pmdi'], merged['timber_count'], alpha=0.6, c='#8B4513', s=50, edgecolor='white')

    # Regression
    slope, intercept, r, p, se = stats.linregress(merged['pmdi'], merged['timber_count'])
    x_line = np.linspace(merged['pmdi'].min(), merged['pmdi'].max(), 100)
    ax2.plot(x_line, slope * x_line + intercept, 'r--', linewidth=2)

    ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    ax2.axvline(x=-1, color='red', linestyle='--', alpha=0.3, label='Drought threshold')

    ax2.set_xlabel('PMDI (negative = drought)')
    ax2.set_ylabel('Timber Count')
    ax2.set_title(f'B. Construction-Climate Correlation\n(r = {r:.3f}, p = {p:.4f})')

    # Add prediction box
    prediction_met = r < 0
    color = '#90EE90' if prediction_met else '#FFB6C1'
    ax2.text(0.05, 0.95, f'Prediction: Negative correlation\nResult: {"Supported" if prediction_met else "Not supported"}',
            transform=ax2.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor=color, alpha=0.8))

    # Panel C: Exotic Goods Over Time
    ax3 = fig.add_subplot(gs[1, 0])

    # Aggregate exotic goods by decade
    exotics_df = data['exotics'].copy()
    exotics_df['decade'] = (exotics_df['date_ce'] // 10) * 10

    # Convert count to numeric, ignoring non-numeric values
    exotics_df['count_numeric'] = pd.to_numeric(exotics_df['count'], errors='coerce').fillna(1)

    # Get numeric counts where available
    macaws = exotics_df[exotics_df['item_type'] == 'scarlet_macaw'].groupby('decade')['count_numeric'].sum()
    turquoise = exotics_df[exotics_df['item_type'] == 'turquoise'].groupby('decade')['count_numeric'].sum() / 1000  # Scale

    ax3.bar(macaws.index - 3, macaws.values, width=6, color='#FF6B6B', alpha=0.7, label='Macaws')
    ax3.bar(turquoise.index + 3, turquoise.values, width=6, color='#4ECDC4', alpha=0.7, label='Turquoise (÷1000)')

    # Get PMDI by decade
    pmdi_decade = data['pmdi'].copy()
    pmdi_decade['decade'] = (pmdi_decade['year'] // 10) * 10
    pmdi_mean = pmdi_decade.groupby('decade')['pmdi'].mean()

    ax3_twin = ax3.twinx()
    ax3_twin.plot(pmdi_mean.index, pmdi_mean.values, 'k--', linewidth=2, alpha=0.5, label='Mean PMDI')
    ax3_twin.axhline(y=0, color='gray', linestyle='-', alpha=0.3)

    ax3.set_xlabel('Decade (CE)')
    ax3.set_ylabel('Count')
    ax3_twin.set_ylabel('Mean PMDI')
    ax3.set_title('C. Exotic Goods Acquisition and Climate')
    ax3.legend(loc='upper left')
    ax3.set_xlim(850, 1150)

    # Panel D: Model Population Dynamics
    ax4 = fig.add_subplot(gs[1, 1])

    sim = data['simulation']
    ax4.plot(sim['year'], sim['total_population'], color='#2E86AB', linewidth=2, label='Population')
    ax4.fill_between(sim['year'], 0, sim['total_population'], color='#2E86AB', alpha=0.2)

    # Highlight periods
    ax4.axvspan(1000, 1130, alpha=0.1, color='green', label='Florescence')
    ax4.axvspan(1130, 1180, alpha=0.2, color='red', label='Collapse')

    # Mark peak
    peak_idx = sim['total_population'].idxmax()
    peak_year = sim.loc[peak_idx, 'year']
    peak_pop = sim.loc[peak_idx, 'total_population']
    ax4.annotate(f'Peak: {peak_pop:,.0f}\n({int(peak_year)} CE)',
                xy=(peak_year, peak_pop), xytext=(peak_year + 30, peak_pop * 0.8),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=9)

    ax4.set_xlabel('Year (CE)')
    ax4.set_ylabel('Population')
    ax4.set_title('D. Model Population Dynamics')
    ax4.legend(loc='upper left')

    # Panel E: Monument Investment and Drought
    ax5 = fig.add_subplot(gs[2, 0])

    # Monument change rate
    sim['monument_change'] = sim['total_monuments'].diff()
    sim['productivity_lag'] = sim['productivity'].shift(1)

    ax5.scatter(sim['productivity'], sim['monument_change'], alpha=0.5, c='#8B4513', s=20)

    # Regression
    valid = sim.dropna(subset=['productivity', 'monument_change'])
    if len(valid) > 10:
        slope, intercept, r, p, se = stats.linregress(valid['productivity'], valid['monument_change'])
        x_line = np.linspace(valid['productivity'].min(), valid['productivity'].max(), 100)
        ax5.plot(x_line, slope * x_line + intercept, 'r--', linewidth=2)

        ax5.set_title(f'E. Model: Monument Investment vs Productivity\n(r = {r:.3f}, p = {p:.4f})')

    ax5.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax5.set_xlabel('Environmental Productivity')
    ax5.set_ylabel('Monument Investment Change')

    # Panel F: Summary Statistics Table
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')

    # Create summary table
    summary_data = [
        ['Metric', 'Value', 'Interpretation'],
        ['Peak Population', f'{peak_pop:,.0f}', f'Year {int(peak_year)} CE'],
        ['Final Population', f'{sim["total_population"].iloc[-1]:,.0f}', 'System collapse'],
        ['Total Monuments', f'{sim["total_monuments"].iloc[-1]:,.0f}', 'Cumulative investment'],
        ['Drought Years', f'{sim["is_drought"].sum()}', f'{100*sim["is_drought"].mean():.1f}% of simulation'],
        ['Total Conflicts', f'{sim["total_conflicts"].iloc[-1]:,.0f}', 'Cumulative'],
        ['Constr-Climate r', f'{r:.3f}', 'Model prediction'],
    ]

    # Create table
    table = ax6.table(cellText=summary_data[1:],
                      colLabels=summary_data[0],
                      cellLoc='center',
                      loc='center',
                      colColours=['#E8E8E8'] * 3)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    ax6.set_title('F. Summary Statistics', fontsize=12, fontweight='bold', y=0.98)

    plt.suptitle('Chaco Canyon Costly Signaling Model: Validation Against Archaeological Record',
                fontsize=14, fontweight='bold', y=0.98)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def create_exotic_goods_detail_figure(save_path=None):
    """Create detailed exotic goods analysis figure."""

    root = get_project_root()
    exotics = pd.read_csv(root / 'data' / 'raw' / 'exotic_goods_dates' / 'exotic_goods_chronology.csv')
    pmdi = pd.read_csv(root / 'data' / 'processed' / 'chaco_pmdi_averaged.csv')

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel A: Macaw imports over time
    ax1 = axes[0, 0]
    macaws = exotics[exotics['item_type'] == 'scarlet_macaw'].copy()
    ax1.stem(macaws['date_ce'], macaws['count'], linefmt='C3-', markerfmt='C3o', basefmt='k-')
    ax1.set_xlabel('Year (CE)')
    ax1.set_ylabel('Macaw Count')
    ax1.set_title('A. Scarlet Macaw Imports (Watson et al. 2015)')

    # Add PMDI
    ax1_twin = ax1.twinx()
    pmdi_subset = pmdi[(pmdi['year'] >= 850) & (pmdi['year'] <= 1150)]
    ax1_twin.fill_between(pmdi_subset['year'], pmdi_subset['pmdi'], 0,
                          where=pmdi_subset['pmdi'] < 0, color='red', alpha=0.1)
    ax1_twin.plot(pmdi_subset['year'], pmdi_subset['pmdi'], 'b-', alpha=0.3)
    ax1_twin.set_ylabel('PMDI', color='blue')

    # Panel B: Turquoise accumulation
    ax2 = axes[0, 1]
    turquoise = exotics[exotics['item_type'] == 'turquoise'].copy()
    turquoise['count_numeric'] = pd.to_numeric(turquoise['count'], errors='coerce').fillna(1)
    ax2.bar(turquoise['date_ce'], turquoise['count_numeric'] / 1000, width=30, color='#4ECDC4', alpha=0.7)
    ax2.set_xlabel('Year (CE)')
    ax2.set_ylabel('Turquoise Count (×1000)')
    ax2.set_title('B. Turquoise Accumulation (Crown et al.)')

    # Panel C: All exotic goods by type
    ax3 = axes[1, 0]
    item_types = exotics['item_type'].unique()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

    # Convert count to numeric
    exotics['count_numeric'] = pd.to_numeric(exotics['count'], errors='coerce').fillna(1)

    # Use log scaling for marker sizes to handle large variation in counts
    # (turquoise has ~70,000 while macaws have ~1-10)
    for i, item in enumerate(item_types):
        subset = exotics[exotics['item_type'] == item]
        # Log scale: ensures visual differentiation without overwhelming
        sizes = np.log10(subset['count_numeric'].clip(lower=1) + 1) * 50
        ax3.scatter(subset['date_ce'], [item] * len(subset), s=sizes,
                   alpha=0.6, color=colors[i % len(colors)], label=item.replace('_', ' '))

    ax3.set_xlabel('Year (CE)')
    ax3.set_ylabel('Item Type')
    ax3.set_title('C. All Exotic Goods by Type and Date')
    ax3.legend(loc='upper left', fontsize=8)

    # Panel D: Exotic goods timing relative to major droughts
    ax4 = axes[1, 1]

    # Get severe droughts
    droughts = pmdi[pmdi['pmdi'] < -3.0][['year', 'pmdi']]

    # Get exotic goods dates
    all_dates = exotics['date_ce'].unique()

    ax4.scatter(droughts['year'], droughts['pmdi'], c='red', s=30, alpha=0.5, label='Severe drought')
    for date in all_dates:
        pmdi_val = pmdi[pmdi['year'] == int(date)]['pmdi'].values
        if len(pmdi_val) > 0:
            ax4.axvline(x=date, color='green', alpha=0.3, linestyle='--')

    ax4.set_xlabel('Year (CE)')
    ax4.set_ylabel('PMDI')
    ax4.set_title('D. Exotic Goods Timing vs Severe Droughts')
    ax4.axhline(y=-3, color='red', linestyle='--', alpha=0.5, label='Severe threshold')
    ax4.legend()
    ax4.set_xlim(850, 1150)

    plt.suptitle('Chaco Canyon Exotic Goods Chronology', fontsize=14, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def main():
    """Generate validation figures."""
    output_dir = get_project_root() / 'figures' / 'final'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Creating validation figures...")
    print("=" * 60)

    # Main validation figure
    create_comprehensive_validation_figure(output_dir / 'figure_6_validation_comprehensive.png')
    plt.close()

    # Exotic goods detail
    create_exotic_goods_detail_figure(output_dir / 'figure_7_exotic_goods_detail.png')
    plt.close()

    print("\n" + "=" * 60)
    print("Validation figures complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
