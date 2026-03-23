"""
Figure 10: Great House Construction Chronology (Gantt Chart)

Creates a horizontal Gantt-style chart showing major construction periods
for Chaco Canyon great houses, color-coded by type, with period shading
and reference lines.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv
from pathlib import Path

# Output path
output_dir = Path("/Users/clipo/PycharmProjects/chaco-signaling/figures/final")
output_dir.mkdir(parents=True, exist_ok=True)

# Font settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 9

# Okabe-Ito colorblind-friendly palette
OI_BLUE = "#0072B2"
OI_ORANGE = "#E69F00"
OI_VERMILLION = "#D55E00"

# Read data
data_path = Path("/Users/clipo/PycharmProjects/chaco-signaling/data/raw/construction_dates/great_house_chronology.csv")
houses = []

with open(data_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['name'].strip()
        if not name:
            continue
        house_type = row['type'].strip()
        founding = int(row['founding_year'].strip())
        start = int(row['major_construction_start'].strip())
        end = int(row['major_construction_end'].strip())
        peak_year = int(row['peak_year'].strip())

        # Handle peak_rooms: some entries like "great_kiva" are not numeric
        peak_rooms_str = row['peak_rooms'].strip()
        try:
            peak_rooms = int(peak_rooms_str)
        except ValueError:
            peak_rooms = None

        houses.append({
            'name': name,
            'type': house_type,
            'founding': founding,
            'start': start,
            'end': end,
            'peak_year': peak_year,
            'peak_rooms': peak_rooms,
        })

# Sort by founding year (earliest at top, which means highest y-index)
houses.sort(key=lambda h: h['founding'])

n = len(houses)

# Set up figure
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

# --- Period background shading ---
# Early Bonito (850-1020)
ax.axvspan(850, 1020, facecolor='#E8E4D8', alpha=0.5, zorder=0)
# Classic Bonito (1020-1130)
ax.axvspan(1020, 1130, facecolor='#D4CDB8', alpha=0.5, zorder=0)
# Late Bonito (1130-1200)
ax.axvspan(1130, 1200, facecolor='#BFB89E', alpha=0.5, zorder=0)

# Period labels at top
label_y = n + 0.3
ax.text(935, label_y, 'Early Bonito', fontsize=7, ha='center', va='bottom',
        fontstyle='italic', color='#777766')
ax.text(1075, label_y, 'Classic Bonito', fontsize=7, ha='center', va='bottom',
        fontstyle='italic', color='#777766')
ax.text(1165, label_y, 'Late\nBonito', fontsize=6.5, ha='center', va='bottom',
        fontstyle='italic', color='#777766', linespacing=0.9)

# --- Vertical reference lines ---
ax.axvline(x=1020, color='#666666', linewidth=1.0, linestyle='--', zorder=1)
ax.axvline(x=1130, color=OI_VERMILLION, linewidth=1.0, linestyle='--', zorder=1)

# Reference line labels
ax.text(1020, -0.8, '1020 CE\nClassic Bonito\nonset', fontsize=6, ha='center',
        va='top', color='#666666', linespacing=0.9)
ax.text(1130, -0.8, '1130 CE\nMegadrought\nonset', fontsize=6, ha='center',
        va='top', color=OI_VERMILLION, linespacing=0.9)

# --- Draw Gantt bars ---
bar_height = 0.6

for i, house in enumerate(houses):
    y = n - 1 - i  # earliest at top

    # Color by type
    if house['type'] == 'core':
        bar_color = OI_BLUE
    else:
        bar_color = OI_ORANGE

    duration = house['end'] - house['start']

    # Draw main construction bar
    bar = ax.barh(y, duration, left=house['start'], height=bar_height,
                  color=bar_color, edgecolor='white', linewidth=0.5,
                  alpha=0.85, zorder=5)

    # Mark peak year with a dot
    ax.plot(house['peak_year'], y, marker='o', markersize=5, color='white',
            markeredgecolor='black', markeredgewidth=0.7, zorder=6)

    # Add room count label to the right of the bar
    if house['peak_rooms'] is not None:
        label_text = f"{house['peak_rooms']} rooms"
    else:
        label_text = "great kiva"
    ax.text(house['end'] + 3, y, label_text, fontsize=6, ha='left',
            va='center', color='#555555', zorder=7)

# --- Y-axis labels ---
y_positions = list(range(n - 1, -1, -1))
y_labels = [h['name'] for h in houses]
ax.set_yticks(y_positions)
ax.set_yticklabels(y_labels, fontsize=7.5)

# --- X-axis ---
ax.set_xlim(800, 1220)
ax.set_xticks(range(800, 1201, 50))
ax.set_xticklabels([str(y) for y in range(800, 1201, 50)], fontsize=7)
ax.set_xlabel('Year (CE)', fontsize=9)

# --- Y-axis limits ---
ax.set_ylim(-1.5, n + 0.8)

# --- Legend ---
legend_elements = [
    mpatches.Patch(facecolor=OI_BLUE, edgecolor='white', alpha=0.85,
                   label='Canyon core great house'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white',
               markeredgecolor='black', markersize=5, markeredgewidth=0.7,
               label='Peak construction year'),
]
legend = ax.legend(handles=legend_elements, loc='lower right', fontsize=7,
                   framealpha=0.9, edgecolor='#CCCCCC', fancybox=False)

# --- Clean styling ---
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_color('#888888')
ax.spines['bottom'].set_color('#888888')
ax.tick_params(axis='y', length=0)  # no y tick marks
ax.tick_params(axis='x', width=0.5, colors='#888888')

# Subtle vertical grid only
ax.xaxis.grid(True, alpha=0.15, linewidth=0.3)
ax.yaxis.grid(False)

plt.tight_layout()

output_path = output_dir / "Figure_10_construction_chronology.png"
fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Figure 10 saved to: {output_path}")
print(f"File size: {output_path.stat().st_size / 1024:.0f} KB")
