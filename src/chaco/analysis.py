"""
Analysis functions for Chaco Canyon simulation results.

Provides tools for:
1. Correlation analysis between construction and climate
2. Strategy comparison and outcome analysis
3. Temporal dynamics visualization
4. Statistical summaries
5. Replicate analysis and confidence intervals
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from scipy import stats

from .simulation import SimulationState


@dataclass
class ReplicateStatistics:
    """Statistics aggregated across replicates."""
    metric_name: str
    mean: float
    std: float
    ci_lower: float
    ci_upper: float
    n_replicates: int
    values: List[float] = field(default_factory=list)


@dataclass
class ScenarioResults:
    """Results from running a scenario with multiple replicates."""
    scenario_name: str
    n_replicates: int
    final_population: ReplicateStatistics
    peak_population: ReplicateStatistics
    total_monuments: ReplicateStatistics
    total_exotics: ReplicateStatistics
    total_conflicts: ReplicateStatistics
    construction_climate_r: ReplicateStatistics
    exotic_stress_r: ReplicateStatistics
    drought_years: ReplicateStatistics
    histories: List[pd.DataFrame] = field(default_factory=list)


def calculate_confidence_interval(
    values: List[float],
    confidence: float = 0.95
) -> Tuple[float, float, float, float]:
    """
    Calculate mean, standard deviation, and confidence interval.

    Args:
        values: List of numeric values
        confidence: Confidence level (default 0.95 for 95% CI)

    Returns:
        Tuple of (mean, std, ci_lower, ci_upper)
    """
    if not values or len(values) < 2:
        return (np.nan, np.nan, np.nan, np.nan)

    arr = np.array(values)
    arr = arr[~np.isnan(arr)]

    if len(arr) < 2:
        return (np.nan, np.nan, np.nan, np.nan)

    mean = np.mean(arr)
    std = np.std(arr, ddof=1)
    n = len(arr)

    # t-distribution for small samples
    t_val = stats.t.ppf((1 + confidence) / 2, n - 1)
    margin = t_val * (std / np.sqrt(n))

    return (mean, std, mean - margin, mean + margin)


def create_replicate_statistics(
    values: List[float],
    metric_name: str,
    confidence: float = 0.95
) -> ReplicateStatistics:
    """
    Create ReplicateStatistics from a list of values.

    Args:
        values: List of metric values across replicates
        metric_name: Name of the metric
        confidence: Confidence level

    Returns:
        ReplicateStatistics object
    """
    mean, std, ci_lower, ci_upper = calculate_confidence_interval(values, confidence)

    return ReplicateStatistics(
        metric_name=metric_name,
        mean=mean,
        std=std,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        n_replicates=len([v for v in values if not np.isnan(v)]),
        values=values
    )


def aggregate_replicate_results(
    histories: List[List[SimulationState]],
    scenario_name: str
) -> ScenarioResults:
    """
    Aggregate results from multiple simulation replicates.

    Args:
        histories: List of simulation histories (one per replicate)
        scenario_name: Name for this scenario

    Returns:
        ScenarioResults with aggregated statistics
    """
    final_pops = []
    peak_pops = []
    monuments = []
    exotics = []
    conflicts = []
    constr_rs = []
    exotic_rs = []
    drought_counts = []
    history_dfs = []

    for history in histories:
        if not history:
            continue

        df = history_to_dataframe(history)
        history_dfs.append(df)

        # Final state metrics
        final = history[-1]
        final_pops.append(final.total_population)
        monuments.append(final.total_monument_investment)
        exotics.append(final.total_exotic_goods)
        conflicts.append(final.total_conflicts)

        # Peak population
        peak_pops.append(df['total_population'].max())

        # Drought years
        drought_counts.append(df['is_drought'].sum())

        # Correlations
        r_constr, _ = calculate_construction_climate_correlation(history)
        r_exotic, _ = calculate_exotic_stress_correlation(history)
        constr_rs.append(r_constr)
        exotic_rs.append(r_exotic)

    return ScenarioResults(
        scenario_name=scenario_name,
        n_replicates=len(histories),
        final_population=create_replicate_statistics(final_pops, "final_population"),
        peak_population=create_replicate_statistics(peak_pops, "peak_population"),
        total_monuments=create_replicate_statistics(monuments, "total_monuments"),
        total_exotics=create_replicate_statistics(exotics, "total_exotics"),
        total_conflicts=create_replicate_statistics(conflicts, "total_conflicts"),
        construction_climate_r=create_replicate_statistics(constr_rs, "construction_climate_r"),
        exotic_stress_r=create_replicate_statistics(exotic_rs, "exotic_stress_r"),
        drought_years=create_replicate_statistics(drought_counts, "drought_years"),
        histories=history_dfs
    )


def format_stat_with_ci(stat: ReplicateStatistics, decimals: int = 2) -> str:
    """
    Format a statistic with confidence interval for reporting.

    Args:
        stat: ReplicateStatistics object
        decimals: Number of decimal places

    Returns:
        Formatted string like "1234.56 ± 123.45 (95% CI [1111.11, 1357.90])"
    """
    if np.isnan(stat.mean):
        return "N/A"

    if decimals == 0:
        return (f"{stat.mean:,.0f} ± {stat.std:,.0f} "
                f"(95% CI [{stat.ci_lower:,.0f}, {stat.ci_upper:,.0f}])")
    else:
        fmt = f",.{decimals}f"
        return (f"{stat.mean:{fmt}} ± {stat.std:{fmt}} "
                f"(95% CI [{stat.ci_lower:{fmt}}, {stat.ci_upper:{fmt}}])")


def format_correlation_with_ci(stat: ReplicateStatistics) -> str:
    """
    Format a correlation with confidence interval.

    Args:
        stat: ReplicateStatistics for correlation values

    Returns:
        Formatted string like "r = -0.45 (95% CI [-0.52, -0.38])"
    """
    if np.isnan(stat.mean):
        return "r = N/A"

    return f"r = {stat.mean:.3f} (95% CI [{stat.ci_lower:.3f}, {stat.ci_upper:.3f}])"


def generate_replicate_summary_report(
    results: ScenarioResults
) -> str:
    """
    Generate a summary report from replicate analysis.

    Args:
        results: ScenarioResults object

    Returns:
        Formatted text report
    """
    lines = [
        "=" * 70,
        f"REPLICATE ANALYSIS: {results.scenario_name}",
        f"N = {results.n_replicates} replicates",
        "=" * 70,
        "",
        "--- POPULATION METRICS ---",
        f"Final Population: {format_stat_with_ci(results.final_population, 0)}",
        f"Peak Population: {format_stat_with_ci(results.peak_population, 0)}",
        "",
        "--- INVESTMENT METRICS ---",
        f"Total Monuments: {format_stat_with_ci(results.total_monuments, 0)}",
        f"Total Exotic Goods: {format_stat_with_ci(results.total_exotics, 0)}",
        "",
        "--- CONFLICT & CLIMATE ---",
        f"Total Conflicts: {format_stat_with_ci(results.total_conflicts, 0)}",
        f"Drought Years: {format_stat_with_ci(results.drought_years, 1)}",
        "",
        "--- KEY CORRELATIONS ---",
        f"Construction-Climate: {format_correlation_with_ci(results.construction_climate_r)}",
        f"  (Negative = more construction during drought)",
        f"Exotic Goods-Stress: {format_correlation_with_ci(results.exotic_stress_r)}",
        f"  (Positive = more exotics during stress)",
        "",
        "=" * 70,
    ]

    return "\n".join(lines)


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
    mean_quality: float
    high_quality_population: float  # q > median
    low_quality_population: float   # q <= median


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

        # Quality-based population breakdown
        active_groups = [g for g in state.groups.values() if g.is_active]
        qualities = [g.quality for g in active_groups]
        median_q = np.median(qualities) if qualities else 0
        record['pop_high_quality'] = sum(
            g.population for g in active_groups if g.quality > median_q
        )
        record['pop_low_quality'] = sum(
            g.population for g in active_groups if g.quality <= median_q
        )
        record['mean_quality'] = np.mean(qualities) if qualities else 0
        # Add sigma and lambda if available
        record['sigma'] = getattr(state, 'sigma', 0.0)
        record['current_lambda'] = getattr(state, 'current_lambda', 0.0)

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

    # Quality-based population breakdown
    high_q_pops = []
    low_q_pops = []
    mean_qualities = []
    for state in period_states:
        active = [g for g in state.groups.values() if g.is_active]
        qualities = [g.quality for g in active]
        median_q = np.median(qualities) if qualities else 0
        high_q_pops.append(sum(g.population for g in active if g.quality > median_q))
        low_q_pops.append(sum(g.population for g in active if g.quality <= median_q))
        mean_qualities.append(np.mean(qualities) if qualities else 0)

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
        mean_quality=float(np.mean(mean_qualities)),
        high_quality_population=float(np.mean(high_q_pops)),
        low_quality_population=float(np.mean(low_q_pops)),
    )


def compare_strategies(
    history: List[SimulationState]
) -> pd.DataFrame:
    """
    Compare outcomes by quality tier (high vs low quality groups).

    Returns:
        DataFrame with quality-tier comparison metrics
    """
    if not history:
        return pd.DataFrame()

    final = history[-1]
    active = [g for g in final.groups.values() if g.is_active]
    if not active:
        return pd.DataFrame()

    qualities = [g.quality for g in active]
    median_q = np.median(qualities)

    tiers = {'high_quality': [], 'low_quality': []}
    for group in active:
        tier = 'high_quality' if group.quality > median_q else 'low_quality'
        tiers[tier].append(group)

    records = []
    for tier_name, groups in tiers.items():
        if not groups:
            continue
        record = {
            'tier': tier_name,
            'n_groups': len(groups),
            'total_population': sum(g.population for g in groups),
            'total_monuments': sum(g.monument_investment for g in groups),
            'total_exotics': sum(g.exotic_goods for g in groups),
            'total_conflicts': sum(g.cumulative_conflicts for g in groups),
            'total_deaths': sum(g.cumulative_deaths for g in groups),
            'mean_quality': float(np.mean([g.quality for g in groups])),
            'mean_partners': float(np.mean([g.exchange_partners for g in groups])),
            'pop_per_group': sum(g.population for g in groups) / len(groups),
            'monuments_per_group': sum(g.monument_investment for g in groups) / len(groups),
        }
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
        f"--- QUALITY TIER COMPARISON ---",
    ]

    if not strategy_df.empty:
        for _, row in strategy_df.iterrows():
            lines.append(f"  {row['tier']}:")
            lines.append(f"    Groups: {row['n_groups']}, Population: {row['total_population']:,}")
            lines.append(f"    Monuments: {row['total_monuments']:.0f}, Exotics: {row['total_exotics']}")
            lines.append(f"    Mean Quality: {row['mean_quality']:.2f}, Mean Partners: {row['mean_partners']:.1f}")

    lines.append("")
    lines.append("--- PERIOD ANALYSIS ---")

    for summary in period_summaries:
        lines.append(f"  {summary.period_name} ({summary.start_year}-{summary.end_year}):")
        lines.append(f"    Mean Pop: {summary.mean_population:,.0f} (+/- {summary.std_population:.0f})")
        lines.append(f"    Monuments: {summary.total_monument_investment:.0f}")
        lines.append(f"    Drought Years: {summary.n_drought_years}")
        lines.append(f"    Mean Quality: {summary.mean_quality:.2f}")
        lines.append(f"    High-Q Pop: {summary.high_quality_population:,.0f}, Low-Q Pop: {summary.low_quality_population:,.0f}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)
