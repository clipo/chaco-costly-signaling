"""
Environmental dynamics for Chaco Canyon simulation.

Uses PDSI (Palmer Drought Severity Index) reconstructions from the
North American Drought Atlas to model environmental variability.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class EnvironmentConfig:
    """Configuration for environmental parameters."""

    # Time range (CE years)
    start_year: int = 800
    end_year: int = 1200

    # Base productivity (relative to optimal = 1.0)
    base_productivity: float = 0.7  # Marginal agricultural environment

    # PDSI-productivity conversion
    # PDSI typically ranges from -6 (extreme drought) to +6 (extreme wet)
    # We convert to productivity multiplier
    pdsi_sensitivity: float = 0.1  # Productivity change per PDSI unit

    # Minimum productivity floor
    min_productivity: float = 0.2

    # Carrying capacity per cell
    base_carrying_capacity: int = 10


class Environment:
    """
    Environmental model for Chaco Canyon based on PDSI reconstructions.

    Attributes:
        config: Environmental configuration
        pdsi_data: Array of annual PDSI values
        years: Array of corresponding years
    """

    def __init__(
        self,
        config: Optional[EnvironmentConfig] = None,
        pdsi_data: Optional[np.ndarray] = None,
        years: Optional[np.ndarray] = None
    ):
        """
        Initialize environment.

        Args:
            config: Environmental configuration
            pdsi_data: Pre-loaded PDSI data (if None, will generate synthetic)
            years: Years corresponding to PDSI data
        """
        self.config = config or EnvironmentConfig()

        if pdsi_data is not None and years is not None:
            self.pdsi_data = pdsi_data
            self.years = years
        else:
            # Generate synthetic PDSI for testing
            self._generate_synthetic_pdsi()

    def _generate_synthetic_pdsi(self):
        """Generate synthetic PDSI data matching Chaco patterns."""
        n_years = self.config.end_year - self.config.start_year
        self.years = np.arange(self.config.start_year, self.config.end_year)

        # Base random variability
        np.random.seed(42)  # Reproducibility
        base_pdsi = np.random.normal(0, 1.5, n_years)

        # Add ENSO-like cycles (~7 year periodicity)
        enso_cycle = 1.5 * np.sin(2 * np.pi * np.arange(n_years) / 7)

        # Add longer-term trends
        # Favorable period ~1000-1100, then megadrought ~1130-1150
        trend = np.zeros(n_years)
        for i, year in enumerate(self.years):
            if 1000 <= year <= 1100:
                trend[i] = 0.5  # Slightly favorable
            elif 1130 <= year <= 1180:
                trend[i] = -2.5  # Megadrought

        self.pdsi_data = base_pdsi + enso_cycle + trend

        # Clip to realistic range
        self.pdsi_data = np.clip(self.pdsi_data, -6, 6)

    def get_pdsi(self, year: int) -> float:
        """
        Get PDSI value for a given year.

        Args:
            year: Year (CE)

        Returns:
            PDSI value for that year
        """
        if year < self.years[0] or year >= self.years[-1]:
            return 0.0  # Default neutral

        idx = year - self.years[0]
        return self.pdsi_data[idx]

    def get_productivity(self, year: int) -> float:
        """
        Convert PDSI to productivity multiplier.

        Args:
            year: Year (CE)

        Returns:
            Productivity multiplier (0 to ~1.5)
        """
        pdsi = self.get_pdsi(year)

        # Convert PDSI to productivity
        # Positive PDSI = wet = higher productivity
        # Negative PDSI = drought = lower productivity
        productivity = self.config.base_productivity + (
            pdsi * self.config.pdsi_sensitivity
        )

        # Apply floor
        return max(self.config.min_productivity, productivity)

    def is_drought(self, year: int, threshold: float = -1.5) -> bool:
        """
        Check if a year is a drought year.

        Args:
            year: Year (CE)
            threshold: PDSI threshold for drought (default -1.5)

        Returns:
            True if drought conditions
        """
        return self.get_pdsi(year) < threshold

    def calculate_sigma(
        self,
        start_year: int,
        end_year: int,
        drought_threshold: float = -1.5
    ) -> float:
        """
        Calculate environmental uncertainty parameter sigma.

        sigma = (magnitude * duration) / frequency

        Args:
            start_year: Start of period
            end_year: End of period
            drought_threshold: PDSI threshold for drought

        Returns:
            Sigma value for the period
        """
        years = range(start_year, end_year)

        # Find drought events
        in_drought = False
        drought_events = []
        current_drought = {'start': None, 'min_pdsi': 0}

        for year in years:
            pdsi = self.get_pdsi(year)
            is_drought = pdsi < drought_threshold

            if is_drought and not in_drought:
                # Starting new drought
                in_drought = True
                current_drought = {'start': year, 'min_pdsi': pdsi}
            elif is_drought and in_drought:
                # Continuing drought
                current_drought['min_pdsi'] = min(
                    current_drought['min_pdsi'], pdsi
                )
            elif not is_drought and in_drought:
                # Ending drought
                in_drought = False
                current_drought['end'] = year
                current_drought['duration'] = (
                    year - current_drought['start']
                )
                drought_events.append(current_drought)

        if not drought_events:
            return 0.0

        # Calculate average characteristics
        n_droughts = len(drought_events)
        total_years = end_year - start_year
        frequency = total_years / n_droughts if n_droughts > 0 else total_years

        avg_magnitude = np.mean([
            abs(d['min_pdsi']) / 6.0  # Normalize to 0-1
            for d in drought_events
        ])
        avg_duration = np.mean([d['duration'] for d in drought_events])

        sigma = (avg_magnitude * avg_duration) / frequency
        return sigma


def load_pdsi_from_file(filepath: str) -> tuple:
    """
    Load PDSI data from CSV file.

    Expected format: year,pdsi columns

    Args:
        filepath: Path to CSV file

    Returns:
        Tuple of (years array, pdsi array)
    """
    import pandas as pd

    df = pd.read_csv(filepath)
    years = df['year'].values
    pdsi = df['pdsi'].values

    return years, pdsi
