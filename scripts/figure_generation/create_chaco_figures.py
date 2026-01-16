#!/usr/bin/env python3
"""
Create publication-quality figures for Chaco Canyon costly signaling simulation.

Figures include:
1. Real PMDI timeseries with archaeological periods
2. Construction-climate correlation
3. Simulation dynamics overview (multi-panel)
4. Population and monument trajectories
5. Strategy comparison
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from pathlib import Path
from typing import Optional

# Set publication-quality defaults
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def load_pmdi_data() -> pd.DataFrame:
    """Load processed PMDI data."""
    data_path = get_project_root() / 'data' / 'processed' / 'chaco_pmdi_averaged.csv'
    return pd.read_csv(data_path)


def load_simulation_history() -> pd.DataFrame:
    """Load simulation results."""
    data_path = get_project_root() / 'data' / 'processed' / 'simulation_history_baseline.csv'
    return pd.read_csv(data_path)


def load_construction_data() -> pd.DataFrame:
    """Load construction episode data."""
    data_path = get_project_root() / 'data' / 'raw' / 'construction_dates' / 'construction_episodes.csv'
    return pd.read_csv(data_path)


def create_pmdi_timeseries_figure(save_path: Optional[Path] = None):
    """
    Create PMDI timeseries figure with archaeological periods highlighted.

    Shows real LBDA PMDI data for Chaco Canyon region with key periods marked.
    """
    pmdi_df = load_pmdi_data()

    # Filter to Chaco period
    pmdi_chaco = pmdi_df[(pmdi_df['year'] >= 700) & (pmdi_df['year'] <= 1300)]

    fig, ax = plt.subplots(figsize=(12, 4))

    # Plot PMDI timeseries
    ax.fill_between(pmdi_chaco['year'], pmdi_chaco['pmdi'], 0,
                    where=pmdi_chaco['pmdi'] > 0, color='#2E86AB', alpha=0.6, label='Wet')
    ax.fill_between(pmdi_chaco['year'], pmdi_chaco['pmdi'], 0,
                    where=pmdi_chaco['pmdi'] <= 0, color='#D62839', alpha=0.6, label='Dry')

    # Add drought threshold line
    ax.axhline(y=-1.0, color='#8B0000', linestyle='--', linewidth=1, alpha=0.7, label='Drought threshold')

    # Highlight archaeological periods
    periods = [
        (850, 920, 'Early Chaco', '#90EE90', 0.2),
        (920, 1000, 'Chaco Expansion', '#98FB98', 0.25),
        (1000, 1130, 'Chaco Florescence', '#00FF00', 0.15),
        (1130, 1180, 'Megadrought/Collapse', '#FFD700', 0.3),
    ]

    for start, end, label, color, alpha in periods:
        ax.axvspan(start, end, alpha=alpha, color=color, label=label)

    # Key dates
    ax.axvline(x=1050, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(x=1130, color='red', linestyle=':', alpha=0.5)
    ax.axvline(x=1150, color='red', linestyle=':', alpha=0.5)

    ax.set_xlabel('Year (CE)')
    ax.set_ylabel('Palmer Modified Drought Index (PMDI)')
    ax.set_title('Chaco Canyon Region Paleoclimate: LBDA Version 2 PMDI Reconstruction (36.25°N, 108.25°W)')

    # Add annotations
    ax.annotate('Peak Construction\n(~1050 CE)', xy=(1050, 5), ha='center', fontsize=8)
    ax.annotate('Megadrought\n(1130-1150 CE)', xy=(1140, -5.5), ha='center', fontsize=8, color='red')

    ax.set_xlim(700, 1300)
    ax.set_ylim(-7, 10)

    # Custom legend
    handles = [
        mpatches.Patch(color='#2E86AB', alpha=0.6, label='Wet periods (PMDI > 0)'),
        mpatches.Patch(color='#D62839', alpha=0.6, label='Dry periods (PMDI < 0)'),
        plt.Line2D([0], [0], color='#8B0000', linestyle='--', label='Drought threshold'),
        mpatches.Patch(color='#00FF00', alpha=0.15, label='Chaco Florescence'),
        mpatches.Patch(color='#FFD700', alpha=0.3, label='Megadrought/Collapse'),
    ]
    ax.legend(handles=handles, loc='upper left', ncol=2, fontsize=8)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")

    return fig


def create_construction_climate_correlation_figure(save_path: Optional[Path] = None):
    """
    Create figure showing construction activity vs climate (PMDI).

    Tests prediction: Construction should correlate with drought, not surplus.
    """
    pmdi_df = load_pmdi_data()
    constr_df = load_construction_data()

    # Merge datasets
    merged = pd.merge(constr_df, pmdi_df, on='year', how='inner')

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: Time series comparison
    ax1 = axes[0]
    ax1_twin = ax1.twinx()

    ax1.bar(merged['year'], merged['timber_count'], color='#8B4513', alpha=0.7, label='Timber counts')
    ax1_twin.plot(merged['year'], merged['pmdi'], color='#2E86AB', linewidth=2, label='PMDI')
    ax1_twin.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax1_twin.axhline(y=-1, color='red', linestyle='--', alpha=0.5)

    ax1.set_xlabel('Year (CE)')
    ax1.set_ylabel('Timber Count (Construction Proxy)', color='#8B4513')
    ax1_twin.set_ylabel('PMDI', color='#2E86AB')
    ax1.set_title('A. Construction Activity and Climate Over Time')
    ax1.tick_params(axis='y', labelcolor='#8B4513')
    ax1_twin.tick_params(axis='y', labelcolor='#2E86AB')

    # Panel B: Scatter with correlation
    ax2 = axes[1]

    ax2.scatter(merged['pmdi'], merged['timber_count'], alpha=0.6, c='#8B4513', s=40)

    # Add regression line
    z = np.polyfit(merged['pmdi'], merged['timber_count'], 1)
    p = np.poly1d(z)
    pmdi_range = np.linspace(merged['pmdi'].min(), merged['pmdi'].max(), 100)
    ax2.plot(pmdi_range, p(pmdi_range), "r--", alpha=0.8, linewidth=2)

    # Calculate correlation
    from scipy import stats
    r, pval = stats.pearsonr(merged['pmdi'], merged['timber_count'])

    ax2.set_xlabel('PMDI (negative = drought)')
    ax2.set_ylabel('Timber Count (Construction Proxy)')
    ax2.set_title(f'B. Construction vs Climate Correlation (r = {r:.3f}, p = {pval:.4f})')

    # Add reference lines
    ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    ax2.axvline(x=-1, color='red', linestyle='--', alpha=0.5)

    # Annotation
    if r < 0:
        ax2.annotate('Prediction: More construction\nduring drought (negative r)',
                    xy=(0.05, 0.95), xycoords='axes fraction', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                    verticalalignment='top')
    else:
        ax2.annotate('Result: No negative correlation\n(doesn\'t support prediction)',
                    xy=(0.05, 0.95), xycoords='axes fraction', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5),
                    verticalalignment='top')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")

    return fig


def create_simulation_dynamics_figure(save_path: Optional[Path] = None):
    """
    Create multi-panel figure showing simulation dynamics.

    Panels:
    A. Population trajectory
    B. Monument investment over time
    C. Environmental productivity (from PMDI)
    D. Strategy comparison by population
    """
    sim_df = load_simulation_history()
    pmdi_df = load_pmdi_data()

    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Panel A: Population trajectory
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(sim_df['year'], sim_df['total_population'], color='#2E86AB', linewidth=2)
    ax1.fill_between(sim_df['year'], 0, sim_df['total_population'], alpha=0.3, color='#2E86AB')

    # Mark peak
    peak_idx = sim_df['total_population'].idxmax()
    peak_year = sim_df.loc[peak_idx, 'year']
    peak_pop = sim_df.loc[peak_idx, 'total_population']
    ax1.axvline(x=peak_year, color='green', linestyle='--', alpha=0.5)
    ax1.annotate(f'Peak: {peak_pop:,.0f}\n({int(peak_year)} CE)',
                xy=(peak_year, peak_pop), xytext=(peak_year + 20, peak_pop * 0.8),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='green'))

    ax1.set_xlabel('Year (CE)')
    ax1.set_ylabel('Total Population')
    ax1.set_title('A. Population Dynamics')
    ax1.axvspan(1130, 1180, alpha=0.2, color='red', label='Megadrought')
    ax1.legend(loc='upper left')

    # Panel B: Monument investment
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(sim_df['year'], sim_df['total_monuments'], color='#8B4513', linewidth=2)
    ax2.fill_between(sim_df['year'], 0, sim_df['total_monuments'], alpha=0.3, color='#8B4513')

    ax2.set_xlabel('Year (CE)')
    ax2.set_ylabel('Cumulative Monument Investment')
    ax2.set_title('B. Monument Construction')
    ax2.axvspan(1130, 1180, alpha=0.2, color='red')

    # Panel C: Environmental productivity
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(sim_df['year'], sim_df['productivity'], color='#228B22', linewidth=1.5, alpha=0.8)

    # Add drought indicator
    drought_years = sim_df[sim_df['is_drought'] == True]['year'].values
    for y in drought_years:
        ax3.axvline(x=y, color='red', alpha=0.1, linewidth=2)

    ax3.set_xlabel('Year (CE)')
    ax3.set_ylabel('Environmental Productivity')
    ax3.set_title('C. Environmental Conditions (from Real PMDI)')
    ax3.axhline(y=0.7, color='gray', linestyle='--', alpha=0.5, label='Baseline')
    ax3.axvspan(1130, 1180, alpha=0.2, color='red', label='Megadrought')
    ax3.legend(loc='upper right')

    # Panel D: Strategy populations
    ax4 = fig.add_subplot(gs[1, 1])

    # Get strategy population columns
    strategy_cols = [col for col in sim_df.columns if col.startswith('pop_')]

    if strategy_cols:
        colors = {'pop_monument_builder': '#FF6B6B', 'pop_balanced': '#4ECDC4', 'pop_reproduction': '#9B59B6'}
        labels = {'pop_monument_builder': 'Monument Builder', 'pop_balanced': 'Balanced', 'pop_reproduction': 'Reproduction'}

        for col in strategy_cols:
            color = colors.get(col, 'gray')
            label = labels.get(col, col)
            ax4.plot(sim_df['year'], sim_df[col], label=label, linewidth=2, color=color)

        ax4.set_xlabel('Year (CE)')
        ax4.set_ylabel('Population by Strategy')
        ax4.set_title('D. Strategy Competition')
        ax4.legend(loc='upper left')
        ax4.axvspan(1130, 1180, alpha=0.2, color='red')

    plt.suptitle('Chaco Canyon Costly Signaling Simulation: Model Dynamics', fontsize=14, y=1.02)

    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")

    return fig


def create_period_comparison_figure(save_path: Optional[Path] = None):
    """
    Create figure comparing archaeological periods.

    Shows mean PMDI, drought frequency, and sigma for each period.
    """
    import json

    # Load period analysis
    period_path = get_project_root() / 'data' / 'processed' / 'chaco_period_analysis.json'
    with open(period_path) as f:
        periods = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # Prepare data
    period_names = list(periods.keys())
    period_labels = [name.replace('_', ' ') for name in period_names]
    mean_pmdi = [periods[p]['mean_pmdi'] for p in period_names]
    drought_freq = [periods[p]['n_drought_years'] / periods[p]['n_years'] for p in period_names]

    # Calculate sigma from processed data (load from file)
    sigma_path = get_project_root() / 'data' / 'processed' / 'chaco_sigma_timeseries.csv'
    sigma_df = pd.read_csv(sigma_path)

    sigmas = []
    for name, data in periods.items():
        period_sigma = sigma_df[(sigma_df['year'] >= data['start_year']) &
                                (sigma_df['year'] < data['end_year'])]['sigma'].mean()
        sigmas.append(period_sigma if not np.isnan(period_sigma) else 0)

    # Colors
    colors = ['#A5D6A7', '#81C784', '#66BB6A', '#4CAF50', '#F44336', '#E57373']

    # Panel A: Mean PMDI
    bars1 = axes[0].bar(period_labels, mean_pmdi, color=colors)
    axes[0].axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    axes[0].set_ylabel('Mean PMDI')
    axes[0].set_title('A. Average Climate Conditions')
    axes[0].tick_params(axis='x', rotation=45)
    for bar, val in zip(bars1, mean_pmdi):
        if val < 0:
            bar.set_color('#F44336')

    # Panel B: Drought Frequency
    bars2 = axes[1].bar(period_labels, [f * 100 for f in drought_freq], color=colors)
    axes[1].set_ylabel('Drought Years (%)')
    axes[1].set_title('B. Drought Frequency')
    axes[1].tick_params(axis='x', rotation=45)
    for bar, val in zip(bars2, drought_freq):
        if val > 0.35:
            bar.set_color('#F44336')

    # Panel C: Environmental Uncertainty (Sigma)
    bars3 = axes[2].bar(period_labels, sigmas, color=colors)
    axes[2].set_ylabel('Environmental Uncertainty (σ)')
    axes[2].set_title('C. Environmental Uncertainty')
    axes[2].tick_params(axis='x', rotation=45)

    plt.suptitle('Chaco Canyon: Environmental Conditions by Archaeological Period', fontsize=14)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")

    return fig


def create_drought_events_figure(save_path: Optional[Path] = None):
    """
    Create figure showing major drought events.

    Highlights the mid-12th century megadrought.
    """
    # Load drought events
    drought_path = get_project_root() / 'data' / 'processed' / 'chaco_drought_events.csv'
    drought_df = pd.read_csv(drought_path)

    # Filter to Chaco period and multi-year events
    chaco_droughts = drought_df[
        (drought_df['start_year'] >= 800) &
        (drought_df['end_year'] <= 1200) &
        (drought_df['duration'] >= 2)
    ].copy()

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot each drought as a horizontal bar
    for i, (_, drought) in enumerate(chaco_droughts.iterrows()):
        color = '#8B0000' if drought['min_pmdi'] < -4 else '#D62839' if drought['min_pmdi'] < -3 else '#FF6B6B'
        ax.barh(i, drought['duration'],
               left=drought['start_year'],
               height=0.7,
               color=color,
               alpha=0.8)

        # Add severity label
        if drought['duration'] >= 3:
            ax.annotate(f"PMDI: {drought['min_pmdi']:.1f}",
                       xy=(drought['start_year'] + drought['duration'] / 2, i),
                       ha='center', va='center', fontsize=7, color='white')

    # Highlight key periods
    ax.axvspan(1000, 1130, alpha=0.1, color='green', label='Chaco Florescence')
    ax.axvspan(1130, 1180, alpha=0.1, color='red', label='Megadrought Period')

    ax.set_xlabel('Year (CE)')
    ax.set_ylabel('Drought Event')
    ax.set_title('Major Drought Events in Chaco Canyon Region (800-1200 CE)')
    ax.set_xlim(800, 1200)

    # Create custom legend
    handles = [
        mpatches.Patch(color='#8B0000', alpha=0.8, label='Extreme (PMDI < -4)'),
        mpatches.Patch(color='#D62839', alpha=0.8, label='Severe (PMDI < -3)'),
        mpatches.Patch(color='#FF6B6B', alpha=0.8, label='Moderate (PMDI < -1)'),
        mpatches.Patch(color='green', alpha=0.1, label='Chaco Florescence'),
        mpatches.Patch(color='red', alpha=0.1, label='Megadrought Period'),
    ]
    ax.legend(handles=handles, loc='upper left')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")

    return fig


def create_all_figures():
    """Generate all figures and save to figures/final directory."""
    output_dir = get_project_root() / 'figures' / 'final'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Creating Chaco Canyon simulation figures...")
    print("=" * 60)

    # Create each figure
    figures = [
        ('figure_1_pmdi_timeseries.png', create_pmdi_timeseries_figure),
        ('figure_2_construction_correlation.png', create_construction_climate_correlation_figure),
        ('figure_3_simulation_dynamics.png', create_simulation_dynamics_figure),
        ('figure_4_period_comparison.png', create_period_comparison_figure),
        ('figure_5_drought_events.png', create_drought_events_figure),
    ]

    for filename, create_func in figures:
        try:
            save_path = output_dir / filename
            create_func(save_path)
            plt.close()
        except Exception as e:
            print(f"Error creating {filename}: {e}")

    print("\n" + "=" * 60)
    print(f"All figures saved to: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    create_all_figures()
