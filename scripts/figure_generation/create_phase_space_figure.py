#!/usr/bin/env python3
"""
Create phase space predictions figure for Chaco Canyon paper.

This figure shows what the model predicts should happen under different
environmental conditions - similar to the Rapa Nui phase space figure.

Key panels:
1. Phase space showing signaling dominance vs. non-signaling across σ values
2. Population trajectories under different scenarios
3. Signaling investment patterns
4. Collapse dynamics and timing
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.gridspec import GridSpec
from pathlib import Path
import matplotlib.patches as mpatches


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def create_phase_space_predictions_figure(save_path=None):
    """
    Create comprehensive phase space figure showing model predictions
    under different environmental conditions.
    """

    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Color scheme (matching Rapa Nui paper)
    # Orange = monument building/signaling dominates
    # Purple = high reproduction dominates (no signaling)
    color_signaling = '#FF8C00'  # Orange
    color_reproduction = '#8A2BE2'  # Purple
    color_collapse = '#DC143C'  # Crimson for collapse

    # ===========================================
    # Panel A: Environmental Phase Space
    # ===========================================
    ax1 = fig.add_subplot(gs[0, 0])

    # Create phase space grid
    frequency = np.linspace(5, 25, 100)  # Years between droughts
    magnitude = np.linspace(0.1, 0.9, 100)  # Drought severity

    F, M = np.meshgrid(frequency, magnitude)

    # Calculate σ for each point
    # σ = (magnitude × duration) / frequency
    duration = 1 + M * 2.5  # Duration scales with magnitude
    sigma = (M * duration) / F

    # Define regions based on σ threshold
    sigma_threshold = 0.15

    # Create colored regions
    colors = np.zeros((*sigma.shape, 4))

    # Below threshold: high reproduction dominates (purple)
    below_mask = sigma < sigma_threshold
    colors[below_mask] = [0.54, 0.17, 0.89, 0.7]  # Purple with alpha

    # Above threshold: signaling dominates (orange)
    above_mask = (sigma >= sigma_threshold) & (sigma < 0.25)
    colors[above_mask] = [1.0, 0.55, 0.0, 0.7]  # Orange with alpha

    # Extreme: collapse zone (red)
    extreme_mask = sigma >= 0.25
    colors[extreme_mask] = [0.86, 0.08, 0.24, 0.7]  # Crimson with alpha

    ax1.imshow(colors, extent=[5, 25, 0.1, 0.9], origin='lower', aspect='auto')

    # Add contour lines for σ
    cs = ax1.contour(F, M, sigma, levels=[0.10, 0.15, 0.20, 0.25, 0.30],
                     colors='white', linewidths=1.5, linestyles='--')
    ax1.clabel(cs, fmt='σ=%.2f', fontsize=8, colors='white')

    # Mark critical threshold
    ax1.contour(F, M, sigma, levels=[sigma_threshold], colors='yellow',
                linewidths=3, linestyles='-')

    # Add Chaco period markers
    # Pre-Chaco: ~15 year return period, mild-moderate magnitude
    ax1.plot(15, 0.35, 'o', markersize=14, color='white', markeredgecolor='black',
             markeredgewidth=2, zorder=10)
    ax1.text(15.5, 0.38, 'Pre-Chaco\n(800-900)', fontsize=9, color='white',
             fontweight='bold', ha='left')

    # Early Chaco: more frequent, moderate magnitude
    ax1.plot(12, 0.45, 's', markersize=14, color='white', markeredgecolor='black',
             markeredgewidth=2, zorder=10)
    ax1.text(12.5, 0.48, 'Early Chaco\n(900-1000)', fontsize=9, color='white',
             fontweight='bold', ha='left')

    # Florescence: frequent droughts, high magnitude
    ax1.plot(10, 0.6, '^', markersize=14, color='white', markeredgecolor='black',
             markeredgewidth=2, zorder=10)
    ax1.text(10.5, 0.63, 'Florescence\n(1000-1130)', fontsize=9, color='white',
             fontweight='bold', ha='left')

    # Megadrought: extreme
    ax1.plot(8, 0.8, 'D', markersize=14, color='white', markeredgecolor='black',
             markeredgewidth=2, zorder=10)
    ax1.text(8.5, 0.75, 'Megadrought\n(1130-1150)', fontsize=9, color='white',
             fontweight='bold', ha='left')

    ax1.set_xlabel('Drought Return Period (years)', fontsize=11)
    ax1.set_ylabel('Drought Magnitude', fontsize=11)
    ax1.set_title('A. Environmental Phase Space', fontsize=12, fontweight='bold')

    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=color_reproduction, label='Reproduction dominates'),
        mpatches.Patch(facecolor=color_signaling, label='Signaling dominates'),
        mpatches.Patch(facecolor=color_collapse, label='Collapse zone'),
    ]
    ax1.legend(handles=legend_elements, loc='lower right', fontsize=9)

    # ===========================================
    # Panel B: Predicted Population Trajectories
    # ===========================================
    ax2 = fig.add_subplot(gs[0, 1])

    years = np.arange(800, 1201)

    # Generate schematic population trajectories for different conditions

    # Low σ (no signaling needed): steady growth, then gradual decline
    pop_low = 500 + 400 * (1 - np.exp(-(years - 800) / 100))
    pop_low = np.where(years > 1100, pop_low * (1 - 0.002 * (years - 1100)), pop_low)

    # Moderate σ (signaling active): boom-bust with recovery
    pop_mod = 500 + 600 * np.sin((years - 800) * np.pi / 300) * np.exp(-(years - 950)**2 / 30000)
    pop_mod = np.maximum(pop_mod, 300)
    pop_mod = np.where(years < 900, 500 + (years - 800) * 2, pop_mod)

    # High σ (megadrought): rapid growth, then collapse
    pop_high = 500 + 700 * (1 - np.exp(-(years - 800) / 80))
    collapse_point = 1130
    pop_high = np.where(years > collapse_point,
                        pop_high[years == collapse_point][0] * np.exp(-0.05 * (years - collapse_point)),
                        pop_high)

    ax2.plot(years, pop_low, '-', color=color_reproduction, linewidth=2.5,
             label='Low σ (reproduction)')
    ax2.plot(years, pop_mod, '-', color=color_signaling, linewidth=2.5,
             label='Moderate σ (signaling)')
    ax2.plot(years, pop_high, '-', color=color_collapse, linewidth=2.5,
             label='Extreme σ (collapse)')

    # Mark key events
    ax2.axvline(x=1000, color='gray', linestyle=':', alpha=0.5)
    ax2.axvline(x=1130, color='gray', linestyle=':', alpha=0.5)
    ax2.text(1000, ax2.get_ylim()[1] * 0.95, 'Florescence\nOnset', fontsize=8,
             ha='center', style='italic')
    ax2.text(1130, ax2.get_ylim()[1] * 0.95, 'Mega-\ndrought', fontsize=8,
             ha='center', style='italic')

    ax2.set_xlabel('Year (CE)', fontsize=11)
    ax2.set_ylabel('Population', fontsize=11)
    ax2.set_title('B. Predicted Population Trajectories', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=9)
    ax2.set_xlim(800, 1200)
    ax2.set_ylim(0, 1500)

    # ===========================================
    # Panel C: Signaling Investment Predictions
    # ===========================================
    ax3 = fig.add_subplot(gs[1, 0])

    # Schematic signaling investment under different conditions

    # Low σ: minimal signaling
    signal_low = 50 + 20 * np.sin((years - 800) * np.pi / 200)
    signal_low = np.maximum(signal_low, 10)

    # Moderate σ: high signaling during stress
    signal_mod = 50 + 150 * np.exp(-((years - 1050)**2) / 5000)
    signal_mod = np.where(years < 900, 50, signal_mod)

    # High σ: peak signaling before collapse
    signal_high = 50 + 200 * (1 - np.exp(-(years - 900) / 50))
    signal_high = np.where(years > 1100, signal_high[years == 1100][0] * 1.5 * np.exp(-0.02 * (years - 1100)), signal_high)
    signal_high = np.where(years > 1150, 0, signal_high)

    ax3.fill_between(years, 0, signal_low, alpha=0.3, color=color_reproduction,
                     label='Low σ')
    ax3.fill_between(years, 0, signal_mod, alpha=0.3, color=color_signaling,
                     label='Moderate σ')
    ax3.fill_between(years, 0, signal_high, alpha=0.3, color=color_collapse,
                     label='Extreme σ')

    ax3.plot(years, signal_low, '-', color=color_reproduction, linewidth=2)
    ax3.plot(years, signal_mod, '-', color=color_signaling, linewidth=2)
    ax3.plot(years, signal_high, '-', color=color_collapse, linewidth=2)

    # Add annotations
    ax3.annotate('Signaling peaks\nduring stress',
                xy=(1050, 200), xytext=(1100, 250),
                fontsize=9, style='italic',
                arrowprops=dict(arrowstyle='->', color='black'))

    ax3.annotate('Collapse:\nsignaling ends',
                xy=(1150, 50), xytext=(1170, 150),
                fontsize=9, style='italic',
                arrowprops=dict(arrowstyle='->', color='black'))

    ax3.set_xlabel('Year (CE)', fontsize=11)
    ax3.set_ylabel('Signaling Investment (relative)', fontsize=11)
    ax3.set_title('C. Predicted Signaling Investment', fontsize=12, fontweight='bold')
    ax3.legend(loc='upper left', fontsize=9)
    ax3.set_xlim(800, 1200)

    # ===========================================
    # Panel D: Predicted Outcomes Summary
    # ===========================================
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')

    ax4.text(0.5, 0.95, 'D. Model Predictions by Environmental Condition',
             fontsize=12, fontweight='bold', ha='center', transform=ax4.transAxes)

    # Create prediction table
    conditions = [
        ('Low σ (< 0.15)', color_reproduction, [
            'Minimal monument building',
            'Low exotic goods investment',
            'Steady population growth',
            'Baseline conflict levels',
            'No "Pax Chaco" effect'
        ]),
        ('Moderate σ (0.15-0.25)', color_signaling, [
            'Active monument building',
            'High exotic goods acquisition',
            'Population peaks then stabilizes',
            'Reduced inter-group conflict',
            '"Pax Chaco" emerges'
        ]),
        ('Extreme σ (> 0.25)', color_collapse, [
            'Maximum signaling before collapse',
            'Exotic goods spike then cease',
            'Population crashes',
            'Post-collapse violence increases',
            'System abandonment'
        ])
    ]

    y_start = 0.85
    for condition, color, predictions in conditions:
        # Condition header
        ax4.add_patch(FancyBboxPatch((0.05, y_start - 0.03), 0.9, 0.08,
                                      boxstyle="round,pad=0.01",
                                      facecolor=color, edgecolor='black',
                                      transform=ax4.transAxes, alpha=0.8))
        ax4.text(0.5, y_start, condition, fontsize=10, fontweight='bold',
                ha='center', transform=ax4.transAxes, color='white')

        y_start -= 0.05
        for pred in predictions:
            ax4.text(0.1, y_start, f'• {pred}', fontsize=9,
                    transform=ax4.transAxes)
            y_start -= 0.04

        y_start -= 0.02

    # Add archaeological validation note
    ax4.text(0.5, 0.02, 'Predictions testable against Chaco archaeological record',
             fontsize=9, style='italic', ha='center', transform=ax4.transAxes,
             color='gray')

    plt.suptitle('Chaco Canyon Costly Signaling Model: Phase Space Predictions',
                fontsize=14, fontweight='bold', y=0.98)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")

    return fig


def main():
    """Generate phase space predictions figure."""
    output_dir = get_project_root() / 'figures' / 'final'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Creating phase space predictions figure...")
    create_phase_space_predictions_figure(
        output_dir / 'figure_10_phase_space_predictions.png'
    )
    plt.close()

    print("\nFigure generation complete!")


if __name__ == '__main__':
    main()
