#!/usr/bin/env python3
"""
Run Chaco Canyon costly signaling simulation.

This script runs the simulation with default parameters matching
the Chaco Canyon archaeological record (800-1200 CE).
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from chaco.simulation import ChacoSimulation, SimulationConfig
from chaco.environment import Environment, EnvironmentConfig
from chaco.spatial import ChacoSpatialStructure, SpatialConfig
from chaco.analysis import (
    history_to_dataframe,
    generate_summary_report,
    calculate_construction_climate_correlation,
    calculate_exotic_stress_correlation,
    compare_strategies
)


def run_baseline_scenario():
    """Run simulation with baseline Chaco parameters."""

    print("=" * 70)
    print("CHACO CANYON COSTLY SIGNALING SIMULATION")
    print("=" * 70)
    print()

    # Configuration
    sim_config = SimulationConfig(
        start_year=800,
        end_year=1200,
        seed=42,
        # Use default parameters calibrated for Chaco
    )

    env_config = EnvironmentConfig(
        start_year=500,
        end_year=1500,
        base_productivity=0.7,  # Marginal environment
    )

    spatial_config = SpatialConfig(
        n_outliers=30,  # ~150 outliers in reality, using 30 for tractability
    )

    # Create components
    print("Initializing simulation components...")
    environment = Environment(env_config)
    spatial = ChacoSpatialStructure(spatial_config)

    print(f"  - Environment: {env_config.start_year}-{env_config.end_year} CE")
    print(f"  - Core great houses: {len(spatial.get_core_houses())}")
    print(f"  - Outlier communities: {len(spatial.get_outliers())}")
    print()

    # Create and run simulation
    print("Running simulation...")
    sim = ChacoSimulation(sim_config, environment, spatial)
    history = sim.run(verbose=True)
    print()

    # Generate report
    report = generate_summary_report(history, "Chaco Canyon Baseline")
    print(report)

    # Save results
    output_dir = Path(__file__).parent.parent / 'data' / 'processed'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save history as CSV
    df = history_to_dataframe(history)
    df.to_csv(output_dir / 'simulation_history_baseline.csv', index=False)
    print(f"\nSaved history to: {output_dir / 'simulation_history_baseline.csv'}")

    # Save strategy comparison
    strategy_df = compare_strategies(history)
    strategy_df.to_csv(output_dir / 'strategy_comparison_baseline.csv', index=False)
    print(f"Saved strategy comparison to: {output_dir / 'strategy_comparison_baseline.csv'}")

    return history


def run_megadrought_scenario():
    """Run simulation with intensified megadrought (sensitivity test)."""

    print("\n" + "=" * 70)
    print("MEGADROUGHT SENSITIVITY TEST")
    print("=" * 70)
    print()

    # Same configuration but with more severe drought
    sim_config = SimulationConfig(
        start_year=800,
        end_year=1200,
        seed=43,
        starvation_death_rate=0.20,  # Higher mortality during drought
    )

    # Create environment with more severe droughts
    env_config = EnvironmentConfig(
        start_year=500,
        end_year=1500,
        base_productivity=0.6,  # Even more marginal
        pdsi_sensitivity=0.15,  # More sensitive to drought
    )

    environment = Environment(env_config)
    spatial = ChacoSpatialStructure()

    sim = ChacoSimulation(sim_config, environment, spatial)
    history = sim.run(verbose=True)

    report = generate_summary_report(history, "Megadrought Scenario")
    print(report)

    return history


def run_no_signaling_counterfactual():
    """
    Run counterfactual scenario with no monument signaling.

    This tests whether signaling provides adaptive benefits.
    """

    print("\n" + "=" * 70)
    print("NO-SIGNALING COUNTERFACTUAL")
    print("=" * 70)
    print()

    sim_config = SimulationConfig(
        start_year=800,
        end_year=1200,
        seed=44,
        monument_investment_rate=0.05,  # Minimal investment
        monument_conflict_reduction=0.10,  # Minimal deterrence
        exotic_investment_rate=0.02,
    )

    environment = Environment()
    spatial = ChacoSpatialStructure()

    sim = ChacoSimulation(sim_config, environment, spatial)
    history = sim.run(verbose=True)

    report = generate_summary_report(history, "No-Signaling Counterfactual")
    print(report)

    return history


def main():
    """Run all scenarios."""

    print("\n" + "#" * 70)
    print("#  CHACO CANYON MULTI-SCALE COSTLY SIGNALING MODEL")
    print("#" * 70)
    print()
    print("This simulation tests whether investment in great houses and")
    print("exotic goods represents adaptive multi-scale costly signaling")
    print("under environmental uncertainty.")
    print()
    print("Key predictions:")
    print("  1. Construction should correlate with drought (not surplus)")
    print("  2. Exotic goods should increase during environmental stress")
    print("  3. Signaling should reduce conflict mortality")
    print("  4. System should collapse during extreme prolonged drought")
    print()

    # Run scenarios
    baseline_history = run_baseline_scenario()
    megadrought_history = run_megadrought_scenario()
    no_signaling_history = run_no_signaling_counterfactual()

    # Compare outcomes
    print("\n" + "=" * 70)
    print("SCENARIO COMPARISON")
    print("=" * 70)
    print()

    scenarios = [
        ("Baseline", baseline_history),
        ("Megadrought", megadrought_history),
        ("No Signaling", no_signaling_history),
    ]

    print(f"{'Scenario':<20} {'Final Pop':>12} {'Monuments':>12} {'Conflicts':>10}")
    print("-" * 56)

    for name, history in scenarios:
        final = history[-1]
        print(f"{name:<20} {final.total_population:>12,} "
              f"{final.total_monument_investment:>12,.0f} "
              f"{final.total_conflicts:>10}")

    print()
    print("Key finding: Monument builders should show lower mortality and")
    print("more stable populations during drought periods.")


if __name__ == '__main__':
    main()
