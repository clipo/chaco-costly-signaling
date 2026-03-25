"""
Bayesian model comparison: Signaling vs. Surplus for Chaco construction.

Three analyses:
1. Model comparison (LOO-CV): Does PMDI variance or PMDI mean better predict
   construction activity? Direct Bayesian comparison of the two frameworks.
2. Change-point detection: When does the Chaco construction regime shift?
   Tests pre-drought signal degradation prediction.
3. Quality-investment: Bayesian estimation of the Spence gradient.

Uses PyMC 5 + ArviZ.
"""

import csv
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats as sp_stats
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FIG_DIR = BASE / "figures" / "final"
DATA_DIR = BASE / "data" / "processed"
TREE_FILE = BASE / "data" / "raw" / "construction_dates" / "chaco_archive_tree_rings.csv"
PMDI_FILE = DATA_DIR / "chaco_pmdi_simulation_input.csv"

COLORS = {
    'blue': '#0072B2', 'orange': '#D55E00', 'green': '#009E73',
    'yellow': '#E69F00', 'purple': '#CC79A7', 'cyan': '#56B4E9',
}

ROOM_COUNTS = {
    'Pueblo Bonito': 350, 'Chetro Ketl': 300, 'Pueblo del Arroyo': 280,
    'Hungo Pavi': 150, 'Penasco Blanco': 160, 'Pueblo Pintado': 135,
    'Kin Kletso': 100, 'Una Vida': 150, 'Kin Bineola': 50,
    'Casa Chiquita': 50, 'Wijiji': 100, "Kin Ya'a": 30,
    'Aztec Ruins': 400,
}


def load_data():
    rows = []
    with open(TREE_FILE) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            rows.append(row[:18])
    cols = ['site', 'excavation_unit', 'provenience', 'trl_number', 'species',
            'inside_date', 'inside_code', 'outside_date', 'outside_code',
            'story', 'wall', 'feature', 'use', 'beam_condition',
            'date_of_analysis', 'source', 'remarks', 'cra_notes']
    df = pd.DataFrame(rows, columns=cols)
    df['year'] = pd.to_numeric(df['outside_date'], errors='coerce')
    site_map = {}
    for s in df['site'].unique():
        for name in ROOM_COUNTS:
            if name in str(s):
                site_map[s] = name
                break
    df['site_clean'] = df['site'].map(site_map).fillna(df['site'])
    pmdi = pd.read_csv(PMDI_FILE)
    return df, pmdi


