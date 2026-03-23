"""
Generate Figure 4: Visibility distributions for great houses vs. great kivas.

Data extracted from Dungan et al. 2018, Figure 4 (p. 910), "A total viewshed
approach to local visibility in the Chaco World," Antiquity 92(364): 905-921.

The values below are approximated from the bar chart histograms in Figure 4.
Great Houses (n=269): Strong right-skew; approximately half fall in deciles 8-10.
    Text (p. 913): "approximately half of the great houses falling into the
    eighth decile or higher"
Great Kivas (n=161): More uniform/central distribution; less emphasis on
    high-visibility locations.

Decile values were read from the histogram bar heights, then adjusted so
counts sum to the reported totals (269 great houses, 161 great kivas).
"""

import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Data from Dungan et al. 2018, Figure 4 (p. 910) ──
# Values approximated from histogram bar heights.
# Great Houses histogram: y-axis to 50, clear right-skew.
#   Reading bar heights (approximate):
#   1: ~3, 2: ~6, 3: ~10, 4: ~13, 5: ~16, 6: ~22, 7: ~30, 8: ~42, 9: ~48, 10: ~47
#   Raw sum = 237; scaled to sum to 269.
#   After careful re-reading with the constraint from p. 913 that "approximately
#   half" fall in decile 8+: deciles 8+9+10 should be ~134-140.
#
# Great Kivas histogram: y-axis to 25, more uniform with slight central peak.
#   Reading bar heights (approximate):
#   1: ~5, 2: ~10, 3: ~14, 4: ~18, 5: ~20, 6: ~22, 7: ~20, 8: ~19, 9: ~18, 10: ~15
#   Raw sum = 161 (adjusted).

deciles = np.arange(1, 11)

# Great Houses (n=269) - approximated from Figure 4 histogram
# Strong right-skew with peak around deciles 8-10
# The text states ~50% in decile 8 or higher
great_houses = np.array([3, 6, 10, 14, 17, 23, 30, 43, 48, 47])
# Verify and adjust to sum to 269
gh_sum = great_houses.sum()  # = 241
# Scale to match n=269
great_houses_scaled = np.round(great_houses * 269 / gh_sum).astype(int)
# Fix rounding to ensure sum = 269
diff = 269 - great_houses_scaled.sum()
# Add/subtract from the largest bin to fix
great_houses_scaled[np.argmax(great_houses_scaled)] += diff
great_houses_final = great_houses_scaled

# Great Kivas (n=161) - approximated from Figure 4 histogram
# More uniform distribution, slight peak around deciles 5-7
# Text notes they are NOT significantly skewed toward high visibility
great_kivas = np.array([5, 10, 15, 18, 21, 23, 20, 19, 17, 13])
# Verify and adjust to sum to 161
gk_sum = great_kivas.sum()  # = 161
great_kivas_scaled = np.round(great_kivas * 161 / gk_sum).astype(int)
diff = 161 - great_kivas_scaled.sum()
great_kivas_scaled[np.argmax(great_kivas_scaled)] += diff
great_kivas_final = great_kivas_scaled

print("Great Houses per decile:", great_houses_final, "sum =", great_houses_final.sum())
print("Great Kivas per decile:", great_kivas_final, "sum =", great_kivas_final.sum())
print(f"Great Houses in deciles 8+: {great_houses_final[7:].sum()} "
      f"({100*great_houses_final[7:].sum()/269:.1f}%)")

# Convert to proportions for comparison
gh_prop = great_houses_final / 269
gk_prop = great_kivas_final / 161
uniform_prop = np.full(10, 0.10)  # expected under uniform distribution

# ── Okabe-Ito colorblind-friendly palette ──
color_gh = '#E69F00'   # orange
color_gk = '#0072B2'   # blue
color_uniform = '#999999'  # gray for reference line

# ── Figure ──
fig, ax = plt.subplots(figsize=(7, 4.5))

bar_width = 0.35
x = np.arange(1, 11)

bars_gh = ax.bar(x - bar_width/2, gh_prop * 100, bar_width,
                 color=color_gh, edgecolor='white', linewidth=0.5,
                 label=f'Great Houses (n=269)', zorder=3)
bars_gk = ax.bar(x + bar_width/2, gk_prop * 100, bar_width,
                 color=color_gk, edgecolor='white', linewidth=0.5,
                 label=f'Great Kivas (n=161)', zorder=3)

# Uniform reference line at 10%
ax.axhline(y=10, color=color_uniform, linestyle='--', linewidth=1.0,
           label='Uniform distribution', zorder=2)

# Axis formatting
ax.set_xlabel('Visibility Decile', fontsize=11)
ax.set_ylabel('Percentage of Sites (%)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(x, fontsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlim(0.2, 10.8)
ax.set_ylim(0, 22)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Subtle gridlines
ax.yaxis.grid(True, alpha=0.2, linewidth=0.5, zorder=0)
ax.set_axisbelow(True)

# Legend
ax.legend(loc='upper left', frameon=True, framealpha=0.9,
          edgecolor='none', fontsize=9)

plt.tight_layout()
plt.savefig('/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_4_visibility_distributions.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("\nFigure 4 saved to figures/final/Figure_4_visibility_distributions.png")
