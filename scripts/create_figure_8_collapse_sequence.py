"""
Figure 8: Collapse Sequence Timeline (AD 1050-1300)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------- style setup ----------
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 9,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
})

# Okabe-Ito colors mapped to event categories
COLORS = {
    'construction': '#0072B2',   # blue
    'ritual':       '#CC79A7',   # pink/reddish-purple
    'environmental':'#D55E00',   # vermillion
    'violence':     '#E69F00',   # amber/orange
    'migration':    '#009E73',   # green
}

# ---------- events ----------
# Each: (start, end, label, category, y_position)
# y_position spaces events vertically
events = [
    (1050, 1100, 'Peak construction &\nnetwork connectivity',  'construction',  7),
    (1075, 1100, 'False-wall construction\nbegins (Van Dyke 2004)',  'construction',  6),
    (1095, 1105, 'Termination rituals at\nPueblo Bonito (Crown & Wills 2018)', 'ritual', 5),
    (1100, 1130, 'Construction investment\ndeclines (Wills et al. 2014)',  'construction',  4),
    (1130, 1180, 'Megadrought',  'environmental', 3),
    (1140, 1160, 'Canyon largely\ndepopulated',  'migration',     2),
    (1150, 1300, 'Post-Chaco violence\nincrease (Mesa Verde region)',  'violence',      1),
    (1100, 1275, 'Aztec as\nsuccessor center',  'migration',     0),
]

# ---------- figure ----------
fig, ax = plt.subplots(figsize=(7, 4.2))

bar_height = 0.55

for (start, end, label, category, ypos) in events:
    color = COLORS[category]
    width = end - start
    # Draw horizontal bar
    ax.barh(ypos, width, left=start, height=bar_height, color=color,
            alpha=0.7, edgecolor=color, linewidth=0.8, zorder=2)
    # Label: place to the right of the bar, or inside if long enough
    if width >= 60:
        ax.text(start + width / 2, ypos, label, ha='center', va='center',
                fontsize=7.5, color='white', fontweight='bold', zorder=3)
    else:
        ax.text(end + 3, ypos, label, ha='left', va='center',
                fontsize=7.5, color='#333333', zorder=3)

# X-axis
ax.set_xlim(1045, 1310)
ax.set_xlabel('Year (CE)', fontsize=10)
ax.set_xticks(np.arange(1050, 1310, 25))

# Y-axis: hide numeric labels
ax.set_yticks([])
ax.set_ylim(-0.8, 8.0)

# Grid: subtle vertical lines only
ax.xaxis.grid(True, linewidth=0.3, alpha=0.4, color='#cccccc', zorder=0)
ax.yaxis.grid(False)

# Spines
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_position(('outward', 5))

# Legend
legend_handles = [
    mpatches.Patch(color=COLORS['construction'], alpha=0.7, label='Construction'),
    mpatches.Patch(color=COLORS['ritual'], alpha=0.7, label='Ritual'),
    mpatches.Patch(color=COLORS['environmental'], alpha=0.7, label='Environmental'),
    mpatches.Patch(color=COLORS['violence'], alpha=0.7, label='Violence'),
    mpatches.Patch(color=COLORS['migration'], alpha=0.7, label='Migration'),
]
ax.legend(handles=legend_handles, loc='upper right', fontsize=7.5,
          frameon=True, framealpha=0.9, edgecolor='#cccccc',
          ncol=1, handlelength=1.2, handleheight=0.9)

ax.tick_params(axis='x', direction='out', length=4)
ax.tick_params(axis='y', length=0)

fig.tight_layout()

outpath = '/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_8_collapse_sequence.png'
fig.savefig(outpath, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'Saved: {outpath}')
