"""
Run the three-layer formal simulation and generate all output figures.

Implements the manuscript's equations:
  Layer 1: x*(q) = sqrt(lambda * (q^2 - q_min^2))
  Layer 2: sigma_eff = sigma_0 / sqrt(1 + kappa*(M_g + M_h))
  Layer 3: lambda(sigma) = lambda_0 + lambda_1 * sigma^alpha, S = exp(-sigma/(1+gamma*k))

Generates:
  - Simulation dynamics (population, monuments, sigma, lambda, conflicts)
  - Quality-investment Spence curve at final state
  - Core vs outlier comparison
  - Replicate analysis with confidence intervals
"""

import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.chaco.simulation import ChacoSimulation, SimulationConfig
from src.chaco.environment import Environment, EnvironmentConfig
from src.chaco.analysis import history_to_dataframe

BASE = Path(__file__).resolve().parents[1]
FIG_DIR = BASE / "figures" / "final"
DATA_DIR = BASE / "data" / "processed"

# Okabe-Ito palette
COLORS = {
    'blue': '#0072B2',
    'orange': '#D55E00',
    'green': '#009E73',
    'yellow': '#E69F00',
    'purple': '#CC79A7',
    'cyan': '#56B4E9',
    'gray': '#999999',
}


def run_replicates(n_replicates=20):
    """Run simulation with multiple replicates for confidence intervals."""
    all_dfs = []

    for rep in range(n_replicates):
        config = SimulationConfig(
            start_year=800,
            end_year=1200,
            seed=42 + rep,
        )
        env = Environment(EnvironmentConfig())
        sim = ChacoSimulation(config, env)
        history = sim.run(verbose=(rep == 0))
        df = history_to_dataframe(history)
        df['replicate'] = rep
        all_dfs.append(df)

        if rep == 0:
            # Save reference simulation for detailed analysis
            ref_sim = sim
            ref_history = history

    combined = pd.concat(all_dfs, ignore_index=True)
    return combined, ref_sim, ref_history


