#!/usr/bin/env python3
"""
Create theoretical predictions figure for Chaco Canyon paper.

This figure shows:
1. The dual signaling channel framework
2. Environmental uncertainty parameter (σ) and thresholds
3. Expected correlations and relationships
4. Chaco periods positioned on phase space
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
from matplotlib.gridspec import GridSpec
from pathlib import Path
import matplotlib.patches as mpatches


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def create_theoretical_framework_figure(save_path=None):
    """Create comprehensive theoretical framework figure."""

    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

    # ===========================================
    # Panel A: Dual Signaling Framework Diagram
    # ===========================================
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')

    # Title
    ax1.text(5, 9.5, 'A. Dual Signaling Framework', fontsize=12, fontweight='bold',
             ha='center', va='top')

    # Environmental uncertainty box at top
    env_box = FancyBboxPatch((3, 7.5), 4, 1.2, boxstyle="round,pad=0.05",
                              facecolor='#FFE4B5', edgecolor='black', linewidth=2)
    ax1.add_patch(env_box)
    ax1.text(5, 8.1, 'Environmental\nUncertainty (σ)', fontsize=10, ha='center', va='center')

    # Left branch: Group-level signaling
    ax1.annotate('', xy=(3.5, 5.5), xytext=(4, 7.5),
                arrowprops=dict(arrowstyle='->', color='#8B4513', lw=2))

    group_box = FancyBboxPatch((1.5, 4.3), 4, 1.2, boxstyle="round,pad=0.05",
                                facecolor='#DEB887', edgecolor='#8B4513', linewidth=2)
    ax1.add_patch(group_box)
    ax1.text(3.5, 4.9, 'GROUP SIGNALING\n(Monuments/Great Houses)', fontsize=9, ha='center', va='center')

    # Right branch: Individual-level signaling
    ax1.annotate('', xy=(6.5, 5.5), xytext=(6, 7.5),
                arrowprops=dict(arrowstyle='->', color='#4169E1', lw=2))

    ind_box = FancyBboxPatch((4.5, 4.3), 4, 1.2, boxstyle="round,pad=0.05",
                              facecolor='#87CEEB', edgecolor='#4169E1', linewidth=2)
    ax1.add_patch(ind_box)
    ax1.text(6.5, 4.9, 'INDIVIDUAL SIGNALING\n(Exotic Goods)', fontsize=9, ha='center', va='center')

    # Arrows to outcomes
    ax1.annotate('', xy=(3.5, 2.8), xytext=(3.5, 4.3),
                arrowprops=dict(arrowstyle='->', color='#8B4513', lw=2))
    ax1.annotate('', xy=(6.5, 2.8), xytext=(6.5, 4.3),
                arrowprops=dict(arrowstyle='->', color='#4169E1', lw=2))

    # Outcome boxes
    out1 = FancyBboxPatch((1.5, 1.8), 4, 1, boxstyle="round,pad=0.05",
                           facecolor='#90EE90', edgecolor='green', linewidth=2)
    ax1.add_patch(out1)
    ax1.text(3.5, 2.3, '↓ Inter-group Conflict\n("Pax Chaco")', fontsize=9, ha='center', va='center')

    out2 = FancyBboxPatch((4.5, 1.8), 4, 1, boxstyle="round,pad=0.05",
                           facecolor='#90EE90', edgecolor='green', linewidth=2)
    ax1.add_patch(out2)
    ax1.text(6.5, 2.3, '↑ Elite Status\n(Ritual Authority)', fontsize=9, ha='center', va='center')

    # Interaction arrow between the two channels
    ax1.annotate('', xy=(5.7, 4.9), xytext=(4.3, 4.9),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5, linestyle='--'))
    ax1.text(5, 5.7, 'Interaction', fontsize=8, ha='center', color='purple', style='italic')

    # Cost annotations
    ax1.text(2.0, 3.6, 'Cost: ~35%\nproductivity', fontsize=7, ha='center', style='italic', color='#8B4513')
    ax1.text(8.0, 3.6, 'Cost: Long-\ndistance risk', fontsize=7, ha='center', style='italic', color='#4169E1')

    # ===========================================
    # Panel B: Environmental σ Parameter
    # ===========================================
    ax2 = fig.add_subplot(gs[0, 1])

    # Create sigma phase space
    frequency = np.linspace(0.5, 3, 100)  # drought frequency (higher = more frequent)
    magnitude = np.linspace(0.1, 0.9, 100)  # drought magnitude

    F, M = np.meshgrid(frequency, magnitude)
    # σ = (magnitude * duration) / frequency
    # Simplified: duration correlates with magnitude
    duration = 1 + M * 2.5
    sigma = (M * duration) / (4 / F)  # frequency as return period inverted

    # Plot contours
    levels = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    cs = ax2.contourf(F, M, sigma, levels=levels, cmap='YlOrRd', alpha=0.7, extend='both')
    ax2.contour(F, M, sigma, levels=levels, colors='gray', linewidths=0.5)

    # Add colorbar
    cbar = plt.colorbar(cs, ax=ax2, label='σ (uncertainty parameter)')

    # Mark critical threshold
    ax2.contour(F, M, sigma, levels=[0.15], colors='red', linewidths=2, linestyles='--')
    ax2.text(2.5, 0.3, 'σ* threshold', fontsize=9, color='red', fontweight='bold')

    # Mark Chaco periods
    # Pre-Chaco: lower uncertainty
    ax2.plot(1.5, 0.4, 'o', markersize=12, color='blue', markeredgecolor='white', markeredgewidth=2)
    ax2.text(1.6, 0.35, 'Pre-Chaco\n(800-900)', fontsize=8, color='blue')

    # Chaco florescence: higher uncertainty
    ax2.plot(2.2, 0.6, 's', markersize=12, color='green', markeredgecolor='white', markeredgewidth=2)
    ax2.text(2.3, 0.55, 'Florescence\n(1000-1130)', fontsize=8, color='green')

    # Megadrought: extreme
    ax2.plot(2.8, 0.8, '^', markersize=12, color='red', markeredgecolor='white', markeredgewidth=2)
    ax2.text(2.5, 0.85, 'Megadrought\n(1130-1150)', fontsize=8, color='red')

    ax2.set_xlabel('Drought Frequency (relative)', fontsize=10)
    ax2.set_ylabel('Drought Magnitude', fontsize=10)
    ax2.set_title('B. Environmental Uncertainty Parameter (σ)', fontsize=12, fontweight='bold')

    # ===========================================
    # Panel C: Expected Correlations
    # ===========================================
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')

    ax3.text(5, 9.5, 'C. Theoretical Predictions', fontsize=12, fontweight='bold',
             ha='center', va='top')

    # List of predictions with expected direction
    predictions = [
        ('P1', 'Construction × Climate', 'NEGATIVE', 'More building during drought',
         '#FF6B6B'),
        ('P2', 'Exotic Goods × Stress', 'POSITIVE', 'More acquisition during stress',
         '#4ECDC4'),
        ('P3', 'Violence during Signaling', 'LOW', 'Reduced conflict when active',
         '#90EE90'),
        ('P4', 'Violence post-Collapse', 'HIGH', 'Increased after abandonment',
         '#FFB6C1'),
    ]

    y_start = 8
    for i, (code, pred, direction, explanation, color) in enumerate(predictions):
        y = y_start - i * 1.8

        # Prediction box
        box = FancyBboxPatch((0.5, y - 0.6), 9, 1.2, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', alpha=0.7)
        ax3.add_patch(box)

        # Text
        ax3.text(1, y, f'{code}:', fontsize=10, fontweight='bold', va='center')
        ax3.text(2, y, pred, fontsize=10, va='center')
        ax3.text(6.5, y, f'→ {direction}', fontsize=10, fontweight='bold', va='center')
        ax3.text(5, y - 0.35, explanation, fontsize=8, style='italic', va='center', ha='center')

    # Add note about testability
    ax3.text(5, 0.5, 'All predictions testable with archaeological data',
             fontsize=9, style='italic', ha='center', color='gray')

    # ===========================================
    # Panel D: Sigma Formula and Chaco Values
    # ===========================================
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.axis('off')

    ax4.text(5, 9.5, 'D. Environmental Uncertainty at Chaco', fontsize=12, fontweight='bold',
             ha='center', va='top')

    # Formula
    ax4.text(5, 8.2, r'$\sigma = \frac{magnitude \times duration}{frequency}$',
             fontsize=14, ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='#F0F0F0', edgecolor='gray'))

    # Explain components
    ax4.text(1, 6.8, '• Magnitude: Productivity reduction (0-1)', fontsize=9)
    ax4.text(1, 6.2, '• Duration: Years shortfall persists', fontsize=9)
    ax4.text(1, 5.6, '• Frequency: Return period (years)', fontsize=9)

    # Chaco-specific values
    ax4.text(5, 4.5, 'Calculated from PMDI Data (LBDA v2)', fontsize=10, fontweight='bold', ha='center')

    periods = [
        ('Pre-Chaco (800-900)', 'σ = 0.135', 'Below threshold', '#87CEEB'),
        ('Early Chaco (900-1000)', 'σ = 0.142', 'Near threshold', '#98FB98'),
        ('Florescence (1000-1130)', 'σ = 0.168', 'Above threshold', '#FFD700'),
        ('Megadrought (1130-1150)', 'σ = 0.195', 'Extreme', '#FF6347'),
    ]

    y = 3.5
    for period, sigma_val, status, color in periods:
        box = FancyBboxPatch((1, y - 0.35), 8, 0.7, boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor='black', alpha=0.6)
        ax4.add_patch(box)
        ax4.text(1.3, y, period, fontsize=9, va='center')
        ax4.text(6, y, sigma_val, fontsize=9, va='center', fontweight='bold')
        ax4.text(8.2, y, status, fontsize=8, va='center', style='italic')
        y -= 0.85

    # Critical threshold note
    ax4.text(5, 0.5, 'Critical threshold σ* ≈ 0.15: signaling becomes adaptive',
             fontsize=9, ha='center', color='red', fontweight='bold')

    plt.suptitle('Chaco Canyon Costly Signaling: Theoretical Framework and Predictions',
                fontsize=14, fontweight='bold', y=0.98)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")

    return fig


def create_replicate_validation_figure(save_path=None):
    """Create figure showing simulation results with confidence intervals."""
    import json

    root = get_project_root()

    # Load replicate analysis results
    with open(root / 'data' / 'processed' / 'replicate_analysis_summary.json', 'r') as f:
        results = json.load(f)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # ===========================================
    # Panel A: Population by Scenario
    # ===========================================
    ax1 = axes[0, 0]

    scenarios = ['baseline', 'megadrought', 'no_signaling']
    scenario_labels = ['Baseline', 'Megadrought', 'No Signaling']
    colors = ['#2E86AB', '#A23B72', '#F18F01']

    x = np.arange(len(scenarios))
    width = 0.35

    # Final population
    final_means = [results[s]['final_population']['mean'] for s in scenarios]
    final_stds = [results[s]['final_population']['std'] for s in scenarios]

    # Peak population
    peak_means = [results[s]['peak_population']['mean'] for s in scenarios]
    peak_stds = [results[s]['peak_population']['std'] for s in scenarios]

    bars1 = ax1.bar(x - width/2, final_means, width, yerr=final_stds, label='Final',
                    color=colors[0], alpha=0.8, capsize=5)
    bars2 = ax1.bar(x + width/2, peak_means, width, yerr=peak_stds, label='Peak',
                    color=colors[1], alpha=0.8, capsize=5)

    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Population')
    ax1.set_title('A. Population by Scenario (N=100 replicates)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenario_labels)
    ax1.legend()

    # ===========================================
    # Panel B: Monument and Exotic Investment
    # ===========================================
    ax2 = axes[0, 1]

    monuments_means = [results[s]['total_monuments']['mean'] for s in scenarios]
    monuments_stds = [results[s]['total_monuments']['std'] for s in scenarios]

    exotics_means = [results[s]['total_exotics']['mean'] for s in scenarios]
    exotics_stds = [results[s]['total_exotics']['std'] for s in scenarios]

    # Scale exotics for visibility
    bars1 = ax2.bar(x - width/2, monuments_means, width, yerr=monuments_stds, label='Monuments',
                    color='#8B4513', alpha=0.8, capsize=5)
    bars2 = ax2.bar(x + width/2, exotics_means, width, yerr=exotics_stds, label='Exotic Goods',
                    color='#4ECDC4', alpha=0.8, capsize=5)

    ax2.set_xlabel('Scenario')
    ax2.set_ylabel('Total Investment')
    ax2.set_title('B. Signaling Investment (N=100 replicates)', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenario_labels)
    ax2.legend()

    # ===========================================
    # Panel C: Construction-Climate Correlation
    # ===========================================
    ax3 = axes[1, 0]

    constr_means = [results[s]['construction_climate_r']['mean'] for s in scenarios]
    constr_cis = [(results[s]['construction_climate_r']['mean'] - results[s]['construction_climate_r']['ci_lower'],
                   results[s]['construction_climate_r']['ci_upper'] - results[s]['construction_climate_r']['mean'])
                  for s in scenarios]
    constr_cis = np.array(constr_cis).T

    bars = ax3.bar(x, constr_means, width * 1.5, yerr=constr_cis, color=colors,
                   alpha=0.8, capsize=5, edgecolor='black')

    ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Scenario')
    ax3.set_ylabel('Correlation (r)')
    ax3.set_title('C. Construction-Climate Correlation\n(95% CI)', fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(scenario_labels)

    # Add prediction box
    ax3.text(0.05, 0.95, 'Prediction: r < 0\n(more during drought)',
            transform=ax3.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='#FFE4B5', alpha=0.8))

    # ===========================================
    # Panel D: Exotic Goods-Stress Correlation
    # ===========================================
    ax4 = axes[1, 1]

    exotic_means = [results[s]['exotic_stress_r']['mean'] for s in scenarios]
    exotic_cis = [(results[s]['exotic_stress_r']['mean'] - results[s]['exotic_stress_r']['ci_lower'],
                   results[s]['exotic_stress_r']['ci_upper'] - results[s]['exotic_stress_r']['mean'])
                  for s in scenarios]
    exotic_cis = np.array(exotic_cis).T

    bars = ax4.bar(x, exotic_means, width * 1.5, yerr=exotic_cis, color=colors,
                   alpha=0.8, capsize=5, edgecolor='black')

    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Scenario')
    ax4.set_ylabel('Correlation (r)')
    ax4.set_title('D. Exotic Goods-Stress Correlation\n(95% CI)', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(scenario_labels)

    # Add prediction box
    ax4.text(0.05, 0.95, 'Prediction: r > 0\n(more during stress)',
            transform=ax4.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='#FFE4B5', alpha=0.8))

    plt.suptitle('Chaco Canyon Model: Replicate Analysis with 95% Confidence Intervals',
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")

    return fig


def main():
    """Generate theoretical and validation figures."""
    output_dir = get_project_root() / 'figures' / 'final'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Creating theoretical framework figure...")
    create_theoretical_framework_figure(output_dir / 'figure_8_theoretical_predictions.png')
    plt.close()

    print("Creating replicate validation figure...")
    create_replicate_validation_figure(output_dir / 'figure_9_replicate_validation.png')
    plt.close()

    print("\nFigure generation complete!")


if __name__ == '__main__':
    main()
