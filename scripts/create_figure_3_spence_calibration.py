"""
Figure 3: Spence Condition Calibrated to Chaco
Equilibrium investment function x*(q) = sqrt(lambda * (q^2 - q_min^2))
calibrated to the Chaco great house spectrum.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
lam = 0.6
q_min = 0.1

q = np.linspace(q_min, 2.0, 500)
x_star = np.sqrt(lam * (q**2 - q_min**2))

# ── Chaco data points ──────────────────────────────────────────────────
chaco_points = [
    (0.1, "Small house communities\n(zero investment)", (-60, 20)),
    (0.5, "Largo Gap\n(~22 rooms)", (-50, 18)),
    (0.7, "Cox Ranch\n(~44 rooms)", (-55, 18)),
    (1.0, "Peripheral\ngreat houses", (15, 15)),
    (1.5, "Chetro Ketl\n(~300 rooms)", (15, 12)),
    (2.0, "Pueblo Bonito\n(~350 rooms)", (-90, 18)),
]

# ── Okabe-Ito inspired colors ──────────────────────────────────────────
curve_color = '#0072B2'       # blue
point_color = '#D55E00'       # vermillion
dashed_color = '#999999'      # grey for dashed lines
annot_color = '#333333'

# ── Figure setup ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

# Plot the equilibrium curve
ax.plot(q, x_star, color=curve_color, linewidth=2.5, zorder=3,
        label=r"$x^*(q) = \sqrt{\lambda(q^2 - q_{\min}^2)}$")

# Plot each Chaco data point
for q_val, label, offset in chaco_points:
    x_val = np.sqrt(lam * (q_val**2 - q_min**2))

    # Point on curve
    ax.plot(q_val, x_val, 'o', color=point_color, markersize=8,
            markeredgecolor='white', markeredgewidth=1.2, zorder=5)

    # Horizontal dashed line to y-axis
    ax.plot([0, q_val], [x_val, x_val], '--', color=dashed_color,
            linewidth=0.8, zorder=2)

    # Vertical dashed line to x-axis
    ax.plot([q_val, q_val], [0, x_val], '--', color=dashed_color,
            linewidth=0.8, zorder=2)

    # Annotation
    ax.annotate(label, xy=(q_val, x_val), xytext=offset,
                textcoords='offset points', fontsize=8,
                color=annot_color, ha='left' if offset[0] > 0 else 'right',
                va='bottom',
                arrowprops=dict(arrowstyle='-', color='#AAAAAA',
                                linewidth=0.8),
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor='none', alpha=0.85))

# ── Axis formatting ────────────────────────────────────────────────────
ax.set_xlabel("Lineage productive capacity ($q$)", fontsize=11,
              labelpad=8)
ax.set_ylabel("Equilibrium monument investment $x^*(q)$", fontsize=11,
              labelpad=8)

ax.set_xlim(-0.05, 2.2)
ax.set_ylim(-0.05, 1.65)

# Minimal gridlines
ax.grid(False)

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Tick formatting
ax.tick_params(axis='both', which='major', labelsize=9, direction='out',
               length=4, width=0.8)

# Parameter annotation in lower-right
param_text = (r"$\lambda = 0.6$" + "\n" +
              r"$q_{\min} = 0.1$")
ax.text(0.97, 0.08, param_text, transform=ax.transAxes,
        fontsize=9, va='bottom', ha='right',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#F7F7F7',
                  edgecolor='#CCCCCC', linewidth=0.8))

# Legend
ax.legend(loc='upper left', fontsize=9.5, frameon=True,
          fancybox=True, framealpha=0.9, edgecolor='#CCCCCC')

# ── Save ────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.5)
outpath = '/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_3_spence_calibration.png'
fig.savefig(outpath, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print(f"Saved: {outpath}")
