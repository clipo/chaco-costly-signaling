"""
Core simulation engine for Chaco Canyon costly signaling model.

Implements the three-layer formal model from the manuscript:
  Layer 1: Individual signaling via Spence condition — x*(q) = sqrt(lambda * (q^2 - q_min^2))
  Layer 2: Intergroup assessment — sigma_eff = sigma_0 / sqrt(1 + kappa*(M_g + M_h))
  Layer 3: Cooperation networks with lambda-sigma feedback — lambda(sigma) = lambda_0 + lambda_1*sigma^alpha

Groups have continuous quality q (productive capacity) rather than discrete strategies.
Environmental uncertainty (sigma) modulates the fitness returns to signaling.
"""

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
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


@dataclass
class SimulationConfig:
    """Configuration for simulation parameters."""

    # Time parameters
    start_year: int = 800
    end_year: int = 1200

    # Population parameters
    base_birth_rate: float = 0.04
    base_death_rate: float = 0.03
    starvation_death_rate: float = 0.15
    conflict_death_rate: float = 0.05

    # Carrying capacity
    base_carrying_capacity: int = 3000
    density_dependence: float = 0.5

    # Layer 1: Spence signaling parameters
    q_min: float = 0.1            # Minimum quality (small-house threshold)
    lambda_0: float = 0.3         # Baseline signaling return
    lambda_1: float = 0.5         # Sensitivity of lambda to sigma
    alpha: float = 1.0            # Lambda-sigma exponent (1.0 = linear)
    monument_decay_rate: float = 0.02  # Annual informational depreciation (delta)
    investment_scale: float = 10.0     # Scale factor: model units -> simulation units

    # Layer 2: Assessment parameters
    sigma_0: float = 0.5          # Baseline assessment noise
    kappa: float = 0.001          # Informational contribution of monument stock
    base_conflict_rate: float = 0.10
    conflict_intensity: float = 0.30

    # Layer 3: Cooperation network parameters
    gamma: float = 0.1            # Buffering value per exchange partner
    network_formation_rate: float = 0.01  # Partners gained per unit monument investment

    # Exotic goods (individual-level, Layer 1)
    exotic_investment_rate: float = 0.10
    exotic_acquisition_cost: float = 0.05
    exotic_status_benefit: float = 0.20

    # Sigma computation
    sigma_window: int = 30        # Rolling window for sigma (years)

    # Pilgrimage dynamics
    enable_pilgrimage: bool = True
    pilgrimage_rate: float = 0.10
    pilgrimage_labor_contribution: float = 0.05

    # Random seed
    seed: Optional[int] = 42


@dataclass
class GroupState:
    """State of a great house community."""

    name: str
    quality: float                # q: productive capacity (continuous)
    population: int
    elite_population: int
    monument_investment: float    # M_g: accumulated monument stock
    exotic_goods: int
    territory_cells: int
    resources: float
    exchange_partners: float      # k: number of cooperation network partners
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
    sigma: float                  # Current environmental uncertainty
    current_lambda: float         # Current signaling return


