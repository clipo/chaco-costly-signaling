#!/usr/bin/env python3
"""
Process real PMDI data from Living Blended Drought Atlas (LBDA) v2 for Chaco Canyon simulation.

Data source: NOAA NCEI LBDA Version 2
- Citation: Gille, E.P., C.S. Wahl, T.M. Vose, and E.R. Cook. 2017.
  Living Blended Drought Atlas (LBDA) Version 2 - Recalibrated reconstruction of
  United States Summer PMDI over the last 2000 years.
  NOAA/NCEI https://doi.org/10.25921/7xm8-jn36

Grid point: 36.25°N, 108.25°W (closest to Chaco Canyon at 36.06°N, 107.96°W)
Resolution: 0.5° x 0.5° gridded PMDI (Palmer Modified Drought Index)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict
import json


def load_chaco_pmdi(filepath: Path) -> pd.DataFrame:
    """Load the extracted Chaco region PMDI data."""
    df = pd.read_csv(filepath, sep=r'\s+')
    return df


def create_spatial_average(df: pd.DataFrame, center_lat: float = 36.25,
                          center_lon: float = -108.25) -> pd.DataFrame:
    """
    Create spatially-weighted average PMDI for Chaco Canyon.

    Uses inverse-distance weighting from center point (Chaco Canyon).
    """
    # Calculate distance from Chaco center for each grid point
    unique_points = df[['Lat', 'Lon']].drop_duplicates()

    # Simple inverse distance weights (approximate, ignores Earth curvature)
    weights = {}
    for _, row in unique_points.iterrows():
        dist = np.sqrt((row['Lat'] - center_lat)**2 + (row['Lon'] - center_lon)**2)
        # Inverse distance weight (with small offset to avoid div by zero)
        weights[(row['Lat'], row['Lon'])] = 1.0 / (dist + 0.1)

    # Normalize weights
    total_weight = sum(weights.values())
    weights = {k: v/total_weight for k, v in weights.items()}

    # Calculate weighted average for each year
    yearly_data = []
    for year in df['Year'].unique():
        year_df = df[df['Year'] == year]
        weighted_pmdi = 0.0
        for _, row in year_df.iterrows():
            w = weights.get((row['Lat'], row['Lon']), 0)
            weighted_pmdi += w * row['PMDI']

        yearly_data.append({
            'year': int(year),
            'pmdi': weighted_pmdi,
            'pmdi_center': float(year_df[
                (year_df['Lat'] == center_lat) &
                (year_df['Lon'] == center_lon)
            ]['PMDI'].values[0]) if len(year_df[
                (year_df['Lat'] == center_lat) &
                (year_df['Lon'] == center_lon)
            ]) > 0 else weighted_pmdi
        })

    return pd.DataFrame(yearly_data).sort_values('year')


def calculate_drought_statistics(df: pd.DataFrame,
                                 drought_threshold: float = -1.0) -> Dict:
    """
    Calculate drought statistics for the Chaco period.

    PMDI scale interpretation:
        >= 4.0: Extremely wet
        3.0 to 3.99: Very wet
        2.0 to 2.99: Moderately wet
        1.0 to 1.99: Slightly wet
        0.5 to 0.99: Incipient wet spell
        -0.49 to 0.49: Near normal
        -0.99 to -0.5: Incipient drought
        -1.99 to -1.0: Mild drought
        -2.99 to -2.0: Moderate drought
        -3.99 to -3.0: Severe drought
        <= -4.0: Extreme drought
    """
    stats = {}

    # Overall statistics
    stats['n_years'] = len(df)
    stats['mean_pmdi'] = float(df['pmdi'].mean())
    stats['std_pmdi'] = float(df['pmdi'].std())
    stats['min_pmdi'] = float(df['pmdi'].min())
    stats['max_pmdi'] = float(df['pmdi'].max())

    # Drought years
    drought_years = df[df['pmdi'] < drought_threshold]
    stats['n_drought_years'] = len(drought_years)
    stats['drought_frequency'] = len(drought_years) / len(df)

    # Severe drought (PMDI < -3)
    severe_drought = df[df['pmdi'] < -3.0]
    stats['n_severe_drought_years'] = len(severe_drought)

    # Extreme drought (PMDI < -4)
    extreme_drought = df[df['pmdi'] < -4.0]
    stats['n_extreme_drought_years'] = len(extreme_drought)
    stats['extreme_drought_years'] = extreme_drought['year'].tolist()

    return stats


def identify_drought_events(df: pd.DataFrame,
                           drought_threshold: float = -1.0) -> pd.DataFrame:
    """
    Identify discrete drought events (consecutive drought years).
    """
    df = df.copy().sort_values('year')
    df['is_drought'] = df['pmdi'] < drought_threshold

    # Find drought events
    events = []
    in_drought = False
    current_event = {}

    for _, row in df.iterrows():
        if row['is_drought'] and not in_drought:
            # Start of drought
            in_drought = True
            current_event = {
                'start_year': row['year'],
                'min_pmdi': row['pmdi'],
                'total_deficit': row['pmdi']
            }
        elif row['is_drought'] and in_drought:
            # Continue drought
            current_event['min_pmdi'] = min(current_event['min_pmdi'], row['pmdi'])
            current_event['total_deficit'] += row['pmdi']
        elif not row['is_drought'] and in_drought:
            # End of drought
            in_drought = False
            current_event['end_year'] = row['year'] - 1
            current_event['duration'] = current_event['end_year'] - current_event['start_year'] + 1
            current_event['mean_pmdi'] = current_event['total_deficit'] / current_event['duration']
            events.append(current_event)

    # Handle drought continuing to end
    if in_drought:
        current_event['end_year'] = df['year'].max()
        current_event['duration'] = current_event['end_year'] - current_event['start_year'] + 1
        current_event['mean_pmdi'] = current_event['total_deficit'] / current_event['duration']
        events.append(current_event)

    return pd.DataFrame(events)


def analyze_periods(df: pd.DataFrame) -> Dict:
    """
    Analyze PMDI statistics for archaeologically significant periods.
    """
    periods = {
        'Pre-Chaco': (500, 800),
        'Early_Chaco': (800, 920),
        'Chaco_Expansion': (920, 1000),
        'Chaco_Florescence': (1000, 1130),
        'Megadrought_Collapse': (1130, 1200),
        'Post-Chaco': (1200, 1500)
    }

    results = {}
    for name, (start, end) in periods.items():
        period_df = df[(df['year'] >= start) & (df['year'] < end)]
        if len(period_df) > 0:
            results[name] = {
                'start_year': start,
                'end_year': end,
                'n_years': len(period_df),
                'mean_pmdi': float(period_df['pmdi'].mean()),
                'std_pmdi': float(period_df['pmdi'].std()),
                'min_pmdi': float(period_df['pmdi'].min()),
                'max_pmdi': float(period_df['pmdi'].max()),
                'n_drought_years': len(period_df[period_df['pmdi'] < -1.0]),
                'n_severe_drought': len(period_df[period_df['pmdi'] < -3.0])
            }

    return results


def calculate_sigma(df: pd.DataFrame, window: int = 100) -> pd.DataFrame:
    """
    Calculate rolling environmental uncertainty parameter (sigma).

    sigma combines:
    - Frequency: how often droughts occur
    - Magnitude: how severe droughts are
    - Duration: how long droughts last

    Formula: sigma = (magnitude * duration) / frequency_interval
    """
    df = df.copy().sort_values('year')

    sigmas = []
    for i in range(window, len(df)):
        window_df = df.iloc[i-window:i]

        # Get drought events in this window
        events = identify_drought_events(window_df)

        if len(events) == 0:
            sigma = 0.0
        else:
            # Calculate components
            n_droughts = len(events)
            frequency_interval = window / n_droughts if n_droughts > 0 else window
            avg_magnitude = abs(events['min_pmdi'].mean()) / 6.0  # Normalize to ~0-1
            avg_duration = events['duration'].mean()

            sigma = (avg_magnitude * avg_duration) / frequency_interval

        sigmas.append({
            'year': df.iloc[i]['year'],
            'sigma': sigma,
            'pmdi': df.iloc[i]['pmdi']
        })

    return pd.DataFrame(sigmas)


def create_simulation_input(df: pd.DataFrame, output_path: Path):
    """
    Create processed PMDI data for direct use by simulation.

    Converts PMDI to productivity multiplier using the formula:
    productivity = base + (pmdi * sensitivity)

    Where:
    - base = 0.7 (marginal baseline for Chaco)
    - sensitivity = 0.05 (scaling factor)
    - Clamped to [0.2, 1.0] range
    """
    output_df = df[['year', 'pmdi']].copy()

    # Parameters for productivity conversion
    base_productivity = 0.7
    pmdi_sensitivity = 0.05
    min_productivity = 0.2
    max_productivity = 1.0

    # Convert PMDI to productivity
    output_df['productivity'] = (
        base_productivity + output_df['pmdi'] * pmdi_sensitivity
    ).clip(min_productivity, max_productivity)

    # Mark drought years (PMDI < -1.0 is mild drought threshold)
    output_df['is_drought'] = output_df['pmdi'] < -1.0

    # Save
    output_df.to_csv(output_path, index=False)
    print(f"Saved simulation input to: {output_path}")

    return output_df


def main():
    """Process LBDA data and generate analysis."""

    # Paths
    raw_dir = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'pdsi_reconstructions'
    processed_dir = Path(__file__).parent.parent.parent / 'data' / 'processed'
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Load regional data
    print("Loading LBDA v2 PMDI data for Chaco region...")
    regional_data = load_chaco_pmdi(raw_dir / 'chaco_region_pmdi_500_1500.csv')
    print(f"  Loaded {len(regional_data)} records")

    # Create spatially-averaged dataset
    print("\nCreating spatially-weighted average...")
    chaco_avg = create_spatial_average(regional_data)
    print(f"  Created {len(chaco_avg)} annual records (500-1500 CE)")

    # Save averaged data
    chaco_avg.to_csv(processed_dir / 'chaco_pmdi_averaged.csv', index=False)

    # Calculate overall statistics
    print("\n" + "="*60)
    print("CHACO CANYON PMDI STATISTICS (500-1500 CE)")
    print("="*60)

    stats = calculate_drought_statistics(chaco_avg)
    print(f"\nOverall Statistics:")
    print(f"  Mean PMDI: {stats['mean_pmdi']:.2f}")
    print(f"  Std PMDI: {stats['std_pmdi']:.2f}")
    print(f"  Range: {stats['min_pmdi']:.2f} to {stats['max_pmdi']:.2f}")
    print(f"  Drought years (PMDI < -1): {stats['n_drought_years']} ({stats['drought_frequency']*100:.1f}%)")
    print(f"  Severe drought years (PMDI < -3): {stats['n_severe_drought_years']}")
    print(f"  Extreme drought years (PMDI < -4): {stats['n_extreme_drought_years']}")
    if stats['extreme_drought_years']:
        print(f"    Years: {stats['extreme_drought_years']}")

    # Period analysis
    print("\n" + "-"*60)
    print("PERIOD ANALYSIS")
    print("-"*60)

    periods = analyze_periods(chaco_avg)
    for name, data in periods.items():
        print(f"\n{name.replace('_', ' ')} ({data['start_year']}-{data['end_year']} CE):")
        print(f"  Mean PMDI: {data['mean_pmdi']:.2f} (±{data['std_pmdi']:.2f})")
        print(f"  Range: {data['min_pmdi']:.2f} to {data['max_pmdi']:.2f}")
        print(f"  Drought years: {data['n_drought_years']}/{data['n_years']}")
        print(f"  Severe drought: {data['n_severe_drought']}")

    # Save period analysis
    with open(processed_dir / 'chaco_period_analysis.json', 'w') as f:
        json.dump(periods, f, indent=2)

    # Identify major drought events
    print("\n" + "-"*60)
    print("MAJOR DROUGHT EVENTS (PMDI < -1.0, duration >= 2 years)")
    print("-"*60)

    drought_events = identify_drought_events(chaco_avg)
    major_events = drought_events[drought_events['duration'] >= 2].sort_values('start_year')

    print(f"\n{'Start':<8} {'End':<8} {'Duration':<10} {'Min PMDI':<10} {'Mean PMDI':<10}")
    print("-" * 48)
    for _, event in major_events.iterrows():
        print(f"{int(event['start_year']):<8} {int(event['end_year']):<8} "
              f"{int(event['duration']):<10} {event['min_pmdi']:<10.2f} {event['mean_pmdi']:<10.2f}")

    # Save drought events
    drought_events.to_csv(processed_dir / 'chaco_drought_events.csv', index=False)

    # Calculate sigma values
    print("\n" + "-"*60)
    print("ENVIRONMENTAL UNCERTAINTY (SIGMA) BY PERIOD")
    print("-"*60)

    sigma_df = calculate_sigma(chaco_avg, window=50)

    # Average sigma by period
    for name, (start, end) in [
        ('Pre-Chaco', (550, 800)),  # Start at 550 to account for window
        ('Early Chaco', (800, 920)),
        ('Chaco Expansion', (920, 1000)),
        ('Chaco Florescence', (1000, 1130)),
        ('Megadrought', (1130, 1200)),
        ('Post-Chaco', (1200, 1450))  # End at 1450 to account for window
    ]:
        period_sigma = sigma_df[(sigma_df['year'] >= start) & (sigma_df['year'] < end)]
        if len(period_sigma) > 0:
            print(f"\n{name} ({start}-{end} CE):")
            print(f"  Mean σ: {period_sigma['sigma'].mean():.4f}")
            print(f"  Max σ: {period_sigma['sigma'].max():.4f}")

    # Save sigma data
    sigma_df.to_csv(processed_dir / 'chaco_sigma_timeseries.csv', index=False)

    # Create simulation input file
    print("\n" + "="*60)
    print("CREATING SIMULATION INPUT")
    print("="*60)

    sim_input = create_simulation_input(chaco_avg, processed_dir / 'chaco_pmdi_simulation_input.csv')

    # Summary statistics for simulation
    print(f"\nProductivity Statistics:")
    print(f"  Mean: {sim_input['productivity'].mean():.3f}")
    print(f"  Std: {sim_input['productivity'].std():.3f}")
    print(f"  Min: {sim_input['productivity'].min():.3f}")
    print(f"  Max: {sim_input['productivity'].max():.3f}")

    # Key droughts
    print("\n" + "-"*60)
    print("KEY DROUGHT EVENTS FOR SIMULATION")
    print("-"*60)

    # Find the worst droughts in the Chaco period
    chaco_period = chaco_avg[(chaco_avg['year'] >= 800) & (chaco_avg['year'] <= 1200)]
    worst_years = chaco_period.nsmallest(10, 'pmdi')

    print(f"\nWorst 10 drought years (800-1200 CE):")
    for _, row in worst_years.iterrows():
        print(f"  {int(row['year'])} CE: PMDI = {row['pmdi']:.2f}")

    # The 1130-1150 megadrought
    megadrought = chaco_avg[(chaco_avg['year'] >= 1130) & (chaco_avg['year'] <= 1150)]
    print(f"\nMid-12th century megadrought (1130-1150 CE):")
    print(f"  Mean PMDI: {megadrought['pmdi'].mean():.2f}")
    print(f"  Min PMDI: {megadrought['pmdi'].min():.2f}")
    print(f"  Drought years: {len(megadrought[megadrought['pmdi'] < -1.0])}/21")

    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    print(f"\nOutput files in {processed_dir}:")
    print("  - chaco_pmdi_averaged.csv (annual PMDI values)")
    print("  - chaco_period_analysis.json (period statistics)")
    print("  - chaco_drought_events.csv (drought event catalog)")
    print("  - chaco_sigma_timeseries.csv (uncertainty parameter)")
    print("  - chaco_pmdi_simulation_input.csv (simulation-ready)")


if __name__ == '__main__':
    main()
