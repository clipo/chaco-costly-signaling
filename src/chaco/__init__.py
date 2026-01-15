"""
Chaco Canyon Costly Signaling Model

An agent-based model testing multi-scale costly signaling under environmental
uncertainty at Chaco Canyon (850-1150 CE).

Modules:
    simulation: Core ABM simulation engine
    environment: PDSI-based environmental dynamics
    spatial: Core-outlier network structure
    analysis: Correlation and statistical analyses
"""

__version__ = "0.1.0"
__author__ = "Carl Lipo"

from .environment import Environment, EnvironmentConfig
from .spatial import ChacoSpatialStructure, SpatialConfig, GreatHouse, GreatHouseType
from .simulation import ChacoSimulation, SimulationConfig, Strategy, GroupState
from .analysis import (
    history_to_dataframe,
    generate_summary_report,
    calculate_construction_climate_correlation,
    calculate_exotic_stress_correlation,
    compare_strategies,
    analyze_period
)

__all__ = [
    'Environment',
    'EnvironmentConfig',
    'ChacoSpatialStructure',
    'SpatialConfig',
    'GreatHouse',
    'GreatHouseType',
    'ChacoSimulation',
    'SimulationConfig',
    'Strategy',
    'GroupState',
    'history_to_dataframe',
    'generate_summary_report',
    'calculate_construction_climate_correlation',
    'calculate_exotic_stress_correlation',
    'compare_strategies',
    'analyze_period',
]
