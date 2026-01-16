#!/usr/bin/env python3
"""
Run replicate analysis for Chaco Canyon costly signaling simulation.

This script runs multiple replicates across scenarios to generate
robust statistical estimates with confidence intervals.

Following the Rapa Nui approach:
- 10 replicates per scenario per run
- 5 independent runs with different seed ranges
- 3 scenarios: Baseline, Megadrought, No-Signaling
- Total: 3 × 10 × 5 = 150 simulations
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict
import time

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from chaco.simulation import ChacoSimulation, SimulationConfig
from chaco.environment import Environment, EnvironmentConfig
from chaco.spatial import ChacoSpatialStructure, SpatialConfig
from chaco.analysis import (
    history_to_dataframe,
    aggregate_replicate_results,
    generate_replicate_summary_report,
    ScenarioResults,
    ReplicateStatistics
)

# Configuration
N_REPLICATES = 20
N_RUNS = 5
SEED_BASE = 42


def get_scenario_configs() -> Dict[str, Dict[str, Any]]:
    """Define scenario configurations."""
    return {
        'baseline': {
            'sim_config': {
                'start_year': 800,
                'end_year': 1200,
            },
            'env_config': {
                'start_year': 500,
                'end_year': 1500,
                'base_productivity': 0.7,
            },
            'spatial_config': {
                'n_outliers': 30,
            }
        },
        'megadrought': {
            'sim_config': {
                'start_year': 800,
                'end_year': 1200,
                'starvation_death_rate': 0.20,
            },
            'env_config': {
                'start_year': 500,
                'end_year': 1500,
                'base_productivity': 0.6,
                'pmdi_sensitivity': 0.08,
                'min_productivity': 0.15,
            },
            'spatial_config': {
                'n_outliers': 30,
            }
        },
        'no_signaling': {
            'sim_config': {
                'start_year': 800,
                'end_year': 1200,
                'monument_investment_rate': 0.05,
                'monument_conflict_reduction': 0.10,
                'exotic_investment_rate': 0.02,
            },
            'env_config': {
                'start_year': 500,
                'end_year': 1500,
                'base_productivity': 0.7,
            },
            'spatial_config': {
                'n_outliers': 30,
            }
        }
    }


def run_single_simulation(
    scenario_name: str,
    config: Dict[str, Any],
    seed: int
) -> List:
    """Run a single simulation with given configuration and seed."""
    sim_params = config['sim_config'].copy()
    sim_params['seed'] = seed
    sim_config = SimulationConfig(**sim_params)

    env_config = EnvironmentConfig(**config['env_config'])
    spatial_config = SpatialConfig(**config['spatial_config'])

    environment = Environment(env_config)
    spatial = ChacoSpatialStructure(spatial_config)

    sim = ChacoSimulation(sim_config, environment, spatial)
    history = sim.run(verbose=False)

    return history


def run_scenario_replicates(
    scenario_name: str,
    config: Dict[str, Any],
    n_replicates: int = N_REPLICATES,
    n_runs: int = N_RUNS,
    seed_base: int = SEED_BASE
) -> ScenarioResults:
    """
    Run multiple replicates across independent runs for a scenario.

    Args:
        scenario_name: Name of the scenario
        config: Configuration dictionary
        n_replicates: Number of replicates per run
        n_runs: Number of independent runs
        seed_base: Base seed for reproducibility

    Returns:
        ScenarioResults with aggregated statistics
    """
    all_histories = []

    total_sims = n_replicates * n_runs
    completed = 0

    print(f"\n{'='*60}")
    print(f"Running scenario: {scenario_name}")
    print(f"Total simulations: {total_sims} ({n_replicates} replicates × {n_runs} runs)")
    print(f"{'='*60}")

    for run_idx in range(n_runs):
        run_seed_base = seed_base + run_idx * 100000

        for rep_idx in range(n_replicates):
            seed = run_seed_base + rep_idx * 1000
            completed += 1

            print(f"  [{completed}/{total_sims}] Run {run_idx+1}, Rep {rep_idx+1} (seed={seed})...", end="", flush=True)

            try:
                history = run_single_simulation(scenario_name, config, seed)
                all_histories.append(history)
                print(" done")
            except Exception as e:
                print(f" FAILED: {e}")

    return aggregate_replicate_results(all_histories, scenario_name)


def serialize_results(results: ScenarioResults) -> Dict[str, Any]:
    """Convert ScenarioResults to JSON-serializable dict."""
    def stat_to_dict(stat: ReplicateStatistics) -> Dict:
        return {
            'metric_name': stat.metric_name,
            'mean': float(stat.mean) if not isinstance(stat.mean, float) else stat.mean,
            'std': float(stat.std) if not isinstance(stat.std, float) else stat.std,
            'ci_lower': float(stat.ci_lower) if not isinstance(stat.ci_lower, float) else stat.ci_lower,
            'ci_upper': float(stat.ci_upper) if not isinstance(stat.ci_upper, float) else stat.ci_upper,
            'n_replicates': stat.n_replicates,
            'values': [float(v) if not isinstance(v, float) else v for v in stat.values]
        }

    return {
        'scenario_name': results.scenario_name,
        'n_replicates': results.n_replicates,
        'final_population': stat_to_dict(results.final_population),
        'peak_population': stat_to_dict(results.peak_population),
        'total_monuments': stat_to_dict(results.total_monuments),
        'total_exotics': stat_to_dict(results.total_exotics),
        'total_conflicts': stat_to_dict(results.total_conflicts),
        'construction_climate_r': stat_to_dict(results.construction_climate_r),
        'exotic_stress_r': stat_to_dict(results.exotic_stress_r),
        'drought_years': stat_to_dict(results.drought_years),
    }


def main():
    """Run complete replicate analysis."""
    start_time = time.time()

    print("\n" + "#" * 70)
    print("#  CHACO CANYON REPLICATE ANALYSIS")
    print("#  Statistical Robustness Testing")
    print("#" * 70)
    print()
    print(f"Configuration:")
    print(f"  - Replicates per run: {N_REPLICATES}")
    print(f"  - Independent runs: {N_RUNS}")
    print(f"  - Scenarios: 3 (baseline, megadrought, no_signaling)")
    print(f"  - Total simulations: {N_REPLICATES * N_RUNS * 3}")
    print()

    scenarios = get_scenario_configs()
    all_results = {}

    for scenario_name, config in scenarios.items():
        results = run_scenario_replicates(scenario_name, config)
        all_results[scenario_name] = results

        # Print summary
        report = generate_replicate_summary_report(results)
        print(report)

    # Save results
    output_dir = Path(__file__).parent.parent / 'data' / 'processed'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON summary
    summary_data = {
        name: serialize_results(results)
        for name, results in all_results.items()
    }

    with open(output_dir / 'replicate_analysis_summary.json', 'w') as f:
        json.dump(summary_data, f, indent=2)

    print(f"\nSaved summary to: {output_dir / 'replicate_analysis_summary.json'}")

    # Save individual scenario histories as CSVs (mean across replicates)
    for name, results in all_results.items():
        if results.histories:
            # Average across histories
            import pandas as pd
            avg_df = pd.concat(results.histories).groupby('year').mean().reset_index()
            avg_df.to_csv(output_dir / f'simulation_history_{name}_mean.csv', index=False)
            print(f"Saved mean history: {output_dir / f'simulation_history_{name}_mean.csv'}")

    # Print comparison table
    print("\n" + "=" * 80)
    print("SCENARIO COMPARISON (Mean ± SD)")
    print("=" * 80)
    print()
    print(f"{'Scenario':<15} {'Final Pop':>18} {'Peak Pop':>18} {'Monuments':>18}")
    print("-" * 72)

    for name, results in all_results.items():
        fp = results.final_population
        pp = results.peak_population
        tm = results.total_monuments
        print(f"{name:<15} {fp.mean:>9,.0f} ± {fp.std:>5,.0f}  "
              f"{pp.mean:>9,.0f} ± {pp.std:>5,.0f}  "
              f"{tm.mean:>9,.0f} ± {tm.std:>5,.0f}")

    print()
    print(f"{'Scenario':<15} {'Constr-Climate r':>20} {'Exotic-Stress r':>20}")
    print("-" * 58)

    for name, results in all_results.items():
        cc = results.construction_climate_r
        es = results.exotic_stress_r
        print(f"{name:<15} {cc.mean:>8.3f} ± {cc.std:>5.3f}      "
              f"{es.mean:>8.3f} ± {es.std:>5.3f}")

    elapsed = time.time() - start_time
    print()
    print(f"\nTotal runtime: {elapsed/60:.1f} minutes")
    print()
    print("Analysis complete!")


if __name__ == '__main__':
    main()
