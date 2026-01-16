"""
Environmental dynamics for Chaco Canyon simulation.

Uses PMDI (Palmer Modified Drought Index) reconstructions from the
Living Blended Drought Atlas (LBDA) Version 2 to model environmental variability.

Data source:
    Gille, E.P., C.S. Wahl, T.M. Vose, and E.R. Cook. 2017.
    Living Blended Drought Atlas (LBDA) Version 2 - Recalibrated reconstruction of
    United States Summer PMDI over the last 2000 years.
    NOAA/NCEI https://doi.org/10.25921/7xm8-jn36

Grid point: 36.25°N, 108.25°W (closest to Chaco Canyon at 36.06°N, 107.96°W)
Resolution: 0.5° x 0.5° gridded PMDI
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from pathlib import Path


@dataclass
class EnvironmentConfig:
    """Configuration for environmental parameters."""

    # Time range (CE years)
    start_year: int = 500
    end_year: int = 1500

    # Base productivity (relative to optimal = 1.0)
    base_productivity: float = 0.7  # Marginal agricultural environment

    # PMDI-productivity conversion
    # PMDI typically ranges from -6 (extreme drought) to +6 (extreme wet)
    # We convert to productivity multiplier
    pmdi_sensitivity: float = 0.05  # Productivity change per PMDI unit

    # Minimum and maximum productivity bounds
    min_productivity: float = 0.2
    max_productivity: float = 1.0

    # Drought threshold (PMDI values below this are drought)
    drought_threshold: float = -1.0

    # Carrying capacity per cell
    base_carrying_capacity: int = 10

    # Path to real PMDI data (if None, uses synthetic)
    pmdi_data_path: Optional[str] = None


class Environment:
    """
    Environmental model for Chaco Canyon based on PMDI reconstructions.

    Uses real paleoclimate data from the Living Blended Drought Atlas (LBDA) v2
    when available, falling back to synthetic data for testing.

    Attributes:
        config: Environmental configuration
        pmdi_data: Dictionary mapping year to PMDI value
        years: Sorted list of available years
    """

    def __init__(
        self,
        config: Optional[EnvironmentConfig] = None,
        pmdi_data: Optional[np.ndarray] = None,
        years: Optional[np.ndarray] = None
    ):
        """
        Initialize environment.

        Args:
            config: Environmental configuration
            pmdi_data: Pre-loaded PMDI data array (if None, will load from file or generate synthetic)
            years: Years corresponding to PMDI data
        """
        self.config = config or EnvironmentConfig()
        self.pmdi_dict: dict = {}

        if pmdi_data is not None and years is not None:
            # Use provided arrays
            for y, p in zip(years, pmdi_data):
                self.pmdi_dict[int(y)] = float(p)
            self.years = sorted(self.pmdi_dict.keys())
        elif self.config.pmdi_data_path:
            # Load from file
            self._load_pmdi_from_file(self.config.pmdi_data_path)
        else:
            # Try to load real data from default location, fall back to synthetic
            self._try_load_real_data()

    def _try_load_real_data(self):
        """Try to load real PMDI data, fall back to synthetic if not found."""
        # Try to find the processed data file
        possible_paths = [
            Path(__file__).parent.parent.parent / 'data' / 'processed' / 'chaco_pmdi_simulation_input.csv',
            Path(__file__).parent.parent.parent / 'data' / 'processed' / 'chaco_pmdi_averaged.csv',
        ]

        for path in possible_paths:
            if path.exists():
                self._load_pmdi_from_file(str(path))
                return

        # Fall back to synthetic data
        self._generate_synthetic_pmdi()

    def _load_pmdi_from_file(self, filepath: str):
        """Load PMDI data from CSV file."""
        df = pd.read_csv(filepath)

        # Handle different column names
        year_col = 'year' if 'year' in df.columns else 'Year'
        pmdi_col = 'pmdi' if 'pmdi' in df.columns else 'PMDI'

        for _, row in df.iterrows():
            year = int(row[year_col])
            pmdi = float(row[pmdi_col])
            self.pmdi_dict[year] = pmdi

        self.years = sorted(self.pmdi_dict.keys())

    def _generate_synthetic_pmdi(self):
        """Generate synthetic PMDI data matching Chaco patterns."""
        n_years = self.config.end_year - self.config.start_year
        year_array = np.arange(self.config.start_year, self.config.end_year)

        # Base random variability
        np.random.seed(42)  # Reproducibility
        base_pmdi = np.random.normal(0, 2.0, n_years)

        # Add ENSO-like cycles (~7 year periodicity)
        enso_cycle = 1.5 * np.sin(2 * np.pi * np.arange(n_years) / 7)

        # Add longer-term trends based on real patterns
        trend = np.zeros(n_years)
        for i, year in enumerate(year_array):
            if 1000 <= year <= 1100:
                trend[i] = 0.3  # Slightly favorable during florescence
            elif 1130 <= year <= 1180:
                trend[i] = -1.5  # Megadrought period

        pmdi_values = base_pmdi + enso_cycle + trend
        pmdi_values = np.clip(pmdi_values, -6, 6)

        for y, p in zip(year_array, pmdi_values):
            self.pmdi_dict[int(y)] = float(p)

        self.years = sorted(self.pmdi_dict.keys())

    def get_pmdi(self, year: int) -> float:
        """
        Get PMDI value for a given year.

        Args:
            year: Year (CE)

        Returns:
            PMDI value for that year
        """
        return self.pmdi_dict.get(year, 0.0)

    # Alias for backwards compatibility
    def get_pdsi(self, year: int) -> float:
        """Alias for get_pmdi (PDSI and PMDI are similar indices)."""
        return self.get_pmdi(year)

    def get_productivity(self, year: int) -> float:
        """
        Convert PMDI to productivity multiplier.

        Args:
            year: Year (CE)

        Returns:
            Productivity multiplier (min_productivity to max_productivity)
        """
        pmdi = self.get_pmdi(year)

        # Convert PMDI to productivity
        # Positive PMDI = wet = higher productivity
        # Negative PMDI = drought = lower productivity
        productivity = self.config.base_productivity + (
            pmdi * self.config.pmdi_sensitivity
        )

        # Clamp to bounds
        return max(self.config.min_productivity,
                   min(self.config.max_productivity, productivity))

    def is_drought(self, year: int, threshold: Optional[float] = None) -> bool:
        """
        Check if a year is a drought year.

        Args:
            year: Year (CE)
            threshold: PMDI threshold for drought (uses config default if None)

        Returns:
            True if drought conditions
        """
        if threshold is None:
            threshold = self.config.drought_threshold
        return self.get_pmdi(year) < threshold

    def get_drought_events(
        self,
        start_year: int,
        end_year: int,
        threshold: Optional[float] = None
    ) -> list:
        """
        Get list of drought events in a time range.

        Returns:
            List of dicts with start_year, end_year, duration, min_pmdi, mean_pmdi
        """
        if threshold is None:
            threshold = self.config.drought_threshold

        events = []
        in_drought = False
        current: dict = {}

        for year in range(start_year, end_year + 1):
            pmdi = self.get_pmdi(year)
            is_drought_year = pmdi < threshold

            if is_drought_year and not in_drought:
                in_drought = True
                current = {
                    'start_year': year,
                    'min_pmdi': pmdi,
                    'total_pmdi': pmdi
                }
            elif is_drought_year and in_drought:
                current['min_pmdi'] = min(current['min_pmdi'], pmdi)
                current['total_pmdi'] += pmdi
            elif not is_drought_year and in_drought:
                in_drought = False
                current['end_year'] = year - 1
                current['duration'] = current['end_year'] - current['start_year'] + 1
                current['mean_pmdi'] = current['total_pmdi'] / current['duration']
                del current['total_pmdi']
                events.append(current)

        # Handle drought at end of range
        if in_drought:
            current['end_year'] = end_year
            current['duration'] = current['end_year'] - current['start_year'] + 1
            current['mean_pmdi'] = current['total_pmdi'] / current['duration']
            del current['total_pmdi']
            events.append(current)

        return events

    def calculate_sigma(
        self,
        start_year: int,
        end_year: int,
        drought_threshold: Optional[float] = None
    ) -> float:
        """
        Calculate environmental uncertainty parameter sigma.

        sigma = (magnitude * duration) / frequency_interval

        Higher sigma indicates more severe environmental uncertainty.

        Args:
            start_year: Start of period
            end_year: End of period
            drought_threshold: PMDI threshold for drought (uses config default if None)

        Returns:
            Sigma value for the period
        """
        if drought_threshold is None:
            drought_threshold = self.config.drought_threshold

        drought_events = self.get_drought_events(start_year, end_year, drought_threshold)

        if not drought_events:
            return 0.0

        n_droughts = len(drought_events)
        total_years = end_year - start_year

        # Frequency interval (years between droughts on average)
        frequency_interval = total_years / n_droughts if n_droughts > 0 else total_years

        # Average magnitude (normalized to 0-1 scale)
        avg_magnitude = np.mean([
            abs(d['min_pmdi']) / 6.0
            for d in drought_events
        ])

        # Average duration
        avg_duration = np.mean([d['duration'] for d in drought_events])

        sigma = float((avg_magnitude * avg_duration) / frequency_interval)
        return sigma

    def get_period_statistics(self, start_year: int, end_year: int) -> dict:
        """
        Calculate statistics for a time period.

        Returns:
            Dict with mean_pmdi, std_pmdi, min_pmdi, max_pmdi, n_drought_years, sigma
        """
        pmdi_values = [
            self.get_pmdi(y)
            for y in range(start_year, end_year + 1)
            if y in self.pmdi_dict
        ]

        if not pmdi_values:
            return {}

        drought_years = sum(
            1 for p in pmdi_values
            if p < self.config.drought_threshold
        )

        return {
            'start_year': start_year,
            'end_year': end_year,
            'n_years': len(pmdi_values),
            'mean_pmdi': float(np.mean(pmdi_values)),
            'std_pmdi': float(np.std(pmdi_values)),
            'min_pmdi': float(np.min(pmdi_values)),
            'max_pmdi': float(np.max(pmdi_values)),
            'n_drought_years': drought_years,
            'drought_frequency': drought_years / len(pmdi_values),
            'sigma': self.calculate_sigma(start_year, end_year)
        }


def load_real_pmdi_environment(
    start_year: int = 500,
    end_year: int = 1500
) -> Environment:
    """
    Factory function to create Environment with real LBDA PMDI data.

    Args:
        start_year: Start year for simulation
        end_year: End year for simulation

    Returns:
        Environment configured with real paleoclimate data
    """
    config = EnvironmentConfig(
        start_year=start_year,
        end_year=end_year,
        base_productivity=0.7,
        pmdi_sensitivity=0.05,
        min_productivity=0.2,
        max_productivity=1.0,
        drought_threshold=-1.0
    )

    return Environment(config)


def load_pmdi_from_file(filepath: str) -> tuple:
    """
    Load PMDI data from CSV file.

    Expected format: year,pmdi columns

    Args:
        filepath: Path to CSV file

    Returns:
        Tuple of (years array, pmdi array)
    """
    df = pd.read_csv(filepath)

    year_col = 'year' if 'year' in df.columns else 'Year'
    pmdi_col = 'pmdi' if 'pmdi' in df.columns else 'PMDI'

    years = df[year_col].values
    pmdi = df[pmdi_col].values

    return years, pmdi
