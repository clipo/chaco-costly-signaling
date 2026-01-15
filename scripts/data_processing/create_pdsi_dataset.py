"""
Create PDSI dataset for Chaco Canyon region.

This script creates a PDSI reconstruction dataset for the Chaco Canyon area
(~36°N, 108°W) based on published drought atlas data and known drought events.

The data is derived from:
- Cook et al. 2004, 2007 North American Drought Atlas
- Cook et al. 2010 Living Blended Drought Atlas (LBDA)
- Published analyses of Chaco-period droughts

Key drought events documented in the literature:
- Mid-12th century megadrought (~1130-1180 CE) - severe, multi-decadal
- Late 11th century dry period (~1090-1100 CE) - moderate
- Early 10th century favorable period (~900-1000 CE) - relatively wet
- Mid-9th century drought (~850-870 CE) - moderate

To obtain actual gridded PDSI data:
1. Visit http://drought.memphis.edu/NADA/
2. Select grid point near 36°N, 108°W
3. Export time series as CSV
4. Replace synthetic data with actual values

Alternatively, download from NOAA NCEI:
https://www.ncei.noaa.gov/products/paleoclimatology/drought-variability
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_synthetic_pdsi(start_year: int = 500, end_year: int = 1500) -> pd.DataFrame:
    """
    Generate synthetic PDSI data matching documented Chaco-period patterns.

    This synthetic data incorporates:
    1. Random inter-annual variability (sd ~1.5)
    2. ENSO-like ~7-year cycles
    3. Multi-decadal oscillations (~30-50 year cycles)
    4. Known drought events from paleoclimate literature

    Args:
        start_year: Start year (CE)
        end_year: End year (CE)

    Returns:
        DataFrame with year and pdsi columns
    """
    np.random.seed(42)  # Reproducibility

    years = np.arange(start_year, end_year)
    n_years = len(years)

    # Component 1: Random variability (white noise)
    noise = np.random.normal(0, 1.0, n_years)

    # Component 2: ENSO-like cycles (~7 year period)
    # ENSO affects Chaco through Pacific teleconnections
    enso = 0.8 * np.sin(2 * np.pi * np.arange(n_years) / 7 + np.random.uniform(0, 2*np.pi))

    # Component 3: Multi-decadal oscillation (~35 year period)
    # Represents Pacific Decadal Oscillation influence
    pdo = 0.5 * np.sin(2 * np.pi * np.arange(n_years) / 35 + np.random.uniform(0, 2*np.pi))

    # Component 4: Century-scale trends
    century = 0.3 * np.sin(2 * np.pi * np.arange(n_years) / 100 + np.random.uniform(0, 2*np.pi))

    # Combine components
    pdsi = noise + enso + pdo + century

    # Apply documented drought events
    for i, year in enumerate(years):
        # Mid-12th century megadrought (well-documented)
        if 1130 <= year <= 1180:
            # Severe and prolonged
            drought_intensity = -2.5 - 0.5 * np.sin(2 * np.pi * (year - 1130) / 25)
            pdsi[i] += drought_intensity

        # Late 11th century dry period
        elif 1090 <= year <= 1105:
            pdsi[i] -= 1.2

        # Chaco florescence favorable period
        elif 1020 <= year <= 1080:
            # Relatively favorable but still variable
            pdsi[i] += 0.4

        # Early construction period - variable
        elif 850 <= year <= 900:
            pdsi[i] -= 0.3  # Slightly dry

        # Post-abandonment recovery
        elif 1200 <= year <= 1250:
            pdsi[i] += 0.5

        # 13th century droughts (Mesa Verde era)
        elif 1270 <= year <= 1300:
            pdsi[i] -= 2.0

    # Clip to realistic PDSI range (-6 to +6)
    pdsi = np.clip(pdsi, -6, 6)

    # Create DataFrame
    df = pd.DataFrame({
        'year': years,
        'pdsi': pdsi.round(2)
    })

    return df


def identify_drought_events(df: pd.DataFrame, threshold: float = -1.5) -> pd.DataFrame:
    """
    Identify drought events in PDSI time series.

    Args:
        df: DataFrame with year and pdsi columns
        threshold: PDSI threshold for drought

    Returns:
        DataFrame of drought events with start, end, duration, severity
    """
    events = []
    in_drought = False
    current_event = {}

    for _, row in df.iterrows():
        year = row['year']
        pdsi = row['pdsi']

        if pdsi < threshold and not in_drought:
            # Starting new drought
            in_drought = True
            current_event = {
                'start_year': year,
                'min_pdsi': pdsi,
                'total_deficit': pdsi - threshold
            }
        elif pdsi < threshold and in_drought:
            # Continuing drought
            current_event['min_pdsi'] = min(current_event['min_pdsi'], pdsi)
            current_event['total_deficit'] += pdsi - threshold
        elif pdsi >= threshold and in_drought:
            # Ending drought
            in_drought = False
            current_event['end_year'] = year - 1
            current_event['duration'] = (
                current_event['end_year'] - current_event['start_year'] + 1
            )
            events.append(current_event)

    return pd.DataFrame(events)


def calculate_period_statistics(
    df: pd.DataFrame,
    start_year: int,
    end_year: int
) -> dict:
    """
    Calculate drought statistics for a time period.

    Args:
        df: DataFrame with year and pdsi columns
        start_year: Period start
        end_year: Period end

    Returns:
        Dictionary with drought frequency, mean magnitude, etc.
    """
    period_data = df[(df['year'] >= start_year) & (df['year'] < end_year)]

    droughts = identify_drought_events(period_data)
    n_droughts = len(droughts)
    period_length = end_year - start_year

    stats = {
        'period': f"{start_year}-{end_year}",
        'mean_pdsi': period_data['pdsi'].mean(),
        'std_pdsi': period_data['pdsi'].std(),
        'min_pdsi': period_data['pdsi'].min(),
        'n_droughts': n_droughts,
        'drought_frequency': period_length / n_droughts if n_droughts > 0 else None,
        'mean_duration': droughts['duration'].mean() if n_droughts > 0 else 0,
        'mean_severity': abs(droughts['min_pdsi'].mean()) if n_droughts > 0 else 0,
    }

    # Calculate sigma (environmental uncertainty parameter)
    if n_droughts > 0 and stats['drought_frequency']:
        magnitude = stats['mean_severity'] / 6.0  # Normalize to 0-1
        stats['sigma'] = (magnitude * stats['mean_duration']) / stats['drought_frequency']
    else:
        stats['sigma'] = 0

    return stats


def main():
    """Generate PDSI dataset and save to file."""

    # Output directory
    output_dir = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'pdsi_reconstructions'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate data
    print("Generating synthetic PDSI data for Chaco Canyon region...")
    df = generate_synthetic_pdsi(500, 1500)

    # Save full dataset
    output_file = output_dir / 'pdsi_chaco_500_1500_synthetic.csv'
    df.to_csv(output_file, index=False)
    print(f"Saved PDSI data to: {output_file}")

    # Identify drought events
    print("\nIdentifying drought events...")
    droughts = identify_drought_events(df)
    drought_file = output_dir / 'drought_events_synthetic.csv'
    droughts.to_csv(drought_file, index=False)
    print(f"Saved drought events to: {drought_file}")
    print(f"Total drought events identified: {len(droughts)}")

    # Calculate statistics for key periods
    print("\nPeriod Statistics:")
    print("-" * 80)

    periods = [
        (800, 900, "Pre-Chaco"),
        (900, 1000, "Early Chaco"),
        (1000, 1100, "Peak Chaco"),
        (1100, 1200, "Late Chaco/Collapse"),
        (1200, 1300, "Post-Chaco"),
    ]

    stats_list = []
    for start, end, name in periods:
        stats = calculate_period_statistics(df, start, end)
        stats['period_name'] = name
        stats_list.append(stats)
        print(f"\n{name} ({start}-{end} CE):")
        print(f"  Mean PDSI: {stats['mean_pdsi']:.2f}")
        print(f"  Drought frequency: {stats['drought_frequency']:.1f} years" if stats['drought_frequency'] else "  No droughts")
        print(f"  Mean drought duration: {stats['mean_duration']:.1f} years")
        print(f"  Sigma (uncertainty): {stats['sigma']:.3f}")

    # Save statistics
    stats_df = pd.DataFrame(stats_list)
    stats_file = output_dir / 'period_statistics_synthetic.csv'
    stats_df.to_csv(stats_file, index=False)
    print(f"\nSaved period statistics to: {stats_file}")

    # Note about real data
    print("\n" + "=" * 80)
    print("NOTE: This is SYNTHETIC data based on published drought patterns.")
    print("For actual research, download real PDSI reconstructions from:")
    print("  - http://drought.memphis.edu/NADA/")
    print("  - https://www.ncei.noaa.gov/products/paleoclimatology/drought-variability")
    print("=" * 80)


if __name__ == '__main__':
    main()
