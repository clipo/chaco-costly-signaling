"""
Figure 2: Three-Layer Model Schematic
Conceptual diagram showing the three layers of the costly signaling model
with Chaco-specific content and feedback loop.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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

plt.rcParams['font.size'] = 9
plt.rcParams['mathtext.default'] = 'regular'

# ── Figure setup ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7.5)
ax.axis('off')

# ── Color palette (soft, colorblind-friendly) ───────────────────────────
color_layer1 = '#D4E6F1'  # soft blue
color_layer2 = '#D5F5E3'  # soft green
color_layer3 = '#FDEBD0'  # soft orange
border_layer1 = '#2980B9'
border_layer2 = '#27AE60'
border_layer3 = '#E67E22'
arrow_color = '#555555'
feedback_color = '#C0392B'

# ── Helper function for rounded boxes ───────────────────────────────────
def draw_layer_box(ax, x, y, w, h, facecolor, edgecolor, label, equation,
                   chaco_line1, chaco_line2):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         facecolor=facecolor, edgecolor=edgecolor,
                         linewidth=1.8, zorder=2)
    ax.add_patch(box)

    cx = x + w / 2
    top = y + h

    # Layer label (bold)
    ax.text(cx, top - 0.30, label,
            ha='center', va='top', fontsize=10.5, fontweight='bold',
            color='#2C3E50', zorder=3)

    # Equation (italic math)
    ax.text(cx, top - 0.68, equation,
            ha='center', va='top', fontsize=9.5,
            color='#2C3E50', fontstyle='italic', zorder=3)

    # Chaco content lines
    ax.text(cx, top - 1.05, chaco_line1,
            ha='center', va='top', fontsize=8.5,
            color='#555555', zorder=3)
    ax.text(cx, top - 1.35, chaco_line2,
            ha='center', va='top', fontsize=8.5,
            color='#555555', zorder=3)


# ── Box dimensions ─────────────────────────────────────────────────────
box_w = 6.4
box_h = 1.6
box_x = 1.8

layer1_y = 5.4
layer2_y = 3.2
layer3_y = 1.0

# ── Draw layer boxes ───────────────────────────────────────────────────
draw_layer_box(ax, box_x, layer1_y, box_w, box_h,
               color_layer1, border_layer1,
               "Layer 1: Individual Signaling Equilibrium",
               r"$c(x, q) = x^2 / (2q)$      $x^*(q) = \sqrt{\lambda(q^2 - q_{min}^2)}$",
               "Lineage quality \u2192 construction investment",
               "Pueblo Bonito matriline (high q) \u2192 350+ rooms\nSmall houses ($q_{min}$) \u2192 zero monument investment")

draw_layer_box(ax, box_x, layer2_y, box_w, box_h,
               color_layer2, border_layer2,
               "Layer 2: Intergroup Assessment",
               r"$\sigma_{eff} = \sigma_0 / \sqrt{1 + \kappa(M_g + M_h)}$      $P(conflict) \downarrow$ with $M$",
               "Great houses in high-visibility locations (p < 0.001)",
               'Result: "Pax Chaco" during florescence')

draw_layer_box(ax, box_x, layer3_y, box_w, box_h,
               color_layer3, border_layer3,
               "Layer 3: Cooperation Networks",
               r"$S(\sigma, k) = \exp(-\sigma / (1 + \gamma k))$",
               "Exchange partners buffer environmental crises",
               r"Feedback: $\lambda(\sigma) = \lambda_0 + \lambda_1 \cdot \sigma$")

# ── Arrows between layers (downward) ───────────────────────────────────
arrow_props = dict(arrowstyle='->', color=arrow_color, linewidth=1.8,
                   mutation_scale=18, zorder=4)

cx = box_x + box_w / 2

# Layer 1 -> Layer 2
ax.annotate('', xy=(cx, layer2_y + box_h + 0.03),
            xytext=(cx, layer1_y - 0.03),
            arrowprops=arrow_props)

# Layer 2 -> Layer 3
ax.annotate('', xy=(cx, layer3_y + box_h + 0.03),
            xytext=(cx, layer2_y - 0.03),
            arrowprops=arrow_props)

# ── Arrow labels ────────────────────────────────────────────────────────
ax.text(cx + 0.15, (layer1_y + layer2_y + box_h) / 2 + 0.02,
        "Signal investment\nreveals quality",
        ha='left', va='center', fontsize=7.5, color=arrow_color,
        fontstyle='italic')

ax.text(cx + 0.15, (layer2_y + layer3_y + box_h) / 2 + 0.02,
        "Reduced conflict\nenables cooperation",
        ha='left', va='center', fontsize=7.5, color=arrow_color,
        fontstyle='italic')

# ── Feedback loop (right side, Layer 3 back to Layer 1) ─────────────────
fb_x = box_x + box_w + 0.25  # right edge of boxes + margin
fb_x2 = fb_x + 0.6

# Draw feedback path: Layer 3 right -> up -> Layer 1 right
# Segment 1: horizontal from Layer 3 right side
ax.annotate('', xy=(fb_x2, layer3_y + box_h / 2),
            xytext=(box_x + box_w, layer3_y + box_h / 2),
            arrowprops=dict(arrowstyle='-', color=feedback_color,
                            linewidth=1.8, linestyle='--'))

# Segment 2: vertical up
ax.annotate('', xy=(fb_x2, layer1_y + box_h / 2),
            xytext=(fb_x2, layer3_y + box_h / 2),
            arrowprops=dict(arrowstyle='-', color=feedback_color,
                            linewidth=1.8, linestyle='--'))

# Segment 3: horizontal back to Layer 1 right side (with arrow)
ax.annotate('', xy=(box_x + box_w, layer1_y + box_h / 2),
            xytext=(fb_x2, layer1_y + box_h / 2),
            arrowprops=dict(arrowstyle='->', color=feedback_color,
                            linewidth=1.8, linestyle='--',
                            mutation_scale=18))

# Feedback label (rotated, along vertical segment)
ax.text(fb_x2 + 0.15, (layer1_y + layer3_y + box_h) / 2,
        r"$\sigma$ (uncertainty) $\uparrow$ $\Rightarrow$ $\lambda$ $\uparrow$"
        "\ndrives investment",
        ha='left', va='center', fontsize=8, color=feedback_color,
        fontweight='bold', rotation=0)

# ── Left-side environmental driver ──────────────────────────────────────
env_x = box_x - 0.2
env_y = layer3_y + box_h / 2

# Environmental uncertainty label on the left
ax.text(0.3, env_y + 0.15, "Environmental\nuncertainty",
        ha='center', va='center', fontsize=8, color='#7D3C98',
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5EEF8',
                  edgecolor='#7D3C98', linewidth=1.2))

ax.annotate('', xy=(box_x, env_y),
            xytext=(1.05, env_y),
            arrowprops=dict(arrowstyle='->', color='#7D3C98',
                            linewidth=1.5, mutation_scale=15))

ax.text(1.35, env_y + 0.25, r"$\sigma$", fontsize=10, color='#7D3C98',
        ha='center', va='bottom', fontweight='bold')

# ── Save ────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.3)
outpath = '/Users/clipo/PycharmProjects/chaco-signaling/figures/final/Figure_2_three_layer_model.png'
fig.savefig(outpath, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print(f"Saved: {outpath}")