def create_simulation_dynamics_figure(combined, ref_df):
    """
    Create multi-panel figure showing simulation dynamics.
    Replaces old figure_8_simulation_dynamics.png.
    """
    fig = plt.figure(figsize=(7, 9))
    gs = GridSpec(4, 1, hspace=0.3, height_ratios=[1, 1, 1, 0.8])

    # Compute replicate statistics
    yearly = combined.groupby('year').agg(
        pop_mean=('total_population', 'mean'),
        pop_lo=('total_population', lambda x: np.percentile(x, 5)),
        pop_hi=('total_population', lambda x: np.percentile(x, 95)),
        mon_mean=('total_monuments', 'mean'),
        mon_lo=('total_monuments', lambda x: np.percentile(x, 5)),
        mon_hi=('total_monuments', lambda x: np.percentile(x, 95)),
        sigma_mean=('sigma', 'mean'),
        lambda_mean=('current_lambda', 'mean'),
        hq_mean=('pop_high_quality', 'mean'),
        lq_mean=('pop_low_quality', 'mean'),
        conflicts_mean=('total_conflicts', 'mean'),
    ).reset_index()

    years = yearly['year']

    for ax in []:
        pass  # placeholder

    # Panel A: Population dynamics
    ax0 = fig.add_subplot(gs[0])
    ax0.fill_between(years, yearly['pop_lo'], yearly['pop_hi'],
                     alpha=0.2, color=COLORS['blue'])
    ax0.plot(years, yearly['pop_mean'], color=COLORS['blue'],
             linewidth=1.5, label='Total population')
    ax0.plot(years, yearly['hq_mean'], color=COLORS['orange'],
             linewidth=1, linestyle='--', label='High-quality groups')
    ax0.plot(years, yearly['lq_mean'], color=COLORS['green'],
             linewidth=1, linestyle='--', label='Low-quality groups')
    ax0.set_ylabel('Population', fontsize=10, fontfamily='sans-serif')
    ax0.legend(fontsize=8, loc='upper left', frameon=False)
    ax0.text(0.02, 0.95, '(a)', transform=ax0.transAxes, fontsize=11,
             fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel B: Monument investment
    ax1 = fig.add_subplot(gs[1])
    ax1.fill_between(years, yearly['mon_lo'], yearly['mon_hi'],
                     alpha=0.2, color=COLORS['orange'])
    ax1.plot(years, yearly['mon_mean'], color=COLORS['orange'],
             linewidth=1.5, label='Total monument stock')
    ax1.set_ylabel('Monument investment', fontsize=10, fontfamily='sans-serif')
    ax1.legend(fontsize=8, loc='upper left', frameon=False)
    ax1.text(0.02, 0.95, '(b)', transform=ax1.transAxes, fontsize=11,
             fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel C: Lambda-sigma feedback
    ax2 = fig.add_subplot(gs[2])
    ax2.plot(years, yearly['sigma_mean'], color=COLORS['green'],
             linewidth=1.5, label='$\\sigma$ (uncertainty)')
    ax2_r = ax2.twinx()
    ax2_r.plot(years, yearly['lambda_mean'], color=COLORS['purple'],
               linewidth=1.5, linestyle='--', label='$\\lambda$ (signaling return)')
    ax2.set_ylabel('$\\sigma$', fontsize=10, fontfamily='sans-serif',
                   color=COLORS['green'])
    ax2_r.set_ylabel('$\\lambda$', fontsize=10, fontfamily='sans-serif',
                     color=COLORS['purple'])
    ax2.tick_params(axis='y', labelcolor=COLORS['green'])
    ax2_r.tick_params(axis='y', labelcolor=COLORS['purple'])
    # Combined legend
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_r.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=8,
               loc='upper left', frameon=False)
    ax2.text(0.02, 0.95, '(c)', transform=ax2.transAxes, fontsize=11,
             fontweight='bold', va='top', fontfamily='sans-serif')

    # Panel D: Conflict rate (cumulative per decade)
    ax3 = fig.add_subplot(gs[3])
    # Compute decadal conflict increments from the reference run
    ref_conflicts = ref_df['total_conflicts'].diff().fillna(0)
    decade_conflicts = ref_conflicts.groupby(ref_df['year'] // 10 * 10).sum()
    ax3.bar(decade_conflicts.index + 5, decade_conflicts.values,
            width=8, color=COLORS['gray'], alpha=0.7, edgecolor='white')
    ax3.set_ylabel('Conflicts/decade', fontsize=10, fontfamily='sans-serif')
    ax3.set_xlabel('Year (CE)', fontsize=10, fontfamily='sans-serif')
    ax3.text(0.02, 0.95, '(d)', transform=ax3.transAxes, fontsize=11,
             fontweight='bold', va='top', fontfamily='sans-serif')

    # Shade florescence and mark collapse
    for ax in [ax0, ax1, ax2, ax3]:
        ax.axvspan(1020, 1130, alpha=0.06, color='orange')
        ax.axvline(1130, color='red', linewidth=0.7, linestyle='--', alpha=0.4)

    ax3.set_xlim(800, 1200)

    out = FIG_DIR / "Figure_8_simulation_dynamics.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def create_quality_investment_figure(ref_sim):
    """
    Create quality vs investment scatter at final simulation state.
    Shows the Spence equilibrium realized in the simulation.
    """
    fig, ax = plt.subplots(figsize=(3.5, 3.5))

    qi = ref_sim.get_quality_investment_summary()
    stats = ref_sim.get_core_vs_outlier_stats()

    qs = [g['quality'] for g in qi]
    ms = [g['monument_investment'] for g in qi]
    pops = [g['population'] for g in qi]
    names = [g['name'] for g in qi]

    # Color by core vs outlier
    core_names = {h.name for h in ref_sim.spatial.get_core_houses()}
    colors = [COLORS['orange'] if n in core_names else COLORS['blue'] for n in names]
    sizes = [max(20, p * 0.5) for p in pops]

    ax.scatter(qs, ms, c=colors, s=sizes, alpha=0.7, edgecolors='white', linewidth=0.5)

    # Label key sites
    for g in qi:
        if g['name'] in ['Pueblo Bonito', 'Chetro Ketl', 'Pueblo Alto']:
            ax.annotate(g['name'], (g['quality'], g['monument_investment']),
                        fontsize=7, fontfamily='sans-serif',
                        xytext=(5, 5), textcoords='offset points')

    # Overlay theoretical curve
    q_range = np.linspace(0.1, 2.2, 100)
    lam = ref_sim._compute_lambda(ref_sim._compute_sigma(ref_sim.current_year - 1))
    x_star = np.sqrt(np.maximum(0, lam * (q_range**2 - 0.1**2)))
    ax.plot(q_range, x_star, color='black', linewidth=1, linestyle='--',
            alpha=0.5, label=f'$x^*(q)$, $\\lambda$={lam:.2f}')

    ax.set_xlabel('Quality ($q$)', fontsize=10, fontfamily='sans-serif')
    ax.set_ylabel('Monument stock ($M$)', fontsize=10, fontfamily='sans-serif')
    ax.legend(fontsize=8, frameon=False)

    out = FIG_DIR / "Figure_13_simulation_quality_investment.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def create_prediction_summary_figure():
    """
    Updated Figure 7: prediction evaluation with discriminability tags
    and honest P5 assessment.
    """
    fig, ax = plt.subplots(figsize=(7, 4))

    predictions = [
        ('P1: Quality-dependent\ninvestment', 'Supported\n(severity caveat)', 'C', COLORS['cyan']),
        ('P2: Elite exotic\ngoods', 'Supported', 'C', COLORS['cyan']),
        ('P3: Signal\nobservability', 'Supported', 'D', COLORS['green']),
        ('P4: Conflict\nreduction', 'Partially\nSupported', 'D', COLORS['yellow']),
        ('P5: Construction\nunder uncertainty', 'Not Supported\n(at tested res.)', 'D', COLORS['orange']),
        ('P6: Network-construction\nco-evolution', 'Supported', 'D', COLORS['green']),
        ('P7: Signal\ndepreciation', 'Supported', 'PD', COLORS['green']),
        ('P8: System\ncollapse', 'Partially\nSupported', 'D', COLORS['yellow']),
    ]

    status_colors = {
        'Supported': COLORS['green'],
        'Supported\n(severity caveat)': COLORS['cyan'],
        'Partially\nSupported': COLORS['yellow'],
        'Not Supported\n(at tested res.)': COLORS['orange'],
    }

    y_pos = np.arange(len(predictions))

    for i, (name, status, disc, color) in enumerate(predictions):
        bar_color = status_colors[status]
        bar_width = {'Supported': 0.9, 'Supported\n(severity caveat)': 0.7,
                     'Partially\nSupported': 0.5, 'Not Supported\n(at tested res.)': 0.2}[status]

        ax.barh(i, bar_width, height=0.6, color=bar_color, alpha=0.7,
                edgecolor='white', linewidth=0.5)

        # Discriminability tag
        disc_label = {'D': 'Discriminating', 'C': 'Convergent', 'PD': 'Partially disc.'}[disc]
        ax.text(bar_width + 0.03, i, f'{status}  [{disc_label}]',
                va='center', fontsize=8, fontfamily='sans-serif')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([p[0] for p in predictions], fontsize=8, fontfamily='sans-serif')
    ax.set_xlim(0, 1.6)
    ax.set_xlabel('Evidence strength', fontsize=10, fontfamily='sans-serif')
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks([])

    out = FIG_DIR / "Figure_7_prediction_summary.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def create_figure1_pmdi(ref_history):
    """
    Updated Figure 1: PMDI timeseries with construction overlay.
    Uses PMDI label (not PDSI).
    """
    fig, ax = plt.subplots(figsize=(7, 3))

    # Load PMDI data
    pmdi_file = DATA_DIR / "chaco_pmdi_simulation_input.csv"
    pmdi = pd.read_csv(pmdi_file)
    pmdi = pmdi[(pmdi['year'] >= 800) & (pmdi['year'] <= 1200)]

    # PMDI fill
    ax.fill_between(pmdi['year'], pmdi['pmdi'], 0,
                    where=pmdi['pmdi'] < 0, color=COLORS['blue'], alpha=0.3)
    ax.fill_between(pmdi['year'], pmdi['pmdi'], 0,
                    where=pmdi['pmdi'] >= 0, color=COLORS['cyan'], alpha=0.3)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylabel('PMDI', fontsize=10, fontfamily='sans-serif')

    # Construction overlay (from great house chronology)
    chrono_file = BASE / "data" / "raw" / "construction_dates" / "great_house_chronology.csv"
    chrono = pd.read_csv(chrono_file)

    # Count active construction projects per year
    years = np.arange(800, 1201)
    activity = np.zeros(len(years))
    for _, row in chrono.iterrows():
        start = int(row['major_construction_start'])
        end = int(row['major_construction_end'])
        for i, y in enumerate(years):
            if start <= y <= end:
                activity[i] += 1

    ax2 = ax.twinx()
    ax2.fill_between(years, activity, alpha=0.3, color=COLORS['orange'])
    ax2.plot(years, activity, color=COLORS['orange'], linewidth=1, alpha=0.7)
    ax2.set_ylabel('Active construction\nprojects', fontsize=10,
                   fontfamily='sans-serif', color=COLORS['orange'])
    ax2.tick_params(axis='y', labelcolor=COLORS['orange'])

    # Key transitions
    ax.axvline(1020, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(1130, color='red', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.text(1022, ax.get_ylim()[1] * 0.9, 'Classic Bonito', fontsize=7,
            fontfamily='sans-serif', alpha=0.7)
    ax.text(1132, ax.get_ylim()[1] * 0.9, 'Megadrought', fontsize=7,
            fontfamily='sans-serif', alpha=0.7, color='red')

    ax.set_xlabel('Year (CE)', fontsize=10, fontfamily='sans-serif')
    ax.set_xlim(800, 1200)

    out = FIG_DIR / "Figure_1_PMDI_construction.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def save_simulation_data(combined, ref_sim):
    """Save simulation output for reproducibility."""
    # Save replicate summary
    yearly = combined.groupby('year').agg(
        pop_mean=('total_population', 'mean'),
        pop_std=('total_population', 'std'),
        mon_mean=('total_monuments', 'mean'),
        mon_std=('total_monuments', 'std'),
        sigma_mean=('sigma', 'mean'),
        lambda_mean=('current_lambda', 'mean'),
    ).reset_index()
    yearly.to_csv(DATA_DIR / "simulation_replicate_summary.csv", index=False)
    print(f"Saved: {DATA_DIR / 'simulation_replicate_summary.csv'}")

    # Save final quality-investment summary
    qi = ref_sim.get_quality_investment_summary()
    qi_df = pd.DataFrame(qi)
    qi_df.to_csv(DATA_DIR / "simulation_quality_investment.csv", index=False)
    print(f"Saved: {DATA_DIR / 'simulation_quality_investment.csv'}")


if __name__ == '__main__':
    print("=" * 70)
    print("Running Chaco formal simulation (20 replicates)")
    print("=" * 70)

    combined, ref_sim, ref_history = run_replicates(n_replicates=20)
    ref_df = history_to_dataframe(ref_history)

    print("\n--- Generating figures ---")
    create_simulation_dynamics_figure(combined, ref_df)
    create_quality_investment_figure(ref_sim)
    create_prediction_summary_figure()
    create_figure1_pmdi(ref_history)

    print("\n--- Saving data ---")
    save_simulation_data(combined, ref_sim)

    # Print summary statistics
    print("\n" + "=" * 70)
    print("SIMULATION SUMMARY (Reference run)")
    print("=" * 70)
    stats = ref_sim.get_core_vs_outlier_stats()
    final = ref_history[-1]
    peak_pop = max(s.total_population for s in ref_history)
    peak_year = next(s.year for s in ref_history if s.total_population == peak_pop)
    peak_mon = max(s.total_monument_investment for s in ref_history)
    peak_mon_year = next(s.year for s in ref_history
                         if s.total_monument_investment == peak_mon)

    print(f"Peak population: {peak_pop} (year {peak_year})")
    print(f"Peak monuments: {peak_mon:.0f} (year {peak_mon_year})")
    print(f"Final population: {final.total_population} (year {final.year})")
    print(f"Final sigma: {final.sigma:.3f}, lambda: {final.current_lambda:.3f}")
    print(f"\nCore houses: avg_q={stats['core']['avg_quality']:.2f}, "
          f"monuments={stats['core']['total_monuments']:.0f}, "
          f"partners={stats['core']['avg_partners']:.1f}")
    print(f"Outliers:    avg_q={stats['outlier']['avg_quality']:.2f}, "
          f"monuments={stats['outlier']['total_monuments']:.0f}, "
          f"partners={stats['outlier']['avg_partners']:.1f}")

    # Spence gradient check
    qi = ref_sim.get_quality_investment_summary()
    print(f"\nSpence gradient (quality -> investment):")
    for g in qi[:3]:
        print(f"  {g['name']}: q={g['quality']:.2f}, M={g['monument_investment']:.1f}")
    print("  ...")
    for g in qi[-3:]:
        print(f"  {g['name']}: q={g['quality']:.2f}, M={g['monument_investment']:.1f}")

    print("\nDone.")