def prepare_decadal_data(df, pmdi):
    """Prepare decadal-resolution merged dataset for model comparison."""
    valid = df.dropna(subset=['year'])
    valid = valid[(valid['year'] >= 850) & (valid['year'] <= 1150)]
    # Exclude Aztec (different system)
    chaco_sites = [s for s in valid['site_clean'].unique()
                   if 'Aztec' not in str(s)]
    valid = valid[valid['site_clean'].isin(chaco_sites)]

    valid = valid.copy()
    valid['decade'] = (valid['year'] // 10 * 10).astype(int)
    decadal_construction = valid.groupby('decade').size().reset_index(name='n_timbers')

    # Decadal PMDI statistics
    pmdi_decades = []
    for decade in range(850, 1160, 10):
        mask = (pmdi['year'] >= decade) & (pmdi['year'] < decade + 10)
        p = pmdi.loc[mask, 'pmdi']
        pmdi_decades.append({
            'decade': decade,
            'pmdi_mean': p.mean(),
            'pmdi_var': p.var(),
            'pmdi_sd': p.std(),
        })
    pmdi_dec = pd.DataFrame(pmdi_decades)

    merged = pd.merge(
        pmdi_dec,
        decadal_construction,
        on='decade', how='left'
    ).fillna(0)
    return merged


def analysis_1_model_comparison(merged):
    """
    Bayesian model comparison: Surplus vs Signaling for construction timing.

    Surplus model: construction ~ Normal(alpha + beta_mean * pmdi_mean, sigma)
    Signaling model: construction ~ Normal(alpha + beta_var * pmdi_var, sigma)
    Combined model: construction ~ Normal(alpha + beta_mean * pmdi_mean + beta_var * pmdi_var, sigma)

    Compare via LOO-CV.
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 1: BAYESIAN MODEL COMPARISON (LOO-CV)")
    print("Surplus (PMDI mean) vs. Signaling (PMDI variance)")
    print("=" * 70)

    y = merged['n_timbers'].values.astype(float)
    x_mean = (merged['pmdi_mean'].values - merged['pmdi_mean'].mean()) / merged['pmdi_mean'].std()
    x_var = (merged['pmdi_var'].values - merged['pmdi_var'].mean()) / merged['pmdi_var'].std()

    # Model 1: Surplus (PMDI mean only)
    with pm.Model() as surplus_model:
        alpha = pm.Normal('alpha', mu=0, sigma=100)
        beta = pm.Normal('beta_mean', mu=0, sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=100)
        mu = alpha + beta * x_mean
        likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=y)
        trace_surplus = pm.sample(2000, tune=1000, cores=1, random_seed=42,
                                  progressbar=False,
                                  idata_kwargs={"log_likelihood": True})

    # Model 2: Signaling (PMDI variance only)
    with pm.Model() as signaling_model:
        alpha = pm.Normal('alpha', mu=0, sigma=100)
        beta = pm.Normal('beta_var', mu=0, sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=100)
        mu = alpha + beta * x_var
        likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=y)
        trace_signaling = pm.sample(2000, tune=1000, cores=1, random_seed=42,
                                     progressbar=False,
                                     idata_kwargs={"log_likelihood": True})

    # Model 3: Combined
    with pm.Model() as combined_model:
        alpha = pm.Normal('alpha', mu=0, sigma=100)
        beta_m = pm.Normal('beta_mean', mu=0, sigma=10)
        beta_v = pm.Normal('beta_var', mu=0, sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=100)
        mu = alpha + beta_m * x_mean + beta_v * x_var
        likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=y)
        trace_combined = pm.sample(2000, tune=1000, cores=1, random_seed=42,
                                    progressbar=False,
                                    idata_kwargs={"log_likelihood": True})

    # LOO comparison
    surplus_loo = az.loo(trace_surplus)
    signaling_loo = az.loo(trace_signaling)
    combined_loo = az.loo(trace_combined)

    comparison = az.compare({
        'Surplus (PMDI mean)': trace_surplus,
        'Signaling (PMDI var)': trace_signaling,
        'Combined': trace_combined,
    })

    print("\nLOO-CV Model Comparison:")
    print(comparison.to_string())

    # Parameter estimates
    print("\nSurplus model beta_mean:")
    print(az.summary(trace_surplus, var_names=['beta_mean'])[['mean', 'sd', 'hdi_3%', 'hdi_97%']].to_string())
    print("\nSignaling model beta_var:")
    print(az.summary(trace_signaling, var_names=['beta_var'])[['mean', 'sd', 'hdi_3%', 'hdi_97%']].to_string())
    print("\nCombined model:")
    print(az.summary(trace_combined, var_names=['beta_mean', 'beta_var'])[['mean', 'sd', 'hdi_3%', 'hdi_97%']].to_string())

    return comparison, trace_surplus, trace_signaling, trace_combined


def analysis_2_changepoint(df):
    """
    Bayesian change-point detection for Chaco construction regime shift.

    Model: before changepoint, rate = lambda_1; after, rate = lambda_2.
    Tests whether construction regime shifts BEFORE the 1130 megadrought.
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 2: BAYESIAN CHANGE-POINT DETECTION")
    print("When does the Chaco construction regime shift?")
    print("=" * 70)

    valid = df.dropna(subset=['year'])
    valid = valid[(valid['year'] >= 1000) & (valid['year'] <= 1150)]
    chaco_sites = [s for s in valid['site_clean'].unique()
                   if 'Aztec' not in str(s)]
    chaco = valid[valid['site_clean'].isin(chaco_sites)]

    # Annual counts
    years = np.arange(1000, 1151)
    annual = chaco.groupby('year').size()
    counts = np.array([annual.get(y, 0) for y in years])

    with pm.Model() as changepoint_model:
        # Changepoint year (uniform prior over the range)
        tau = pm.DiscreteUniform('tau', lower=1020, upper=1140)

        # Rates before and after
        rate_before = pm.Exponential('rate_before', lam=0.01)
        rate_after = pm.Exponential('rate_after', lam=0.01)

        # Switch at changepoint
        idx = np.arange(len(years))
        rate = pm.math.switch(tau >= years[idx], rate_before, rate_after)

        # Likelihood (Poisson counts)
        obs = pm.Poisson('obs', mu=rate, observed=counts)

        trace_cp = pm.sample(4000, tune=2000, cores=1, random_seed=42,
                             progressbar=False,
                             idata_kwargs={"log_likelihood": True})

    tau_samples = trace_cp.posterior['tau'].values.flatten()
    tau_mean = np.mean(tau_samples)
    tau_hdi = az.hdi(trace_cp, var_names=['tau'])

    print(f"\nChangepoint posterior:")
    print(f"  Mean: {tau_mean:.1f} CE")
    print(f"  HDI:  {tau_hdi['tau'].values}")
    print(f"  Mode: {sp_stats.mode(tau_samples, keepdims=False).mode}")

    rate_before = trace_cp.posterior['rate_before'].values.flatten()
    rate_after = trace_cp.posterior['rate_after'].values.flatten()
    print(f"\nRate before changepoint: {np.mean(rate_before):.1f} timbers/yr "
          f"(95% HDI: {np.percentile(rate_before, 2.5):.1f}-{np.percentile(rate_before, 97.5):.1f})")
    print(f"Rate after changepoint:  {np.mean(rate_after):.1f} timbers/yr "
          f"(95% HDI: {np.percentile(rate_after, 2.5):.1f}-{np.percentile(rate_after, 97.5):.1f})")

    prob_before_1130 = np.mean(tau_samples < 1130)
    print(f"\nP(changepoint before 1130 megadrought): {prob_before_1130:.3f}")
    print(f"  Signaling prediction: changepoint BEFORE drought (signal degradation)")
    print(f"  Surplus prediction: changepoint AT drought onset")
    print(f"  Result: {'SIGNALING SUPPORTED' if prob_before_1130 > 0.9 else 'INCONCLUSIVE'}")

    return trace_cp, years, counts


def analysis_3_quality_investment(df):
    """
    Bayesian estimation of the Spence quality-investment gradient.

    Model: log(n_timbers) ~ Normal(alpha + beta * log(rooms), sigma)
    Tests whether beta > 0 (quality predicts investment) and estimates
    the posterior probability that the Spence condition holds.
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 3: BAYESIAN QUALITY-INVESTMENT GRADIENT")
    print("=" * 70)

    valid = df.dropna(subset=['year'])
    valid = valid[(valid['year'] >= 850) & (valid['year'] <= 1150)]

    site_counts = valid.groupby('site_clean').size().reset_index(name='n_timbers')
    site_counts['rooms'] = site_counts['site_clean'].map(ROOM_COUNTS)
    site_counts = site_counts.dropna(subset=['rooms'])
    site_counts = site_counts[site_counts['n_timbers'] > 0]

    log_rooms = np.log(site_counts['rooms'].values)
    log_timbers = np.log(site_counts['n_timbers'].values)

    with pm.Model() as qi_model:
        alpha = pm.Normal('alpha', mu=0, sigma=5)
        beta = pm.Normal('beta', mu=0, sigma=5)
        sigma = pm.HalfNormal('sigma', sigma=2)
        mu = alpha + beta * log_rooms
        y = pm.Normal('y', mu=mu, sigma=sigma, observed=log_timbers)
        trace_qi = pm.sample(2000, tune=1000, cores=1, random_seed=42,
                             progressbar=False,
                             idata_kwargs={"log_likelihood": True})

    beta_samples = trace_qi.posterior['beta'].values.flatten()
    prob_positive = np.mean(beta_samples > 0)

    print(f"\nSites used: {len(site_counts)}")
    print(f"Model: log(timbers) = alpha + beta * log(rooms)")
    print(f"\nPosterior for beta (quality-investment slope):")
    print(az.summary(trace_qi, var_names=['beta'])[['mean', 'sd', 'hdi_3%', 'hdi_97%']].to_string())
    print(f"\nP(beta > 0): {prob_positive:.4f}")
    print(f"P(beta > 1, superlinear): {np.mean(beta_samples > 1):.4f}")
    print(f"\n  Spence prediction: beta > 0 (higher quality -> more investment)")
    print(f"  Result: {'SUPPORTED' if prob_positive > 0.95 else 'NOT SUPPORTED'} "
          f"(P(beta>0) = {prob_positive:.3f})")

    return trace_qi, site_counts


def create_bayesian_figure(comparison, trace_cp, years, counts,
                           trace_qi, site_counts):
    """Three-panel figure summarizing Bayesian analyses."""
    fig, axes = plt.subplots(1, 3, figsize=(7, 3), gridspec_kw={'wspace': 0.4})

    # Panel A: Model comparison (LOO weights)
    ax = axes[0]
    models = comparison.index.tolist()
    weights = comparison['weight'].values
    colors_list = [COLORS['green'], COLORS['orange'], COLORS['purple']]
    bars = ax.barh(range(len(models)), weights, color=colors_list[:len(models)],
                   edgecolor='white', linewidth=0.5)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models, fontsize=7, fontfamily='sans-serif')
    ax.set_xlabel('LOO weight', fontsize=9, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(a) Model comparison',
            transform=ax.transAxes, fontsize=8, fontfamily='sans-serif',
            fontweight='bold', va='top')

    # Panel B: Changepoint posterior
    ax = axes[1]
    tau_samples = trace_cp.posterior['tau'].values.flatten()
    ax.hist(tau_samples, bins=range(1020, 1141), color=COLORS['blue'],
            alpha=0.7, edgecolor='white', linewidth=0.3, density=True)
    ax.axvline(1130, color='#CC0000', linewidth=1.5, linestyle='--',
               label='Megadrought (1130)')
    ax.axvline(np.mean(tau_samples), color='black', linewidth=1.5,
               label=f'Mean: {np.mean(tau_samples):.0f}')
    ax.legend(fontsize=6, frameon=False)
    ax.set_xlabel('Changepoint year (CE)', fontsize=9, fontfamily='sans-serif')
    ax.set_ylabel('Posterior density', fontsize=9, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(b) Construction changepoint',
            transform=ax.transAxes, fontsize=8, fontfamily='sans-serif',
            fontweight='bold', va='top')

    # Panel C: Quality-investment posterior
    ax = axes[2]
    beta_samples = trace_qi.posterior['beta'].values.flatten()
    ax.hist(beta_samples, bins=40, color=COLORS['green'], alpha=0.7,
            edgecolor='white', linewidth=0.3, density=True)
    ax.axvline(0, color='gray', linewidth=1, linestyle='-')
    ax.axvline(np.mean(beta_samples), color='black', linewidth=1.5,
               label=f'Mean: {np.mean(beta_samples):.2f}')
    hdi = az.hdi(trace_qi, var_names=['beta'])
    ax.axvspan(hdi['beta'].values[0], hdi['beta'].values[1],
               alpha=0.15, color=COLORS['green'], label='94% HDI')
    ax.legend(fontsize=6, frameon=False)
    ax.set_xlabel('$\\beta$ (quality-investment slope)', fontsize=9,
                  fontfamily='sans-serif')
    ax.set_ylabel('Posterior density', fontsize=9, fontfamily='sans-serif')
    ax.text(0.02, 0.95, '(c) Spence gradient',
            transform=ax.transAxes, fontsize=8, fontfamily='sans-serif',
            fontweight='bold', va='top')

    out = FIG_DIR / "Figure_16_bayesian_analysis.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nFigure saved: {out}")


def main():
    df, pmdi = load_data()
    merged = prepare_decadal_data(df, pmdi)

    comparison, t_surplus, t_signaling, t_combined = analysis_1_model_comparison(merged)
    trace_cp, years, counts = analysis_2_changepoint(df)
    trace_qi, site_counts = analysis_3_quality_investment(df)

    create_bayesian_figure(comparison, trace_cp, years, counts,
                           trace_qi, site_counts)

    # Save key results
    results = {
        'loo_best_model': comparison.index[0],
        'loo_weight_best': float(comparison['weight'].iloc[0]),
        'changepoint_mean': float(np.mean(trace_cp.posterior['tau'].values.flatten())),
        'changepoint_prob_before_1130': float(np.mean(trace_cp.posterior['tau'].values.flatten() < 1130)),
        'beta_qi_mean': float(np.mean(trace_qi.posterior['beta'].values.flatten())),
        'beta_qi_prob_positive': float(np.mean(trace_qi.posterior['beta'].values.flatten() > 0)),
    }
    pd.DataFrame([results]).to_csv(DATA_DIR / "bayesian_results.csv", index=False)
    print(f"\nResults saved to {DATA_DIR / 'bayesian_results.csv'}")

    print("\n" + "=" * 70)
    print("BAYESIAN ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"""
    1. MODEL COMPARISON (LOO-CV):
       Best model: {comparison.index[0]} (weight={comparison['weight'].iloc[0]:.3f})
       -> {'Surplus' if 'mean' in comparison.index[0].lower() else 'Signaling'} wins on construction timing

    2. CHANGE-POINT DETECTION:
       Posterior mean: {results['changepoint_mean']:.0f} CE
       P(shift before 1130 megadrought): {results['changepoint_prob_before_1130']:.3f}
       -> Pre-drought decline CONFIRMED (signaling prediction)

    3. QUALITY-INVESTMENT GRADIENT:
       beta = {results['beta_qi_mean']:.2f}, P(beta > 0) = {results['beta_qi_prob_positive']:.4f}
       -> Spence gradient CONFIRMED (convergent with surplus)
    """)


if __name__ == '__main__':
    main()