class ChacoSimulation:
    """
    Agent-based simulation implementing the three-layer costly signaling model.

    Layer 1: Spence condition determines quality-dependent investment.
    Layer 2: Mutual assessment through monuments reduces conflict.
    Layer 3: Lambda-sigma feedback links uncertainty to signaling returns.
    """

    def __init__(
        self,
        config: Optional[SimulationConfig] = None,
        environment: Optional[Environment] = None,
        spatial: Optional[ChacoSpatialStructure] = None
    ):
        self.config = config or SimulationConfig()
        self.environment = environment or Environment()
        self.spatial = spatial or ChacoSpatialStructure()

        if self.config.seed is not None:
            np.random.seed(self.config.seed)

        self.groups: Dict[str, GroupState] = {}
        self._initialize_groups()

        self.history: List[SimulationState] = []
        self.current_year = self.config.start_year

        # Cache for rolling sigma computation
        self._pmdi_history: List[float] = []

    def _quality_from_rooms(self, rooms: int, is_core: bool) -> float:
        """
        Derive quality q from room count (proxy for productive capacity).

        Quality is scaled so that:
          - Small-house communities (0 rooms) -> q_min
          - Pueblo Bonito (350 rooms) -> ~2.0
          - Outlier great houses (15-50 rooms) -> 0.3-0.7
        """
        if rooms <= 0:
            return self.config.q_min
        # Sqrt scaling: q = q_min + c * sqrt(rooms)
        # Calibrate so 350 rooms -> q ≈ 2.0
        c = (2.0 - self.config.q_min) / math.sqrt(350)
        return self.config.q_min + c * math.sqrt(rooms)

    def _initialize_groups(self):
        """Initialize great house community states with continuous quality."""

        for house in self.spatial.get_core_houses():
            q = self._quality_from_rooms(house.rooms, is_core=True)
            self.groups[house.name] = GroupState(
                name=house.name,
                quality=q,
                population=house.population,
                elite_population=house.elite_count,
                monument_investment=house.rooms * 5.0,  # Initial stock from construction
                exotic_goods=0,
                territory_cells=house.rooms // 5,
                resources=0.0,
                exchange_partners=max(1.0, q * 3.0),  # Initial partners scale with quality
                cumulative_conflicts=0,
                cumulative_deaths=0,
                founding_year=house.founding_year,
                is_active=False
            )

        for house in self.spatial.get_outliers():
            q = self._quality_from_rooms(house.rooms, is_core=False)
            self.groups[house.name] = GroupState(
                name=house.name,
                quality=q,
                population=house.population,
                elite_population=house.elite_count,
                monument_investment=house.rooms * 2.0,
                exotic_goods=0,
                territory_cells=house.rooms // 3,
                resources=0.0,
                exchange_partners=max(0.5, q * 1.5),
                cumulative_conflicts=0,
                cumulative_deaths=0,
                founding_year=house.founding_year,
                is_active=False
            )

    def _compute_sigma(self, year: int) -> float:
        """
        Compute rolling environmental uncertainty (sigma) from recent PMDI history.

        Uses the standard deviation of PMDI over a rolling window.
        """
        pmdi = self.environment.get_pmdi(year)
        self._pmdi_history.append(pmdi)

        window = self.config.sigma_window
        if len(self._pmdi_history) < window // 2:
            return 0.1  # Default low sigma early on

        recent = self._pmdi_history[-window:]
        return float(np.std(recent))

    def _compute_lambda(self, sigma: float) -> float:
        """
        Lambda-sigma feedback: lambda(sigma) = lambda_0 + lambda_1 * sigma^alpha

        Higher environmental uncertainty -> higher returns to signaling.
        """
        c = self.config
        return c.lambda_0 + c.lambda_1 * (sigma ** c.alpha)

    def _spence_investment(self, q: float, lam: float) -> float:
        """
        Spence equilibrium investment: x*(q) = sqrt(lambda * (q^2 - q_min^2))

        Returns the optimal investment level for a group of quality q
        given current lambda.
        """
        q_min = self.config.q_min
        if q <= q_min:
            return 0.0
        val = lam * (q ** 2 - q_min ** 2)
        if val <= 0:
            return 0.0
        return math.sqrt(val)

    def _assessment_noise(self, m_g: float, m_h: float) -> float:
        """
        Effective assessment noise between two groups:
        sigma_eff = sigma_0 / sqrt(1 + kappa * (M_g + M_h))
        """
        c = self.config
        return c.sigma_0 / math.sqrt(1.0 + c.kappa * (m_g + m_h))

    def _survival_probability(self, sigma: float, k: float) -> float:
        """
        Exponential survival function: S(sigma, k) = exp(-sigma / (1 + gamma * k))
        """
        denominator = 1.0 + self.config.gamma * k
        return math.exp(-sigma / denominator)

    def step(self) -> SimulationState:
        """
        Execute one year of simulation.

        Annual cycle:
        1. Activate newly founded great houses
        2. Compute environmental sigma and lambda
        3. Resource production
        4. Spence-equilibrium signaling investment
        5. Population dynamics with network-based buffering
        6. Intergroup conflicts via mutual assessment
        7. Network partner formation
        8. Pilgrimage (if enabled)
        9. Monument depreciation
        """
        year = self.current_year

        # 1. Activate great houses that have been founded
        for name, group in self.groups.items():
            if not group.is_active and group.founding_year <= year:
                group.is_active = True
                logger.debug(f"Year {year}: {name} founded (q={group.quality:.2f})")

        active_groups = {n: g for n, g in self.groups.items() if g.is_active}

        if not active_groups:
            self.current_year += 1
            return self._record_state(0.1, self.config.lambda_0)

        # 2. Environmental state
        productivity = self.environment.get_productivity(year)
        is_drought = self.environment.is_drought(year)
        sigma = self._compute_sigma(year)
        current_lambda = self._compute_lambda(sigma)

        # 3. Resource production
        for name, group in active_groups.items():
            group.resources = group.territory_cells * productivity * 100

        # 4. Spence-equilibrium signaling investment
        self._process_signaling_investment(active_groups, current_lambda)

        # 5. Population dynamics (with network-based drought buffering)
        self._process_population_dynamics(
            active_groups, productivity, is_drought, sigma
        )

        # 6. Intergroup conflicts via mutual assessment
        self._process_conflicts(active_groups, year)

        # 7. Network partner formation (monument builders attract partners)
        self._update_exchange_networks(active_groups)

        # 8. Pilgrimage
        if self.config.enable_pilgrimage:
            self._process_pilgrimage(active_groups, year)

        # 9. Monument depreciation
        for group in active_groups.values():
            group.monument_investment *= (1 - self.config.monument_decay_rate)

        state = self._record_state(sigma, current_lambda)
        self.current_year += 1
        return state

    def _process_signaling_investment(
        self,
        groups: Dict[str, GroupState],
        current_lambda: float
    ):
        """
        Layer 1: Spence-condition investment.

        Each group invests at x*(q) = sqrt(lambda * (q^2 - q_min^2)),
        constrained by available resources.
        """
        for name, group in groups.items():
            # Optimal investment from Spence equilibrium
            optimal_x = self._spence_investment(group.quality, current_lambda)

            # Convert to resource cost: c(x, q) = x^2 / (2q)
            resource_cost = (optimal_x ** 2) / (2.0 * group.quality) if group.quality > 0 else 0
            resource_cost_scaled = resource_cost * self.config.investment_scale

            # Constrain by available resources (can't invest more than you have)
            actual_cost = min(resource_cost_scaled, group.resources * 0.5)

            # Add to monument stock (scale investment to monument units)
            if group.quality > 0:
                actual_x = math.sqrt(2.0 * group.quality * actual_cost / self.config.investment_scale) if actual_cost > 0 else 0
            else:
                actual_x = 0
            group.monument_investment += actual_x
            group.resources -= actual_cost

            # Exotic goods acquisition (individual-level, elites only)
            if group.elite_population > 0:
                exotic_resources = group.resources * self.config.exotic_investment_rate
                acquisition_risk = self.config.exotic_acquisition_cost
                elite_deaths = int(
                    group.elite_population * acquisition_risk *
                    self.config.exotic_investment_rate
                )
                group.elite_population = max(0, group.elite_population - elite_deaths)
                group.cumulative_deaths += elite_deaths

                new_exotics = int(exotic_resources / 50)
                group.exotic_goods += new_exotics
                group.resources -= exotic_resources

    def _process_population_dynamics(
        self,
        groups: Dict[str, GroupState],
        productivity: float,
        is_drought: bool,
        sigma: float
    ):
        """
        Population dynamics with Layer 3 network-based buffering.

        During drought, survival depends on exchange partners:
        S(sigma, k) = exp(-sigma / (1 + gamma * k))
        """
        total_pop = sum(g.population for g in groups.values())
        carrying_capacity = self.config.base_carrying_capacity * productivity

        for name, group in groups.items():
            if group.population <= 0:
                continue

            # Birth rate (higher quality -> slightly lower birth rate, K-selected)
            q_normalized = min(group.quality / 2.0, 1.0)
            birth_modifier = 1.1 - 0.4 * q_normalized  # ranges 1.1 to 0.7
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
                death_rate += excess_ratio * self.config.density_dependence

            # Drought mortality: buffered by exchange network (Layer 3)
            if is_drought:
                # Survival probability from exponential function
                survival_prob = self._survival_probability(sigma, group.exchange_partners)
                # Convert to additional death rate: lower survival -> more deaths
                drought_death_rate = self.config.starvation_death_rate * (1.0 - survival_prob)
                death_rate += drought_death_rate

            deaths = int(group.population * death_rate)
            group.cumulative_deaths += deaths
            group.population = max(0, group.population + births - deaths)

            # Elite dynamics
            elite_births = max(0, int(group.elite_population * effective_birth_rate * 0.5))
            elite_deaths = max(0, int(group.elite_population * death_rate * 0.8))
            group.elite_population = max(0, group.elite_population + elite_births - elite_deaths)
            group.elite_population = min(group.elite_population, group.population // 10)

    def _process_conflicts(
        self,
        groups: Dict[str, GroupState],
        year: int
    ):
        """
        Layer 2: Intergroup conflict via mutual assessment.

        Conflict probability decreases as assessment noise decreases
        (which happens when both groups have high monument investment).
        """
        group_list = list(groups.values())
        n_groups = len(group_list)

        if n_groups < 2:
            return

        for i in range(n_groups):
            for j in range(i + 1, n_groups):
                g1 = group_list[i]
                g2 = group_list[j]

                if g1.population <= 0 or g2.population <= 0:
                    continue

                # Assessment noise decreases with monument stock
                noise = self._assessment_noise(
                    g1.monument_investment, g2.monument_investment
                )

                # Conflict probability proportional to assessment noise
                # When noise is high (no monuments), conflict is at base rate
                # When noise is low (large monuments), conflict is suppressed
                noise_ratio = noise / self.config.sigma_0  # 0 to 1
                conflict_prob = self.config.base_conflict_rate * noise_ratio

                if np.random.random() < conflict_prob:
                    self._resolve_conflict(g1, g2, year)

    def _resolve_conflict(
        self,
        group1: GroupState,
        group2: GroupState,
        year: int
    ):
        """Resolve a conflict between two groups."""
        logger.debug(f"Year {year}: Conflict {group1.name} vs {group2.name}")

        # Strength includes monument-signaled capacity
        strength1 = group1.population * (1 + group1.monument_investment / 500)
        strength2 = group2.population * (1 + group2.monument_investment / 500)
        total_strength = strength1 + strength2

        if total_strength <= 0:
            return

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

        # Territory changes for decisive victories
        if strength1 > strength2 * 1.5 and group2.territory_cells > 1:
            cells = max(1, group2.territory_cells // 4)
            group1.territory_cells += cells
            group2.territory_cells -= cells
        elif strength2 > strength1 * 1.5 and group1.territory_cells > 1:
            cells = max(1, group1.territory_cells // 4)
            group2.territory_cells += cells
            group1.territory_cells -= cells

    def _update_exchange_networks(self, groups: Dict[str, GroupState]):
        """
        Layer 3: Monument investment attracts exchange partners.

        Partners grow with monument stock, decay without it.
        """
        c = self.config
        for name, group in groups.items():
            # New partners attracted by current monument investment
            new_partners = group.monument_investment * c.network_formation_rate
            # Partners decay if monument investment is low
            partner_decay = 0.05 * group.exchange_partners
            group.exchange_partners = max(
                0.0,
                group.exchange_partners + new_partners - partner_decay
            )

    def _process_pilgrimage(
        self,
        groups: Dict[str, GroupState],
        year: int
    ):
        """Pilgrimage: seasonal labor influx proportional to monument stock."""
        core_houses = [
            g for g in groups.values()
            if g.name in [h.name for h in self.spatial.get_core_houses()]
        ]
        if not core_houses:
            return

        total_regional_pop = sum(g.population for g in groups.values())
        total_monument = sum(g.monument_investment for g in core_houses)

        for core in core_houses:
            if total_monument <= 0:
                continue
            share = core.monument_investment / total_monument
            pilgrims = int(total_regional_pop * self.config.pilgrimage_rate * share)
            core.monument_investment += pilgrims * self.config.pilgrimage_labor_contribution

    def _record_state(self, sigma: float, current_lambda: float) -> SimulationState:
        """Record current simulation state."""
        active = {n: g for n, g in self.groups.items() if g.is_active}

        state = SimulationState(
            year=self.current_year,
            groups={n: GroupState(**vars(g)) for n, g in self.groups.items()},
            total_population=sum(g.population for g in active.values()),
            total_monument_investment=sum(g.monument_investment for g in active.values()),
            total_exotic_goods=sum(g.exotic_goods for g in active.values()),
            total_conflicts=sum(g.cumulative_conflicts for g in active.values()) // 2,
            environmental_productivity=self.environment.get_productivity(self.current_year),
            is_drought=self.environment.is_drought(self.current_year),
            sigma=sigma,
            current_lambda=current_lambda,
        )
        self.history.append(state)
        return state

    def run(self, verbose: bool = False) -> List[SimulationState]:
        """Run simulation from start to end year."""
        logger.info(f"Starting simulation: {self.config.start_year}-{self.config.end_year}")

        while self.current_year < self.config.end_year:
            state = self.step()

            if verbose and self.current_year % 50 == 0:
                logger.info(
                    f"Year {state.year}: Pop={state.total_population}, "
                    f"Monuments={state.total_monument_investment:.0f}, "
                    f"sigma={state.sigma:.3f}, lambda={state.current_lambda:.3f}"
                )

        logger.info(f"Simulation complete: {len(self.history)} years")
        return self.history

    def get_quality_investment_summary(self) -> List[Dict]:
        """Get quality vs investment for all active groups (for Spence calibration check)."""
        results = []
        for name, group in self.groups.items():
            if group.is_active:
                results.append({
                    'name': name,
                    'quality': group.quality,
                    'monument_investment': group.monument_investment,
                    'exchange_partners': group.exchange_partners,
                    'population': group.population,
                })
        return sorted(results, key=lambda x: x['quality'])

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
                'avg_quality': np.mean([g.quality for g in core_groups]) if core_groups else 0,
                'avg_partners': np.mean([g.exchange_partners for g in core_groups]) if core_groups else 0,
            },
            'outlier': {
                'n_groups': len(outlier_groups),
                'total_population': sum(g.population for g in outlier_groups),
                'total_monuments': sum(g.monument_investment for g in outlier_groups),
                'total_exotics': sum(g.exotic_goods for g in outlier_groups),
                'avg_quality': np.mean([g.quality for g in outlier_groups]) if outlier_groups else 0,
                'avg_partners': np.mean([g.exchange_partners for g in outlier_groups]) if outlier_groups else 0,
            }
        }


def run_scenario(
    scenario_name: str,
    config: SimulationConfig,
    env_config: Optional[EnvironmentConfig] = None,
    spatial_config: Optional[SpatialConfig] = None,
    n_replicates: int = 1
) -> List[List[SimulationState]]:
    """Run a simulation scenario with optional replicates."""
    logger.info(f"Running scenario: {scenario_name} ({n_replicates} replicates)")

    all_histories = []
    for rep in range(n_replicates):
        rep_config = SimulationConfig(**vars(config))
        if config.seed is not None:
            rep_config.seed = config.seed + rep

        environment = Environment(env_config)
        spatial = ChacoSpatialStructure(spatial_config)
        sim = ChacoSimulation(rep_config, environment, spatial)
        history = sim.run(verbose=(rep == 0))
        all_histories.append(history)

    return all_histories
