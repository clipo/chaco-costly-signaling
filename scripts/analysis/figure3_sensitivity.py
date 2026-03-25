"""
Figure 3 Sensitivity Analysis: Spence equilibrium investment x*(q)
across a range of lambda values.

Shows that the qualitative pattern (monotonically increasing, concave)
is robust to the choice of lambda. Chaco sites marked at the reference
parameterization (lambda = 0.6).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ── Font setup ──────────────────────────────────────────────────────────
for font in ['Arial', 'Helvetica', 'DejaVu Sans']:
    try:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [font]
        fig_test = plt.figure()
        fig_test.text(0.5, 0.5, 'test')
        plt.close(fig_test)
        break
    except Exception:
        continue

plt.rcParams['font.size'] = 10
plt.rcParams['mathtext.default'] = 'regular'

# ── Parameters ──────────────────────────────────────────────────────────
q_min = 0.1
lambda_values = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
lambda_ref = 0.6  # reference parameterization for site markers

q = np.linspace(q_min, 2.5, 600)


def x_star(q_arr, lam, qm):
    """Spence equilibrium investment: x*(q) = sqrt(lambda * (q^2 - q_min^2))"""
    return np.sqrt(lam * (q_arr**2 - qm**2))


# ── Chaco site data ────────────────────────────────────────────────────
# (q_value, label, annotation_offset)
chaco_sites = [
    (0.1,  "Small house\ncommunities",             (-15, 22)),
    (0.5,  "Largo Gap\n(~22 rooms)",                (-60, 18)),
    (0.7,  "Cox Ranch\n(~44 rooms)",                (-60, 16)),
    (1.3,  "Hungo Pavi\n(~150 rooms)",              (12, 14)),
    (1.86, "Chetro Ketl\n(~300 rooms)",             (12, 10)),
    (2.0,  "Pueblo Bonito\n(~350 rooms)",           (-95, 16)),
]

# ── Colormap: viridis-based, colorblind-friendly ───────────────────────
cmap = plt.cm.viridis
norm = plt.Normalize(vmin=min(lambda_values), vmax=max(lambda_values))

# ── Figure ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

# Compute envelope (min/max across all lambda values) for shaded band
x_all = np.array([x_star(q, lam, q_min) for lam in lambda_values])
x_lower = x_all.min(axis=0)
x_upper = x_all.max(axis=0)

ax.fill_between(q, x_lower, x_upper, color='#CCCCCC', alpha=0.35,
                zorder=1, label='Range across $\\lambda$ values')

# Plot each lambda curve
for lam in lambda_values:
    color = cmap(norm(lam))
    lw = 2.5 if lam == lambda_ref else 1.5
    ls = '-' if lam == lambda_ref else '--'
    alpha = 1.0 if lam == lambda_ref else 0.8
    ax.plot(q, x_star(q, lam, q_min), color=color, linewidth=lw,
            linestyle=ls, alpha=alpha, zorder=3,
            label=f'$\\lambda = {lam:.1f}$')

# ── Chaco site markers on the reference curve ──────────────────────────
point_color = '#D55E00'  # Okabe-Ito vermillion
annot_color = '#333333'

for q_val, label, offset in chaco_sites:
    x_val = x_star(np.array([q_val]), lambda_ref, q_min)[0]

    ax.plot(q_val, x_val, 'o', color=point_color, markersize=8,
            markeredgecolor='white', markeredgewidth=1.2, zorder=6)

    ax.annotate(label, xy=(q_val, x_val), xytext=offset,
                textcoords='offset points', fontsize=7.5,
                color=annot_color,
                ha='left' if offset[0] > 0 else 'right',
                va='bottom',
                arrowprops=dict(arrowstyle='-', color='#AAAAAA',
                                linewidth=0.8),
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor='none', alpha=0.85),
                zorder=7)

# ── Axis formatting ────────────────────────────────────────────────────
ax.set_xlabel("Quality ($q$)", fontsize=11, labelpad=8)
ax.set_ylabel("Equilibrium investment $x^*(q)$", fontsize=11, labelpad=8)

ax.set_xlim(-0.05, 2.6)
ax.set_ylim(-0.05, max(x_upper) * 1.08)

ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='both', which='major', labelsize=9, direction='out',
               length=4, width=0.8)

# ── Legend ──────────────────────────────────────────────────────────────
# Custom legend: lambda curves, shaded band, and site markers
handles, labels = ax.get_legend_handles_labels()

# Add a custom entry for the site markers
site_handle = Line2D([0], [0], marker='o', color='w',
                     markerfacecolor=point_color, markeredgecolor='white',
                     markeredgewidth=1.0, markersize=7, linestyle='None')
handles.append(site_handle)
labels.append('Chaco sites ($\\lambda = 0.6$)')

ax.legend(handles=handles, labels=labels, loc='upper left', fontsize=8,
          frameon=True, fancybox=True, framealpha=0.9, edgecolor='#CCCCCC',
          ncol=2)

# ── Parameter box ──────────────────────────────────────────────────────
param_text = (r"$x^*(q) = \sqrt{\lambda\,(q^2 - q_{\min}^2)}$" + "\n" +
              r"$q_{\min} = 0.1$")
ax.text(0.97, 0.05, param_text, transform=ax.transAxes,
        fontsize=9, va='bottom', ha='right',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#F7F7F7',
                  edgecolor='#CCCCCC', linewidth=0.8))

# ── Save ───────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.5)
outpath = '/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_3_spence_sensitivity.png'
fig.savefig(outpath, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print(f"Saved: {outpath}")
