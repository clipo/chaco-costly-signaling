"""
Spatial structure for Chaco Canyon simulation.

Implements hierarchical network: Core canyon great houses + outlier communities.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import numpy as np


class GreatHouseType(Enum):
    """Types of great houses."""
    CORE = "core"       # Canyon great houses (Pueblo Bonito, Chetro Ketl, etc.)
    OUTLIER = "outlier"  # Regional outlier great houses


@dataclass
class GreatHouse:
    """
    Represents a great house community.

    Attributes:
        name: Name of the great house
        house_type: Core or outlier
        location: (x, y) coordinates
        founding_year: Year construction began
        rooms: Number of rooms (proxy for size/investment)
        population: Current population
        elite_count: Number of elite individuals
        monument_investment: Cumulative construction investment
        exotic_goods: Count of exotic items (turquoise, macaws, etc.)
    """
    name: str
    house_type: GreatHouseType
    location: tuple
    founding_year: int = 850

    # Size and population
    rooms: int = 50
    population: int = 100
    elite_count: int = 5

    # Signaling investments
    monument_investment: float = 0.0
    exotic_goods: int = 0

    # Strategy parameters
    monument_investment_rate: float = 0.35  # Fraction of productivity to monuments
    exotic_acquisition_rate: float = 0.10   # Fraction to exotic goods


@dataclass
class OutlierNetwork:
    """
    Network of outlier great houses connected to core.

    Attributes:
        outliers: List of outlier great houses
        connections: Dict mapping outlier name to connected core houses
    """
    outliers: List[GreatHouse] = field(default_factory=list)
    connections: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class SpatialConfig:
    """Configuration for spatial structure."""

    # Canyon dimensions (arbitrary units)
    canyon_length: float = 20.0
    canyon_width: float = 5.0

    # Core great houses (based on archaeological data)
    core_houses: List[Dict] = field(default_factory=lambda: [
        {
            'name': 'Pueblo Bonito',
            'location': (10, 2.5),
            'founding_year': 850,
            'rooms': 350,
        },
        {
            'name': 'Chetro Ketl',
            'location': (12, 2.5),
            'founding_year': 990,
            'rooms': 300,
        },
        {
            'name': 'Pueblo del Arroyo',
            'location': (8, 2.5),
            'founding_year': 1075,
            'rooms': 280,
        },
        {
            'name': 'Pueblo Alto',
            'location': (10, 4.5),
            'founding_year': 1020,
            'rooms': 130,
        },
        {
            'name': 'Kin Kletso',
            'location': (7, 2.5),
            'founding_year': 1125,
            'rooms': 100,
        },
    ])

    # Number of outlier communities to generate
    n_outliers: int = 30

    # Outlier distance range from canyon center
    outlier_min_distance: float = 30.0
    outlier_max_distance: float = 150.0


class ChacoSpatialStructure:
    """
    Spatial structure of the Chaco system.

    Implements the core canyon + outlier network architecture.
    """

    def __init__(self, config: Optional[SpatialConfig] = None):
        """
        Initialize spatial structure.

        Args:
            config: Spatial configuration
        """
        self.config = config or SpatialConfig()

        # Initialize core great houses
        self.core_houses: Dict[str, GreatHouse] = {}
        self._initialize_core_houses()

        # Initialize outlier network
        self.outlier_network = OutlierNetwork()
        self._initialize_outliers()

    def _initialize_core_houses(self):
        """Create core great house objects."""
        for house_data in self.config.core_houses:
            house = GreatHouse(
                name=house_data['name'],
                house_type=GreatHouseType.CORE,
                location=house_data['location'],
                founding_year=house_data['founding_year'],
                rooms=house_data['rooms'],
                population=house_data['rooms'] * 2,  # Rough estimate
                elite_count=max(5, house_data['rooms'] // 50),
            )
            self.core_houses[house.name] = house

    def _initialize_outliers(self):
        """Generate outlier great house communities."""
        np.random.seed(123)

        canyon_center = (
            self.config.canyon_length / 2,
            self.config.canyon_width / 2
        )

        for i in range(self.config.n_outliers):
            # Random angle and distance
            angle = np.random.uniform(0, 2 * np.pi)
            distance = np.random.uniform(
                self.config.outlier_min_distance,
                self.config.outlier_max_distance
            )

            # Calculate position
            x = canyon_center[0] + distance * np.cos(angle)
            y = canyon_center[1] + distance * np.sin(angle)

            # Outliers are smaller than core houses
            rooms = np.random.randint(15, 50)

            outlier = GreatHouse(
                name=f"Outlier_{i+1}",
                house_type=GreatHouseType.OUTLIER,
                location=(x, y),
                founding_year=np.random.randint(900, 1100),
                rooms=rooms,
                population=rooms * 3,  # Higher density in outliers
                elite_count=max(1, rooms // 20),
                monument_investment_rate=0.20,  # Lower than core
            )

            self.outlier_network.outliers.append(outlier)

            # Connect to nearest core house
            nearest_core = self._find_nearest_core(outlier.location)
            if nearest_core:
                if outlier.name not in self.outlier_network.connections:
                    self.outlier_network.connections[outlier.name] = []
                self.outlier_network.connections[outlier.name].append(
                    nearest_core
                )

    def _find_nearest_core(self, location: tuple) -> Optional[str]:
        """Find the nearest core great house to a location."""
        min_dist = float('inf')
        nearest = None

        for name, house in self.core_houses.items():
            dist = np.sqrt(
                (location[0] - house.location[0])**2 +
                (location[1] - house.location[1])**2
            )
            if dist < min_dist:
                min_dist = dist
                nearest = name

        return nearest

    def get_all_houses(self) -> List[GreatHouse]:
        """Get all great houses (core + outliers)."""
        return list(self.core_houses.values()) + self.outlier_network.outliers

    def get_core_houses(self) -> List[GreatHouse]:
        """Get only core canyon great houses."""
        return list(self.core_houses.values())

    def get_outliers(self) -> List[GreatHouse]:
        """Get only outlier great houses."""
        return self.outlier_network.outliers

    def get_total_population(self) -> int:
        """Get total population across all great houses."""
        return sum(h.population for h in self.get_all_houses())

    def get_total_monument_investment(self) -> float:
        """Get total monument investment across all great houses."""
        return sum(h.monument_investment for h in self.get_all_houses())

    def get_active_houses(self, year: int) -> List[GreatHouse]:
        """Get great houses that were founded by a given year."""
        return [h for h in self.get_all_houses() if h.founding_year <= year]

    def distance_between(self, house1: str, house2: str) -> float:
        """Calculate distance between two great houses."""
        h1 = self.core_houses.get(house1)
        h2 = self.core_houses.get(house2)

        if h1 is None:
            h1 = next(
                (o for o in self.outlier_network.outliers if o.name == house1),
                None
            )
        if h2 is None:
            h2 = next(
                (o for o in self.outlier_network.outliers if o.name == house2),
                None
            )

        if h1 is None or h2 is None:
            return float('inf')

        return np.sqrt(
            (h1.location[0] - h2.location[0])**2 +
            (h1.location[1] - h2.location[1])**2
        )
