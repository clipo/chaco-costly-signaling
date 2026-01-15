"""
Analysis functions for Chaco Canyon simulation results.

Provides tools for:
1. Correlation analysis between construction and climate
2. Strategy comparison and outcome analysis
3. Temporal dynamics visualization
4. Statistical summaries
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from .simulation import SimulationState, Strategy


@dataclass
class PeriodSummary:
    """Summary statistics for a time period."""
    period_name: str
    start_year: int
    end_year: int
    mean_population: float
    std_population: float
    total_monument_investment: float
    total_exotic_goods: int
    total_conflicts: int
    mean_productivity: float
    n_drought_years: int
    dominant_strategy: Strategy
    strategy_populations: Dict[Strategy, float]


def history_to_dataframe(history: List[SimulationState]) -> pd.DataFrame:
    """
    Convert simulation history to pandas DataFrame.

    Args:
        history: List of SimulationState objects

    Returns:
        DataFrame with one row per year
    """
    records = []

    for state in history:
        record = {
            'year': state.year,
            'total_population': state.total_population,
            'total_monuments': state.total_monument_investment,
            'total_exotics': state.total_exotic_goods,
            'total_conflicts': state.total_conflicts,
            'productivity': state.environmental_productivity,
            'is_drought': state.is_drought,
        }

        # Strategy-specific populations
        strategy_pops = {s: 0 for s in Strategy}
        for group in state.groups.values():
            if group.is_active:
                strategy_pops[group.strategy] += group.population

        for strategy, pop in strategy_pops.items():
            record[f'pop_{strategy.value}'] = pop

        records.append(record)

    return pd.DataFrame(records)


def calculate_construction_climate_correlation(
    history: List[SimulationState],
    lag: int = 0
) -> Tuple[float, float]:
    """
    Calculate correlation between construction activity and climate (PDSI proxy).

    Args:
        history: Simulation history
        lag: Years to lag construction behind climate (positive = construction follows drought)

    Returns:
        Tuple of (correlation coefficient, p-value)
    """
    from scipy import stats

    df = history_to_dataframe(history)

    if len(df) < 10:
        return (np.nan, np.nan)

    # Calculate year-over-year monument investment change as construction proxy
    df['monument_change'] = df['total_monuments'].diff()

    # Apply lag
    if lag > 0:
        productivity = df['productivity'].values[:-lag]
        construction = df['monument_change'].values[lag:]
    elif lag < 0:
        productivity = df['productivity'].values[-lag:]
        construction = df['monument_change'].values[:lag]
    else:
        productivity = df['productivity'].values[1:]  # Skip first NaN
        construction = df['monument_change'].values[1:]

    # Remove NaN values
    mask = ~(np.isnan(productivity) | np.isnan(construction))
    productivity = productivity[mask]
    construction = construction[mask]

    if len(productivity) < 5:
        return (np.nan, np.nan)

    r, p = stats.pearsonr(productivity, construction)
    return (r, p)


def calculate_exotic_stress_correlation(
    history: List[SimulationState]
) -> Tuple[float, float]:
    """
    Calculate correlation between exotic goods acquisition and environmental stress.

    Prediction: Exotic goods should INCREASE during stress (positive correlation
    with low productivity / negative correlation with PDSI).

    Returns:
        Tuple of (correlation coefficient, p-value)
    """
    from scipy import stats

    df = history_to_dataframe(history)

    if len(df) < 10:
        return (np.nan, np.nan)

    # Year-over-year change in exotics
    df['exotic_change'] = df['total_exotics'].diff()

    # Inverse productivity as stress measure
    df['stress'] = 1 - df['productivity']

    # Skip first year (NaN from diff)
    stress = df['stress'].values[1:]
    exotics = df['exotic_change'].values[1:]

    mask = ~(np.isnan(stress) | np.isnan(exotics))
    stress = stress[mask]
    exotics = exotics[mask]

    if len(stress) < 5:
        return (np.nan, np.nan)

    r, p = stats.pearsonr(stress, exotics)
    return (r, p)


def analyze_period(
    history: List[SimulationState],
    start_year: int,
    end_year: int,
    period_name: str
) -> PeriodSummary:
    """
    Analyze simulation results for a specific time period.

    Args:
        history: Simulation history
        start_year: Period start
        end_year: Period end
        period_name: Name for this period

    Returns:
        PeriodSummary with statistics
    """
    period_states = [s for s in history if start_year <= s.year < end_year]

    if not period_states:
        raise ValueError(f"No data for period {start_year}-{end_year}")

    populations = [s.total_population for s in period_states]
    productivities = [s.environmental_productivity for s in period_states]
    drought_years = sum(1 for s in period_states if s.is_drought)

    # Final state for cumulative values
    final = period_states[-1]

    # Strategy populations
    strategy_pops = {s: [] for s in Strategy}
    for state in period_states:
        state_strategy_pops = {s: 0 for s in Strategy}
        for group in state.groups.values():
            if group.is_active:
                state_strategy_pops[group.strategy] += group.population
        for strategy, pop in state_strategy_pops.items():
            strategy_pops[strategy].append(pop)

    mean_strategy_pops = {s: np.mean(pops) if pops else 0
                          for s, pops in strategy_pops.items()}

    # Dominant strategy
    dominant = max(mean_strategy_pops, key=mean_strategy_pops.get)

    return PeriodSummary(
        period_name=period_name,
        start_year=start_year,
        end_year=end_year,
        mean_population=float(np.mean(populations)),
        std_population=float(np.std(populations)),
        total_monument_investment=final.total_monument_investment,
        total_exotic_goods=final.total_exotic_goods,
        total_conflicts=final.total_conflicts,
        mean_productivity=float(np.mean(productivities)),
        n_drought_years=drought_years,
        dominant_strategy=dominant,
        strategy_populations=mean_strategy_pops
    )


def compare_strategies(
    history: List[SimulationState]
) -> pd.DataFrame:
    """
    Compare outcomes by strategy type.

    Returns:
        DataFrame with strategy comparison metrics
    """
    # Collect data from final state
    if not history:
        return pd.DataFrame()

    final = history[-1]

    strategy_data = {s: {
        'n_groups': 0,
        'total_population': 0,
        'total_monuments': 0,
        'total_exotics': 0,
        'total_conflicts': 0,
        'total_deaths': 0,
    } for s in Strategy}

    for group in final.groups.values():
        if not group.is_active:
            continue

        s = group.strategy
        strategy_data[s]['n_groups'] += 1
        strategy_data[s]['total_population'] += group.population
        strategy_data[s]['total_monuments'] += group.monument_investment
        strategy_data[s]['total_exotics'] += group.exotic_goods
        strategy_data[s]['total_conflicts'] += group.cumulative_conflicts
        strategy_data[s]['total_deaths'] += group.cumulative_deaths

    records = []
    for strategy, data in strategy_data.items():
        record = {'strategy': strategy.value}
        record.update(data)

        # Calculate per-capita metrics
        if data['n_groups'] > 0:
            record['pop_per_group'] = data['total_population'] / data['n_groups']
            record['monuments_per_group'] = data['total_monuments'] / data['n_groups']
        else:
            record['pop_per_group'] = 0
            record['monuments_per_group'] = 0

        if data['total_population'] > 0:
            record['deaths_per_capita'] = data['total_deaths'] / data['total_population']
            record['conflicts_per_capita'] = data['total_conflicts'] / data['total_population']
        else:
            record['deaths_per_capita'] = 0
            record['conflicts_per_capita'] = 0

        records.append(record)

    return pd.DataFrame(records)


def calculate_sigma(
    history: List[SimulationState],
    drought_threshold: float = 0.6
) -> float:
    """
    Calculate environmental uncertainty parameter sigma from simulation history.

    sigma = (magnitude * duration) / frequency

    Args:
        history: Simulation history
        drought_threshold: Productivity threshold for drought

    Returns:
        Sigma value
    """
    if not history:
        return 0.0

    # Find drought events
    in_drought = False
    drought_events = []
    current_drought: Dict = {}

    for state in history:
        is_drought = state.environmental_productivity < drought_threshold

        if is_drought and not in_drought:
            in_drought = True
            current_drought = {
                'start': state.year,
                'min_prod': state.environmental_productivity
            }
        elif is_drought and in_drought:
            current_drought['min_prod'] = min(
                current_drought['min_prod'],
                state.environmental_productivity
            )
        elif not is_drought and in_drought:
            in_drought = False
            current_drought['end'] = state.year
            current_drought['duration'] = current_drought['end'] - current_drought['start']
            drought_events.append(current_drought)

    if not drought_events:
        return 0.0

    n_droughts = len(drought_events)
    total_years = history[-1].year - history[0].year
    frequency = total_years / n_droughts if n_droughts > 0 else total_years

    avg_magnitude = np.mean([
        (drought_threshold - d['min_prod']) / drought_threshold
        for d in drought_events
    ])
    avg_duration = np.mean([d['duration'] for d in drought_events])

    sigma = (avg_magnitude * avg_duration) / frequency
    return float(sigma)


def generate_summary_report(
    history: List[SimulationState],
    scenario_name: str = "Simulation"
) -> str:
    """
    Generate a text summary report of simulation results.

    Args:
        history: Simulation history
        scenario_name: Name for the report

    Returns:
        Formatted text report
    """
    if not history:
        return "No simulation data available."

    df = history_to_dataframe(history)
    start_year = history[0].year
    end_year = history[-1].year

    # Correlations
    constr_corr, constr_p = calculate_construction_climate_correlation(history)
    exotic_corr, exotic_p = calculate_exotic_stress_correlation(history)

    # Strategy comparison
    strategy_df = compare_strategies(history)

    # Period analyses
    periods = [
        (800, 900, "Pre-Chaco"),
        (900, 1000, "Early Chaco"),
        (1000, 1100, "Peak Chaco"),
        (1100, 1200, "Late Chaco/Collapse"),
    ]

    period_summaries = []
    for start, end, name in periods:
        if start >= start_year and end <= end_year + 1:
            try:
                summary = analyze_period(history, start, end, name)
                period_summaries.append(summary)
            except ValueError:
                pass

    # Build report
    lines = [
        f"=" * 70,
        f"SIMULATION REPORT: {scenario_name}",
        f"=" * 70,
        f"",
        f"Time Range: {start_year} - {end_year} CE ({end_year - start_year} years)",
        f"",
        f"--- OVERALL STATISTICS ---",
        f"Final Population: {history[-1].total_population:,}",
        f"Peak Population: {df['total_population'].max():,} (Year {df.loc[df['total_population'].idxmax(), 'year']})",
        f"Total Monument Investment: {history[-1].total_monument_investment:,.0f}",
        f"Total Exotic Goods: {history[-1].total_exotic_goods:,}",
        f"Total Conflicts: {history[-1].total_conflicts:,}",
        f"Drought Years: {df['is_drought'].sum()} ({100*df['is_drought'].mean():.1f}%)",
        f"",
        f"--- CORRELATIONS ---",
        f"Construction-Climate Correlation: r = {constr_corr:.3f}" + (f" (p = {constr_p:.4f})" if not np.isnan(constr_p) else ""),
        f"  (Negative = more construction during drought)",
        f"Exotic Goods-Stress Correlation: r = {exotic_corr:.3f}" + (f" (p = {exotic_p:.4f})" if not np.isnan(exotic_p) else ""),
        f"  (Positive = more exotics during stress)",
        f"",
        f"--- STRATEGY COMPARISON ---",
    ]

    if not strategy_df.empty:
        for _, row in strategy_df.iterrows():
            lines.append(f"  {row['strategy']}:")
            lines.append(f"    Groups: {row['n_groups']}, Population: {row['total_population']:,}")
            lines.append(f"    Monuments: {row['total_monuments']:.0f}, Exotics: {row['total_exotics']}")
            lines.append(f"    Deaths/capita: {row['deaths_per_capita']:.3f}")

    lines.append("")
    lines.append("--- PERIOD ANALYSIS ---")

    for summary in period_summaries:
        lines.append(f"  {summary.period_name} ({summary.start_year}-{summary.end_year}):")
        lines.append(f"    Mean Pop: {summary.mean_population:,.0f} (+/- {summary.std_population:.0f})")
        lines.append(f"    Monuments: {summary.total_monument_investment:.0f}")
        lines.append(f"    Drought Years: {summary.n_drought_years}")
        lines.append(f"    Dominant Strategy: {summary.dominant_strategy.value}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)
