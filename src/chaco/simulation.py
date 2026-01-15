"""
Core simulation engine for Chaco Canyon costly signaling model.

Implements a hybrid multi-scale model with:
1. Group-level signaling through monument construction (great houses)
2. Individual-level signaling through exotic goods acquisition (elites)
3. Environmental uncertainty from PDSI-based drought dynamics
4. Core-outlier network spatial structure
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

from .environment import Environment, EnvironmentConfig
from .spatial import (
    ChacoSpatialStructure,
    SpatialConfig,
    GreatHouse,
    GreatHouseType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Strategy(Enum):
    """Signaling strategies for great house communities."""
    MONUMENT_BUILDER = "monument_builder"  # High monument investment
    BALANCED = "balanced"                   # Moderate investment in both
    REPRODUCTION_FOCUSED = "reproduction"   # Minimize signaling, maximize growth


@dataclass
class SimulationConfig:
    """Configuration for simulation parameters."""

    # Time parameters
    start_year: int = 800
    end_year: int = 1200

    # Population parameters
    base_birth_rate: float = 0.04          # Annual births per capita
    base_death_rate: float = 0.03          # Annual deaths per capita
    starvation_death_rate: float = 0.15    # Additional mortality during shortfall
    conflict_death_rate: float = 0.05      # Mortality from conflicts

    # Carrying capacity
    base_carrying_capacity: int = 3000     # Canyon-wide carrying capacity
    density_dependence: float = 0.5        # Strength of density effects

    # Signaling parameters - Group level (monuments)
    monument_investment_rate: float = 0.35  # Fraction of productivity to monuments
    monument_conflict_reduction: float = 0.75  # Conflict reduction from mutual signaling
    monument_decay_rate: float = 0.01       # Annual decay of monument investment

    # Signaling parameters - Individual level (exotic goods)
    exotic_investment_rate: float = 0.10    # Fraction to exotic goods
    exotic_status_benefit: float = 0.20     # Reproductive advantage for elites
    exotic_acquisition_cost: float = 0.05   # Mortality risk from long-distance travel

    # Conflict parameters
    base_conflict_rate: float = 0.10        # Annual probability of inter-group conflict
    conflict_intensity: float = 0.30        # Proportion of combatants killed
    territory_value: float = 1.0            # Value of territory in conflicts

    # Pilgrimage dynamics
    enable_pilgrimage: bool = True
    pilgrimage_rate: float = 0.10           # Fraction of regional pop visiting annually
    pilgrimage_labor_contribution: float = 0.05  # Labor contributed by pilgrims

    # Random seed
    seed: Optional[int] = 42


@dataclass
class GroupState:
    """State of a great house community."""

    name: str
    strategy: Strategy
    population: int
    elite_population: int
    monument_investment: float
    exotic_goods: int
    territory_cells: int
    resources: float
    cumulative_conflicts: int
    cumulative_deaths: int
    founding_year: int
    is_active: bool = True


@dataclass
class SimulationState:
    """Complete state of simulation at a point in time."""

    year: int
    groups: Dict[str, GroupState]
    total_population: int
    total_monument_investment: float
    total_exotic_goods: int
    total_conflicts: int
    environmental_productivity: float
    is_drought: bool


class ChacoSimulation:
    """
    Agent-based simulation of Chaco Canyon costly signaling dynamics.

    Models competition between great house communities with different
    signaling strategies under environmental uncertainty.
    """

    def __init__(
        self,
        config: Optional[SimulationConfig] = None,
        environment: Optional[Environment] = None,
        spatial: Optional[ChacoSpatialStructure] = None
    ):
        """
        Initialize simulation.

        Args:
            config: Simulation configuration
            environment: Environmental model (PDSI-based)
            spatial: Spatial structure (core + outliers)
        """
        self.config = config or SimulationConfig()
        self.environment = environment or Environment()
        self.spatial = spatial or ChacoSpatialStructure()

        # Set random seed
        if self.config.seed is not None:
            np.random.seed(self.config.seed)

        # Initialize group states
        self.groups: Dict[str, GroupState] = {}
        self._initialize_groups()

        # History tracking
        self.history: List[SimulationState] = []

        # Current year
        self.current_year = self.config.start_year

    def _initialize_groups(self):
        """Initialize great house community states."""

        # Assign strategies to great houses
        # Core houses more likely to be monument builders
        # Outliers more variable

        for house in self.spatial.get_core_houses():
            # Core houses are monument builders
            strategy = Strategy.MONUMENT_BUILDER

            self.groups[house.name] = GroupState(
                name=house.name,
                strategy=strategy,
                population=house.population,
                elite_population=house.elite_count,
                monument_investment=house.rooms * 10.0,  # Initial from room count
                exotic_goods=0,
                territory_cells=house.rooms // 5,
                resources=0.0,
                cumulative_conflicts=0,
                cumulative_deaths=0,
                founding_year=house.founding_year,
                is_active=False  # Activated when year >= founding_year
            )

        for house in self.spatial.get_outliers():
            # Outliers have mixed strategies
            strategy_roll = np.random.random()
            if strategy_roll < 0.4:
                strategy = Strategy.MONUMENT_BUILDER
            elif strategy_roll < 0.7:
                strategy = Strategy.BALANCED
            else:
                strategy = Strategy.REPRODUCTION_FOCUSED

            self.groups[house.name] = GroupState(
                name=house.name,
                strategy=strategy,
                population=house.population,
                elite_population=house.elite_count,
                monument_investment=house.rooms * 5.0,
                exotic_goods=0,
                territory_cells=house.rooms // 3,
                resources=0.0,
                cumulative_conflicts=0,
                cumulative_deaths=0,
                founding_year=house.founding_year,
                is_active=False
            )

    def _get_strategy_parameters(self, strategy: Strategy) -> Tuple[float, float]:
        """
        Get monument and exotic investment rates for a strategy.

        Returns:
            Tuple of (monument_rate, exotic_rate)
        """
        if strategy == Strategy.MONUMENT_BUILDER:
            return (self.config.monument_investment_rate,
                    self.config.exotic_investment_rate)
        elif strategy == Strategy.BALANCED:
            return (self.config.monument_investment_rate * 0.5,
                    self.config.exotic_investment_rate * 0.5)
        else:  # REPRODUCTION_FOCUSED
            return (0.05, 0.02)

    def step(self) -> SimulationState:
        """
        Execute one year of simulation.

        Annual cycle:
        1. Activate newly founded great houses
        2. Environmental productivity (with drought effects)
        3. Resource production and allocation
        4. Signaling investment (monuments and exotics)
        5. Population dynamics (births, deaths)
        6. Inter-group conflicts
        7. Pilgrimage dynamics (if enabled)
        8. Record state

        Returns:
            SimulationState for this year
        """
        year = self.current_year

        # 1. Activate great houses that have been founded
        for name, group in self.groups.items():
            if not group.is_active and group.founding_year <= year:
                group.is_active = True
                logger.debug(f"Year {year}: {name} founded")

        # Get active groups
        active_groups = {n: g for n, g in self.groups.items() if g.is_active}

        if not active_groups:
            # No active groups yet
            self.current_year += 1
            return self._record_state()

        # 2. Environmental productivity
        productivity = self.environment.get_productivity(year)
        is_drought = self.environment.is_drought(year)

        if is_drought:
            logger.debug(f"Year {year}: DROUGHT (productivity={productivity:.2f})")

        # 3. Resource production for each group
        for name, group in active_groups.items():
            base_resources = group.territory_cells * productivity * 100
            group.resources = base_resources

        # 4. Signaling investment
        self._process_signaling_investment(active_groups, year)

        # 5. Population dynamics
        self._process_population_dynamics(active_groups, productivity, is_drought)

        # 6. Inter-group conflicts
        self._process_conflicts(active_groups, year)

        # 7. Pilgrimage (if enabled)
        if self.config.enable_pilgrimage:
            self._process_pilgrimage(active_groups, year)

        # 8. Monument decay
        for group in active_groups.values():
            group.monument_investment *= (1 - self.config.monument_decay_rate)

        # Record state and advance year
        state = self._record_state()
        self.current_year += 1

        return state

    def _process_signaling_investment(
        self,
        groups: Dict[str, GroupState],
        year: int
    ):
        """Process monument construction and exotic goods acquisition."""

        for name, group in groups.items():
            monument_rate, exotic_rate = self._get_strategy_parameters(group.strategy)

            # Monument investment (group-level signaling)
            monument_resources = group.resources * monument_rate
            group.monument_investment += monument_resources / 100  # Scale factor
            group.resources -= monument_resources

            # Exotic goods acquisition (individual-level signaling)
            # Only elites acquire exotics
            if group.elite_population > 0:
                exotic_resources = group.resources * exotic_rate

                # Risk of acquisition (mortality during long-distance travel)
                acquisition_risk = self.config.exotic_acquisition_cost
                elite_deaths = int(group.elite_population * acquisition_risk * exotic_rate)
                group.elite_population = max(0, group.elite_population - elite_deaths)
                group.cumulative_deaths += elite_deaths

                # Successful acquisition
                new_exotics = int(exotic_resources / 50)  # Exotics are rare
                group.exotic_goods += new_exotics
                group.resources -= exotic_resources

    def _process_population_dynamics(
        self,
        groups: Dict[str, GroupState],
        productivity: float,
        is_drought: bool
    ):
        """Process births and deaths for each group."""

        total_pop = sum(g.population for g in groups.values())
        carrying_capacity = self.config.base_carrying_capacity * productivity

        for name, group in groups.items():
            if group.population <= 0:
                continue

            # Birth rate modified by strategy
            _, exotic_rate = self._get_strategy_parameters(group.strategy)

            # Monument builders have lower birth rate (K-selected)
            if group.strategy == Strategy.MONUMENT_BUILDER:
                birth_modifier = 0.7  # 30% reduction
            elif group.strategy == Strategy.BALANCED:
                birth_modifier = 0.85
            else:
                birth_modifier = 1.1  # r-selected bonus

            # Elite reproductive advantage from exotic goods
            elite_bonus = 0
            if group.elite_population > 0 and group.exotic_goods > 0:
                elite_bonus = min(0.2, group.exotic_goods / 100 * self.config.exotic_status_benefit)

            effective_birth_rate = self.config.base_birth_rate * birth_modifier * (1 + elite_bonus)
            births = int(group.population * effective_birth_rate)

            # Death rate
            death_rate = self.config.base_death_rate

            # Density-dependent mortality
            if total_pop > carrying_capacity:
                excess_ratio = (total_pop - carrying_capacity) / carrying_capacity
                density_deaths = excess_ratio * self.config.density_dependence
                death_rate += density_deaths

            # Drought mortality
            if is_drought:
                # Monument builders buffer better (K-selected, below carrying capacity)
                if group.strategy == Strategy.MONUMENT_BUILDER:
                    drought_modifier = 0.5  # 50% reduction in drought deaths
                elif group.strategy == Strategy.BALANCED:
                    drought_modifier = 0.75
                else:
                    drought_modifier = 1.2  # r-selected groups crash harder

                death_rate += self.config.starvation_death_rate * drought_modifier

            deaths = int(group.population * death_rate)
            group.cumulative_deaths += deaths

            # Update population
            group.population = max(0, group.population + births - deaths)

            # Elite population follows similar dynamics (simplified)
            elite_births = max(0, int(group.elite_population * effective_birth_rate * 0.5))
            elite_deaths = max(0, int(group.elite_population * death_rate * 0.8))
            group.elite_population = max(0, group.elite_population + elite_births - elite_deaths)

            # Ensure elite population doesn't exceed 10% of total
            group.elite_population = min(group.elite_population, group.population // 10)

    def _process_conflicts(
        self,
        groups: Dict[str, GroupState],
        year: int
    ):
        """Process inter-group conflicts."""

        group_list = list(groups.values())
        n_groups = len(group_list)

        if n_groups < 2:
            return

        # Each pair has a chance of conflict
        for i in range(n_groups):
            for j in range(i + 1, n_groups):
                group1 = group_list[i]
                group2 = group_list[j]

                if group1.population <= 0 or group2.population <= 0:
                    continue

                # Base conflict probability
                conflict_prob = self.config.base_conflict_rate

                # Signaling reduces conflict
                # Both must be monument builders for full reduction
                if (group1.strategy == Strategy.MONUMENT_BUILDER and
                    group2.strategy == Strategy.MONUMENT_BUILDER):
                    # Mutual signaling creates deterrence
                    signal_strength = min(
                        group1.monument_investment,
                        group2.monument_investment
                    ) / 1000  # Normalize
                    conflict_reduction = self.config.monument_conflict_reduction * min(1, signal_strength)
                    conflict_prob *= (1 - conflict_reduction)
                elif (group1.strategy == Strategy.MONUMENT_BUILDER or
                      group2.strategy == Strategy.MONUMENT_BUILDER):
                    # One-sided signaling provides some deterrence
                    conflict_prob *= 0.7

                # Roll for conflict
                if np.random.random() < conflict_prob:
                    self._resolve_conflict(group1, group2, year)

    def _resolve_conflict(
        self,
        group1: GroupState,
        group2: GroupState,
        year: int
    ):
        """Resolve a conflict between two groups."""

        logger.debug(f"Year {year}: Conflict between {group1.name} and {group2.name}")

        # Determine casualties based on relative strength
        # Monument investment provides defensive bonus
        strength1 = group1.population * (1 + group1.monument_investment / 1000)
        strength2 = group2.population * (1 + group2.monument_investment / 1000)

        total_strength = strength1 + strength2

        # Casualties proportional to enemy strength
        casualties1 = int(
            group1.population * self.config.conflict_intensity *
            (strength2 / total_strength)
        )
        casualties2 = int(
            group2.population * self.config.conflict_intensity *
            (strength1 / total_strength)
        )

        group1.population = max(0, group1.population - casualties1)
        group2.population = max(0, group2.population - casualties2)

        group1.cumulative_deaths += casualties1
        group2.cumulative_deaths += casualties2

        group1.cumulative_conflicts += 1
        group2.cumulative_conflicts += 1

        # Winner may gain territory
        if strength1 > strength2 * 1.5 and group2.territory_cells > 1:
            cells_gained = max(1, group2.territory_cells // 4)
            group1.territory_cells += cells_gained
            group2.territory_cells -= cells_gained
        elif strength2 > strength1 * 1.5 and group1.territory_cells > 1:
            cells_gained = max(1, group1.territory_cells // 4)
            group2.territory_cells += cells_gained
            group1.territory_cells -= cells_gained

    def _process_pilgrimage(
        self,
        groups: Dict[str, GroupState],
        year: int
    ):
        """Process pilgrimage dynamics - seasonal population influx to core."""

        # Only core houses receive pilgrims
        core_houses = [g for g in groups.values()
                       if g.name in [h.name for h in self.spatial.get_core_houses()]]

        if not core_houses:
            return

        # Regional population estimate
        total_regional_pop = sum(g.population for g in groups.values())

        # Pilgrims attracted by monument investment
        total_monument = sum(g.monument_investment for g in core_houses)

        for core_group in core_houses:
            if total_monument <= 0:
                continue

            # Share of pilgrims proportional to monument investment
            monument_share = core_group.monument_investment / total_monument

            # Number of pilgrims
            pilgrims = int(
                total_regional_pop *
                self.config.pilgrimage_rate *
                monument_share
            )

            # Pilgrims contribute labor to monument construction
            labor_contribution = pilgrims * self.config.pilgrimage_labor_contribution
            core_group.monument_investment += labor_contribution

    def _record_state(self) -> SimulationState:
        """Record current simulation state."""

        active_groups = {n: g for n, g in self.groups.items() if g.is_active}

        state = SimulationState(
            year=self.current_year,
            groups={n: GroupState(**vars(g)) for n, g in self.groups.items()},
            total_population=sum(g.population for g in active_groups.values()),
            total_monument_investment=sum(g.monument_investment for g in active_groups.values()),
            total_exotic_goods=sum(g.exotic_goods for g in active_groups.values()),
            total_conflicts=sum(g.cumulative_conflicts for g in active_groups.values()) // 2,
            environmental_productivity=self.environment.get_productivity(self.current_year),
            is_drought=self.environment.is_drought(self.current_year)
        )

        self.history.append(state)
        return state

    def run(self, verbose: bool = False) -> List[SimulationState]:
        """
        Run simulation from start to end year.

        Args:
            verbose: Print progress updates

        Returns:
            List of SimulationState for each year
        """
        logger.info(f"Starting simulation: {self.config.start_year} - {self.config.end_year}")

        while self.current_year < self.config.end_year:
            state = self.step()

            if verbose and self.current_year % 50 == 0:
                logger.info(
                    f"Year {state.year}: Pop={state.total_population}, "
                    f"Monuments={state.total_monument_investment:.0f}, "
                    f"Exotics={state.total_exotic_goods}, "
                    f"Conflicts={state.total_conflicts}"
                )

        logger.info(f"Simulation complete: {len(self.history)} years")
        return self.history

    def get_strategy_populations(self) -> Dict[Strategy, int]:
        """Get total population by strategy."""
        pops = {s: 0 for s in Strategy}
        for group in self.groups.values():
            if group.is_active:
                pops[group.strategy] += group.population
        return pops

    def get_core_vs_outlier_stats(self) -> Dict[str, Dict]:
        """Get statistics comparing core vs outlier great houses."""

        core_names = {h.name for h in self.spatial.get_core_houses()}

        core_groups = [g for n, g in self.groups.items()
                       if n in core_names and g.is_active]
        outlier_groups = [g for n, g in self.groups.items()
                         if n not in core_names and g.is_active]

        return {
            'core': {
                'n_groups': len(core_groups),
                'total_population': sum(g.population for g in core_groups),
                'total_monuments': sum(g.monument_investment for g in core_groups),
                'total_exotics': sum(g.exotic_goods for g in core_groups),
                'total_conflicts': sum(g.cumulative_conflicts for g in core_groups),
            },
            'outlier': {
                'n_groups': len(outlier_groups),
                'total_population': sum(g.population for g in outlier_groups),
                'total_monuments': sum(g.monument_investment for g in outlier_groups),
                'total_exotics': sum(g.exotic_goods for g in outlier_groups),
                'total_conflicts': sum(g.cumulative_conflicts for g in outlier_groups),
            }
        }


def run_scenario(
    scenario_name: str,
    config: SimulationConfig,
    env_config: Optional[EnvironmentConfig] = None,
    spatial_config: Optional[SpatialConfig] = None,
    n_replicates: int = 1
) -> List[List[SimulationState]]:
    """
    Run a simulation scenario with optional replicates.

    Args:
        scenario_name: Name for logging
        config: Simulation configuration
        env_config: Environmental configuration
        spatial_config: Spatial configuration
        n_replicates: Number of replicate runs

    Returns:
        List of histories (one per replicate)
    """
    logger.info(f"Running scenario: {scenario_name} ({n_replicates} replicates)")

    all_histories = []

    for rep in range(n_replicates):
        # Create new random seed for each replicate
        rep_config = SimulationConfig(**vars(config))
        if config.seed is not None:
            rep_config.seed = config.seed + rep

        environment = Environment(env_config)
        spatial = ChacoSpatialStructure(spatial_config)

        sim = ChacoSimulation(rep_config, environment, spatial)
        history = sim.run(verbose=(rep == 0))

        all_histories.append(history)

    return all_histories
