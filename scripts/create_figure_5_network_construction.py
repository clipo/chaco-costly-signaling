"""
Generate Figure 5: Network connectivity alongside construction activity.

Network data approximated from Mills et al. 2018, "Evaluating Chaco migration
scenarios using dynamic social network analysis," Antiquity 92(364): 922-939.

The paper presents ceramic similarity networks for the Chaco World at 50-year
intervals (AD 800-1200) but does not provide tabular network metrics. The
values below are approximated from the network map figures (Figures 3, 4, 7, 8)
and textual descriptions:

- Figure 3 (p. 928): AD 800-850 (very sparse, ~5-8 nodes, few ties);
  AD 850-900 (~25-30 nodes, moderate ties, two disconnected components)
- Figure 4 (p. 930): AD 900-950 (~40 nodes, growing connectivity);
  AD 950-1000 (~60 nodes, substantially more ties, N-S gap closing)
- Figure 7 (p. 934): AD 1000-1050 (~100 nodes, dense connectivity);
  AD 1050-1100 (~130+ nodes, maximum connectivity, most dense network)
- Figure 8 (p. 935): AD 1100-1150 (~110 nodes, still dense but restructured,
  three communities); AD 1150-1200 (~100 nodes, widespread but shifting)

Text (p. 931): "After AD 1050, however, the Chaco Canyon community became more
linked to the greater Northern San Juan area... More nodes, and more connected
nodes, are present throughout the Chaco World."

Text (p. 923): 325 nodes total (sites with >=30 identified sherds).

Construction data from Guiterman et al. 2015 via construction_episodes.csv.

NOTE: Network metric values (relative connectivity index) are APPROXIMATIONS
from visual inspection of the network figures. The paper does not report
numerical network metrics in the main text; eigenvector centrality values
are referenced in supplementary tables (OSM, Tables S1-S8) that were not
available for this extraction.
"""

import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Network connectivity data (approximated from Mills et al. 2018 figures) ──
# Period midpoints and relative connectivity index (0-1 scale)
# based on visual density of network ties and number of nodes visible
# in Figures 3, 4, 7, 8.
network_data = {
    'period_start': [800, 850, 900, 950, 1000, 1050, 1100, 1150],
    'period_end':   [850, 900, 950, 1000, 1050, 1100, 1150, 1200],
    # Approximate node counts visible in each network figure
    # Fig 3 left: ~6; Fig 3 right: ~28; Fig 4 left: ~42; Fig 4 right: ~62
    # Fig 7 left: ~95; Fig 7 right: ~135; Fig 8 left: ~110; Fig 8 right: ~105
    'approx_nodes': [6, 28, 42, 62, 95, 135, 110, 105],
    # Relative connectivity: composite of node count, tie density, and
    # geographic extent, scaled 0-1 (1 = AD 1050-1100 peak)
    # These are subjective visual estimates from the network maps.
    'relative_connectivity': [0.04, 0.15, 0.28, 0.42, 0.70, 1.00, 0.82, 0.75],
}
net_df = pd.DataFrame(network_data)
net_df['period_mid'] = (net_df['period_start'] + net_df['period_end']) / 2

# ── Construction data from Guiterman et al. 2015 ──
constr = pd.read_csv('/Users/clipo/PycharmProjects/chaco-signaling/data/raw/'
                     'construction_dates/construction_episodes.csv')

# Aggregate construction into 50-year bins matching network periods
constr_bins = []
for _, row in net_df.iterrows():
    start, end = row['period_start'], row['period_end']
    mask = (constr['year'] >= start) & (constr['year'] < end)
    total = constr.loc[mask, 'timber_count'].sum()
    constr_bins.append(total)
net_df['timber_count'] = constr_bins

print("Network and construction data:")
print(net_df[['period_start', 'period_end', 'approx_nodes',
              'relative_connectivity', 'timber_count']].to_string(index=False))

# ── Okabe-Ito colorblind-friendly palette ──
color_network = '#0072B2'    # blue
color_construction = '#E69F00'  # orange

# ── Figure ──
fig, ax1 = plt.subplots(figsize=(7, 4.5))

# Construction bars (background)
bar_width = 40
ax1.bar(net_df['period_mid'], net_df['timber_count'],
        width=bar_width, color=color_construction, alpha=0.6,
        edgecolor='white', linewidth=0.5, zorder=2,
        label='Timber count (Guiterman et al. 2015)')

ax1.set_xlabel('Year (CE)', fontsize=11)
ax1.set_ylabel('Total Timber Count (per 50-yr interval)', fontsize=11,
               color=color_construction)
ax1.tick_params(axis='y', labelcolor=color_construction, labelsize=10)
ax1.tick_params(axis='x', labelsize=10)
ax1.set_xlim(775, 1225)

# Remove top spine from both axes
ax1.spines['top'].set_visible(False)

# Network connectivity (second y-axis)
ax2 = ax1.twinx()
ax2.plot(net_df['period_mid'], net_df['relative_connectivity'],
         color=color_network, linewidth=2.5, marker='o', markersize=7,
         markeredgecolor='white', markeredgewidth=1.0, zorder=4,
         label='Relative network connectivity (Mills et al. 2018)')

ax2.set_ylabel('Relative Network Connectivity', fontsize=11,
               color=color_network)
ax2.tick_params(axis='y', labelcolor=color_network, labelsize=10)
ax2.set_ylim(-0.05, 1.15)

# Remove top and right spine styling
ax2.spines['top'].set_visible(False)

# Subtle gridlines on primary axis only
ax1.yaxis.grid(True, alpha=0.15, linewidth=0.5, zorder=0)
ax1.set_axisbelow(True)

# Add period labels
period_labels = [
    (875, 'Pre-Chaco'),
    (1025, 'Early\nFlorescence'),
    (1075, 'Peak\nFlorescence'),
    (1150, 'Decline')
]

# Annotate the peak
ax2.annotate('Peak connectivity\nAD 1050-1100',
             xy=(1075, 1.00), xytext=(1140, 0.90),
             fontsize=8, color=color_network,
             arrowprops=dict(arrowstyle='->', color=color_network,
                             lw=1.0),
             ha='left', va='top')

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           loc='upper left', frameon=True, framealpha=0.9,
           edgecolor='none', fontsize=8)

plt.tight_layout()
plt.savefig('/Users/clipo/PycharmProjects/chaco-signaling/figures/final/'
            'Figure_5_network_construction.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("\nFigure 5 saved to figures/final/Figure_5_network_construction.png")
