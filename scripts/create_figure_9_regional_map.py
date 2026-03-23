"""
Figure 9: Regional Map of Chaco Canyon and Procurement Networks

Creates a schematic map showing Chaco Canyon's location, resource procurement
networks, great house influence area, and the Great North Road.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from pathlib import Path

# Output path
output_dir = Path("/Users/clipo/PycharmProjects/chaco-signaling/figures/final")
output_dir.mkdir(parents=True, exist_ok=True)

# Okabe-Ito colorblind-friendly palette
OI_ORANGE = "#E69F00"
OI_SKYBLUE = "#56B4E9"
OI_GREEN = "#009E73"
OI_YELLOW = "#F0E442"
OI_BLUE = "#0072B2"
OI_VERMILLION = "#D55E00"
OI_PURPLE = "#CC79A7"
OI_BLACK = "#000000"

# Set up figure
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

# Font settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 9

# Map extent (lon, lat)
ax.set_xlim(-110.5, -104.5)
ax.set_ylim(33.5, 38.0)

# --- State boundary at ~37°N ---
ax.axhline(y=37.0, color='#888888', linewidth=0.8, linestyle='-', zorder=1)
ax.text(-107.5, 37.15, 'COLORADO', fontsize=10, fontweight='bold',
        ha='center', va='bottom', color='#666666', fontstyle='italic')
ax.text(-107.5, 36.85, 'NEW MEXICO', fontsize=10, fontweight='bold',
        ha='center', va='top', color='#666666', fontstyle='italic')

# --- San Juan Basin (approximate polygon) ---
sjb_lons = [-109.5, -108.5, -107.0, -106.5, -106.8, -107.5, -108.8, -109.5]
sjb_lats = [37.0, 37.2, 37.0, 36.5, 35.8, 35.5, 35.8, 37.0]
sjb_poly = plt.Polygon(list(zip(sjb_lons, sjb_lats)), closed=True,
                        facecolor='#F5F0E0', edgecolor='#BBAA77',
                        linewidth=1.2, linestyle='--', alpha=0.5, zorder=2)
ax.add_patch(sjb_poly)
ax.text(-108.0, 35.6, 'San Juan\nBasin', fontsize=8, ha='center',
        va='center', color='#998855', fontstyle='italic', zorder=3)

# --- Chaco influence region (~150 km radius, approx 1.35° at this lat) ---
influence_circle = plt.Circle((-107.96, 36.06), 1.35,
                               facecolor='#E8E0D0', edgecolor='#AA9966',
                               linewidth=1.0, linestyle=':', alpha=0.3, zorder=2)
ax.add_patch(influence_circle)
ax.text(-106.5, 34.85, 'Approximate extent of\nChaco influence (~150 km)',
        fontsize=6.5, ha='center', va='top', color='#AA9966',
        fontstyle='italic', zorder=3)

# --- Chaco Canyon (central point) ---
ax.plot(-107.96, 36.06, marker='*', markersize=18, color=OI_VERMILLION,
        markeredgecolor='black', markeredgewidth=0.5, zorder=10)
ax.text(-107.96, 36.16, 'Chaco Canyon', fontsize=9, fontweight='bold',
        ha='center', va='bottom', color=OI_VERMILLION, zorder=10)

# --- Aztec Ruins ---
ax.plot(-107.99, 36.83, marker='s', markersize=8, color=OI_BLUE,
        markeredgecolor='black', markeredgewidth=0.5, zorder=10)
ax.text(-107.85, 36.87, 'Aztec Ruins', fontsize=7.5, ha='left',
        va='bottom', color=OI_BLUE, fontweight='bold', zorder=10)

# --- Great North Road (Chaco to Aztec) ---
ax.plot([-107.96, -107.99], [36.06, 36.83], color=OI_BLUE,
        linewidth=2.0, linestyle='-', zorder=5)
ax.text(-108.15, 36.45, 'Great\nNorth\nRoad', fontsize=6.5,
        ha='center', va='center', color=OI_BLUE, rotation=85,
        fontstyle='italic', zorder=6)

# --- Resource sources ---

# Chuska Mountains (timber)
chuska_lon, chuska_lat = -108.9, 36.7
ax.plot(chuska_lon, chuska_lat, marker='^', markersize=10, color=OI_GREEN,
        markeredgecolor='black', markeredgewidth=0.5, zorder=10)
ax.text(chuska_lon - 0.15, chuska_lat + 0.12, 'Chuska Mts.\n(timber, post-1020 CE)',
        fontsize=7, ha='center', va='bottom', color=OI_GREEN, fontweight='bold', zorder=10)
# Arrow from Chuska to Chaco
ax.annotate('', xy=(-107.96, 36.06), xytext=(chuska_lon, chuska_lat),
            arrowprops=dict(arrowstyle='->', color=OI_GREEN, lw=1.5,
                           connectionstyle='arc3,rad=0.1'), zorder=7)
ax.text(-108.55, 36.25, '~75 km', fontsize=6.5, ha='center', va='center',
        color=OI_GREEN, fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8),
        zorder=8)

# Zuni Mountains (early timber)
zuni_lon, zuni_lat = -108.5, 35.1
ax.plot(zuni_lon, zuni_lat, marker='^', markersize=10, color='#66AA55',
        markeredgecolor='black', markeredgewidth=0.5, zorder=10)
ax.text(zuni_lon + 0.15, zuni_lat - 0.15, 'Zuni Mts.\n(timber, pre-1020 CE)',
        fontsize=7, ha='center', va='top', color='#66AA55', fontweight='bold', zorder=10)
# Arrow from Zuni to Chaco
ax.annotate('', xy=(-107.96, 36.06), xytext=(zuni_lon, zuni_lat),
            arrowprops=dict(arrowstyle='->', color='#66AA55', lw=1.5,
                           connectionstyle='arc3,rad=-0.1'), zorder=7)
ax.text(-108.4, 35.65, '~100 km', fontsize=6.5, ha='center', va='center',
        color='#66AA55', fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8),
        zorder=8)

# Cerrillos Hills (turquoise)
cerrillos_lon, cerrillos_lat = -106.1, 35.4
ax.plot(cerrillos_lon, cerrillos_lat, marker='D', markersize=8, color=OI_SKYBLUE,
        markeredgecolor='black', markeredgewidth=0.5, zorder=10)
ax.text(cerrillos_lon + 0.15, cerrillos_lat + 0.1, 'Cerrillos Hills\n(turquoise)',
        fontsize=7, ha='left', va='bottom', color=OI_SKYBLUE, fontweight='bold', zorder=10)
# Arrow from Cerrillos to Chaco
ax.annotate('', xy=(-107.96, 36.06), xytext=(cerrillos_lon, cerrillos_lat),
            arrowprops=dict(arrowstyle='->', color=OI_SKYBLUE, lw=1.5,
                           connectionstyle='arc3,rad=0.15'), zorder=7)
ax.text(-106.8, 35.9, '~250 km', fontsize=6.5, ha='center', va='center',
        color=OI_SKYBLUE, fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8),
        zorder=8)

# Gulf of California (marine shell) - arrow pointing SW
ax.annotate('', xy=(-110.0, 34.0), xytext=(-109.2, 34.8),
            arrowprops=dict(arrowstyle='->', color=OI_ORANGE, lw=2.0), zorder=7)
ax.text(-110.0, 33.8, 'Gulf of California\n(marine shell)\n~800 km',
        fontsize=7, ha='center', va='top', color=OI_ORANGE, fontweight='bold', zorder=10)
# Dashed line from Chaco toward SW
ax.plot([-107.96, -109.2], [36.06, 34.8], color=OI_ORANGE,
        linewidth=1.2, linestyle='--', zorder=5)

# Mesoamerica (macaws, cacao) - arrow pointing S
ax.annotate('', xy=(-107.5, 33.7), xytext=(-107.5, 34.3),
            arrowprops=dict(arrowstyle='->', color=OI_PURPLE, lw=2.0), zorder=7)
ax.text(-107.5, 33.55, 'Mesoamerica\n(macaws, cacao)\n~1,800 km',
        fontsize=7, ha='center', va='top', color=OI_PURPLE, fontweight='bold', zorder=10)
# Dashed line from Chaco toward S
ax.plot([-107.96, -107.5], [36.06, 34.3], color=OI_PURPLE,
        linewidth=1.2, linestyle='--', zorder=5)

# --- Scale bar ---
# At latitude 36°, 1° longitude ~ 90 km
# 100 km ~ 1.11° longitude
scale_x = -105.5
scale_y = 34.0
bar_length = 1.11  # degrees for ~100 km at this latitude
ax.plot([scale_x, scale_x + bar_length], [scale_y, scale_y],
        color='black', linewidth=2, zorder=10)
ax.plot([scale_x, scale_x], [scale_y - 0.05, scale_y + 0.05],
        color='black', linewidth=2, zorder=10)
ax.plot([scale_x + bar_length, scale_x + bar_length], [scale_y - 0.05, scale_y + 0.05],
        color='black', linewidth=2, zorder=10)
ax.text(scale_x + bar_length / 2, scale_y + 0.1, '100 km',
        fontsize=7, ha='center', va='bottom', zorder=10)

# --- North arrow ---
arrow_x = -105.0
arrow_y = 37.0
ax.annotate('N', xy=(arrow_x, arrow_y + 0.5), xytext=(arrow_x, arrow_y),
            fontsize=10, fontweight='bold', ha='center', va='bottom',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            zorder=10)

# --- Legend ---
legend_elements = [
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor=OI_VERMILLION,
               markeredgecolor='black', markersize=12, label='Chaco Canyon'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=OI_BLUE,
               markeredgecolor='black', markersize=8, label='Outlier great house'),
    plt.Line2D([0], [0], marker='^', color='w', markerfacecolor=OI_GREEN,
               markeredgecolor='black', markersize=8, label='Timber source'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor=OI_SKYBLUE,
               markeredgecolor='black', markersize=7, label='Turquoise source'),
    plt.Line2D([0], [0], color=OI_ORANGE, linewidth=1.5, linestyle='--',
               label='Marine shell route'),
    plt.Line2D([0], [0], color=OI_PURPLE, linewidth=1.5, linestyle='--',
               label='Mesoamerican trade route'),
    plt.Line2D([0], [0], color=OI_BLUE, linewidth=2.0,
               label='Great North Road'),
]
legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=6.5,
                   framealpha=0.9, edgecolor='#CCCCCC', fancybox=False)

# --- Axis formatting ---
ax.set_xlabel('Longitude (°W)', fontsize=9, fontfamily='sans-serif')
ax.set_ylabel('Latitude (°N)', fontsize=9, fontfamily='sans-serif')

# Format tick labels to show degrees
ax.set_xticks([-110, -109, -108, -107, -106, -105])
ax.set_xticklabels(['110°W', '109°W', '108°W', '107°W', '106°W', '105°W'], fontsize=7)
ax.set_yticks([34, 35, 36, 37, 38])
ax.set_yticklabels(['34°N', '35°N', '36°N', '37°N', '38°N'], fontsize=7)

# Clean frame
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
for spine in ax.spines.values():
    spine.set_linewidth(0.5)
    spine.set_color('#888888')
ax.tick_params(width=0.5, colors='#888888')

# Subtle grid
ax.grid(True, alpha=0.15, linewidth=0.3)

# Set aspect to approximate real-world proportions at this latitude
# At 36°N, lon:lat ratio is about cos(36°) ≈ 0.809
ax.set_aspect(1.0 / np.cos(np.radians(36.0)))

plt.tight_layout()

output_path = output_dir / "Figure_9_regional_map.png"
fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Figure 9 saved to: {output_path}")
print(f"File size: {output_path.stat().st_size / 1024:.0f} KB")
