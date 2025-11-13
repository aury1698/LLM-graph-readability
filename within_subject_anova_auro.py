import os
import pandas as pd
import numpy as np

# Added imports for non parametric tests: do we want to use wilcoxon or nemenyi?
from scipy.stats import (
    norm, probplot, shapiro, ttest_rel, 
    friedmanchisquare, wilcoxon
)
from statsmodels.stats.anova import AnovaResults, AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
from itertools import combinations


BASE_PATH = "layout_algorithms_performance"

RESULTS_DIR = os.path.join(BASE_PATH, "results")
MODELS_TO_LOAD = ["gemini-2.5-flash", "mistral-small-3.1-24b", "gpt-5", "glm-4.5v-106b"]
SHOT_TYPES = ["zero_shot", "few_shot"]
COT_TYPES = ["cot", "no_cot"]


def load_and_aggregate_results():
    """Loads all individual CSVs into one master DataFrame."""
    all_data_frames = []

    for model in MODELS_TO_LOAD:
        for shot in SHOT_TYPES:
            for cot in COT_TYPES:
                config_path = os.path.join(RESULTS_DIR, model, shot, cot)

                if not os.path.isdir(config_path):
                    continue

                for f in os.listdir(config_path):
                    if f.startswith("results_attempt_") and f.endswith(".csv"):
                        file_path = os.path.join(config_path, f)
                        df = pd.read_csv(file_path)
                        all_data_frames.append(df)

    if not all_data_frames:
        print(f"Warning: no csv files found in {RESULTS_DIR}")
        return pd.DataFrame()

    return pd.concat(all_data_frames, ignore_index=True)


def pre_transform(df: pd.DataFrame):
    """
    (Aurora's "rich" pre-transform)
    Cleans data, renames columns, calculates 'Error', 
    and creates the 'Subject' identifier upfront.
    """
    df = df.copy()
    
    df.rename(columns={"Model Name": "Model"}, inplace=True)
    df.rename(columns={"LLM Mode": "Shots"}, inplace=True)
    df.rename(columns={"COT Mode": "Cot"}, inplace=True)
    df.rename(columns={"Output Tokens": "Output_Tokens"}, inplace=True)
    
    df["Layout"] = df["Layout"].str.split("_").str[0]
    df["Correct"] = (
        df["Correct Prediction (True/False)"]
        .astype(str)
        .apply(lambda x: 1 if x.strip() == "True" else 0)
    )
    
    # Create the 'Error' metric (1=Error, 0=Correct)
    df["Error"] = 1 - df["Correct"]
    
    # Create the 'Subject' (N=16) - this is the "participant"
    df["Subject"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )
    
    # Drop original columns not needed for analysis
    df = df.drop(columns=["Correct Prediction (True/False)", "Correct"])
    
    return df


def check_normality(df: pd.DataFrame, dv="Error"):
    """
    Checks normality using Shapiro-Wilk, Q-Q Plot, and Histogram.
    This function matches Bastian's checks.
    Returns True if data appears normal, False otherwise.
    """
    # Aggregate data to get one value per subject/layout
    df_agg = df.groupby(["Subject", "Layout"], as_index=False)[dv].mean()
    
    print(f"\n--- Normality Check for {dv} --- \n")
    
    data = df_agg[dv].dropna()
    if data.empty or len(data) < 3:
        print(f"No data for {dv} to check.")
        return False  # Cannot be normal if no data
    
    # Visual inspections 
    # 1. Q-Q Plot
    plt.figure()
    probplot(data, dist="norm", plot=plt)
    plt.title(f"Q-Q Plot for {dv}")
    qq_plot_filename = f"qq_plot_{dv}.png"
    plt.savefig(qq_plot_filename)
    # print(f"Saving Q-Q plot to {qq_plot_filename}")
    plt.show() 
    plt.close()

    # 2. Histogram 
    plt.figure()
    mu, sigma = data.mean(), data.std(ddof=0)
    
    padding = 0.1 * (data.max() - data.min() if data.max() != data.min() else 1.0)
    if np.isnan(padding) or padding == 0: 
        padding = 1.0
    
    xs_min = data.min() - padding
    xs_max = data.max() + padding

    if np.isnan(xs_min) or np.isnan(xs_max):
        print("Cannot generate linspace, invalid min/max/padding. Using fallback.")
        xs = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 200)
    else:
        xs = np.linspace(xs_min, xs_max, 200)

    plt.hist(data, bins=20, density=True, alpha=0.6, color="C0", edgecolor="k")
    plt.plot(xs, norm.pdf(xs, loc=mu, scale=sigma), "r-", lw=2, label=f"Normal PDF (μ={mu:.3f}, σ={sigma:.3f})")
    plt.title(f"Histogram of {dv} mean with normal curve")
    plt.xlabel(f"Mean {dv}")
    plt.ylabel("Density")
    plt.legend()
    plot_filename = f"normality_plot_{dv}.png"
    plt.savefig(plot_filename)
    # print(f"Saving normality plot to {plot_filename}")
    plt.show() 
    plt.close()

    # Global Shapiro-Wilk Normality Check
    try:
        stat, p = shapiro(data)
        print(f"Global Normality Check (Shapiro-Wilk): \n W={stat:.3f}, p={p:.3f}{'     <--- NOT NORMAL' if p < 0.05 else ''}\n")
        is_global_normal = p > 0.05
    except Exception as e:
        print(f"Global Shapiro Error: {e}")
        return False  # Cannot proceed

    # Per-Group (Layout) Normality Check
    all_groups_normal = True
    print("Per-Layout Normality Check (Shapiro-Wilk):\n")
    for cond, subset in df_agg.groupby("Layout"):
        subset_data = subset[dv].dropna()
        if len(subset_data) < 3:
            print(f"{cond}: SKIPPED (insufficient data, N={len(subset_data)})")
            continue
        stat, p = shapiro(subset_data)
        print(f"{cond}: W={stat:.3f}, p={p:.3f}{'     <--- NOT NORMAL' if p < 0.05 else ''}\n")
        if p < 0.05:
            all_groups_normal = False
            
    if is_global_normal and all_groups_normal:
        print(f"-> RESULT: Data for {dv} appears sufficiently normal for parametric tests.")
        return True
    else:
        print(f"-> RESULT: Data for {dv} VIOLATES normality assumptions.")
        return False


def run_parametric_post_hoc(df: pd.DataFrame, dv="Error", alpha=0.05):
    """
    Performs PARAMETRIC post-hoc tests (paired t-tests + Holm correction).
    This replicates the "Tukey's WSD" logic from the paper.
    """
    print(f"\n--- Parametric Post-Hoc for {dv} (Paired T-tests + Holm Correction) ---")
    
    df_agg = df.groupby(["Subject", "Layout"], as_index=False)[dv].mean()
    df_wide = df_agg.pivot(index="Subject", columns="Layout", values=dv)
    
    layouts = df_wide.columns
    comparisons = list(combinations(layouts, 2))
    p_values = []
    results = []

    for layout_a, layout_b in comparisons:
        data_a = df_wide[layout_a]
        data_b = df_wide[layout_b]
        
        common_data = pd.concat([data_a, data_b], axis=1, keys=['a', 'b']).dropna()
        
        if len(common_data) < 2:
            print(f"Skipping {layout_a} vs {layout_b}: insufficient paired data")
            continue
            
        stat, p = ttest_rel(common_data['a'], common_data['b'])  # Paired T-test
        p_values.append(p)
        results.append((layout_a, layout_b, stat, p))

    if not p_values:
        print("No post-hoc comparisons were performed.")
        return

    reject, p_values_corrected, _, _ = multipletests(p_values, alpha=alpha, method='holm')
    
    print("Layout A       | Layout B       |   T-Stat |   p-unc | p-adj (Holm) | Significant")
    print("-" * 75)
    for i, (layout_a, layout_b, stat, p) in enumerate(results):
        sig_str = "YES" if reject[i] else "no"
        print(f"{layout_a:<14} | {layout_b:<14} | {stat:>8.3f} | {p:>6.3f} | {p_values_corrected[i]:>12.3f} | {sig_str}")


def run_non_parametric_post_hoc(df: pd.DataFrame, dv="Error", alpha=0.05):
    """
    Performs NON-PARAMETRIC post-hoc tests (Wilcoxon + Bonferroni correction).
    """
    print(f"\n--- Non-Parametric Post-Hoc for {dv} (Wilcoxon + Bonferroni Correction) ---")
    
    df_agg = df.groupby(["Subject", "Layout"], as_index=False)[dv].mean()
    df_wide = df_agg.pivot(index="Subject", columns="Layout", values=dv)
    
    layouts = df_wide.columns
    comparisons = list(combinations(layouts, 2))
    p_values = []
    results = []

    for layout_a, layout_b in comparisons:
        data_a = df_wide[layout_a]
        data_b = df_wide[layout_b]
        
        common_data = pd.concat([data_a, data_b], axis=1, keys=['a', 'b']).dropna()
        
        if len(common_data) < 2:
            print(f"Skipping {layout_a} vs {layout_b}: insufficient paired data")
            continue
            
        # Wilcoxon signed-rank test for paired samples --> should it be Nemenyi instead?
        try:
            stat, p = wilcoxon(common_data['a'], common_data['b'], zero_method='wilcox')
        except ValueError:
            # This can happen if all differences are zero,
            # in which case p=1.0 and stat=0 (or NaN)
            stat, p = 0.0, 1.0

        p_values.append(p)
        results.append((layout_a, layout_b, stat, p))

    if not p_values:
        print("No post-hoc comparisons were performed.")
        return

    # Use Bonferroni correction, which is more standard (and conservative)
    # for non-parametric post-hocs like this.
    reject, p_values_corrected, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')
    
    print("Layout A       | Layout B       |   W-Stat |   p-unc | p-adj (Bonf) | Significant")
    print("-" * 75)
    for i, (layout_a, layout_b, stat, p) in enumerate(results):
        sig_str = "YES" if reject[i] else "no"
        print(f"{layout_a:<14} | {layout_b:<14} | {stat:>8.3f} | {p:>6.3f} | {p_values_corrected[i]:>12.3f} | {sig_str}")


def run_main_parametric_analysis(df: pd.DataFrame):
    """
    Runs the main PARAMETRIC analysis (ANOVA), replicating Section 3 of the paper.
    This is run regardless of normality, to match Purchase & Bastian.
    """
    print("\n\n" + "=" * 80)
    print("STEP 2: PARAMETRIC ANALYSIS (REPLICATING PAPER)")
    print("        (ANOVA is run regardless of normality)")
    print("=" * 80)

    # --- Analysis for Error ---
    print("\n--- Main Effect of Layout on Error (ANOVA) ---")
    try:
        aov_error = AnovaRM(
            data=df,
            depvar="Error",
            subject="Subject",
            within=["Layout"],
            aggregate_func="mean",  # Automatically aggregates the 3 questions
        ).fit()
        print(aov_error)
        error_p_value = aov_error.anova_table["Pr > F"].iloc[0]
    except Exception as e:
        print(f"Error during AnovaRM for Error: {e}")
        error_p_value = 1.0  # Set to 1 to skip post-hoc

    # --- Analysis for Output Tokens (Response Time) ---
    print("\n--- Main Effect of Layout on Output_Tokens (ANOVA) ---")
    try:
        aov_tokens = AnovaRM(
            data=df,
            depvar="Output_Tokens",
            subject="Subject",
            within=["Layout"],
            aggregate_func="mean",
        ).fit()
        print(aov_tokens)
        tokens_p_value = aov_tokens.anova_table["Pr > F"].iloc[0]
    except Exception as e:
        print(f"Error during AnovaRM for Output_Tokens: {e}")
        tokens_p_value = 1.0  # Set to 1 to skip post-hoc

    # --- Post-Hoc Analysis ---
    print("\n" + "=" * 80)
    print("STEP 3: PARAMETRIC POST-HOC (Tukey/T-test)")
    print("=" * 80)
    
    if error_p_value < 0.05:
        print(f"Parametric main effect for Error is significant (p={error_p_value:.4f}).")
        run_parametric_post_hoc(df, dv="Error")
    else:
        print(f"No significant parametric main effect for Error (p={error_p_value:.4f}). Skipping post-hoc.")
        
    if tokens_p_value < 0.05:
        print(f"\nParametric main effect for Output_Tokens is significant (p={tokens_p_value:.4f}).")
        run_parametric_post_hoc(df, dv="Output_Tokens")
    else:
        print(f"\nNo significant parametric main effect for Output_Tokens (p={tokens_p_value:.4f}). Skipping post-hoc.")


def run_non_parametric_analysis(df: pd.DataFrame, dv="Error"):
    """
    Runs the NON-PARAMETRIC main analysis (Friedman Test).
    """
    print(f"\n--- Non-Parametric Main Effect of Layout on {dv} (Friedman Test) ---")
    
    # it seems that Friedman test requires wide-form data (one column per condition)
    df_agg = df.groupby(["Subject", "Layout"], as_index=False)[dv].mean()
    df_wide = df_agg.pivot(index="Subject", columns="Layout", values=dv)
    
    # Friedman in scipy cannot handle any missing data
    df_wide_clean = df_wide.dropna()
    
    if len(df_wide_clean) < 2:
        print(f"Skipping Friedman test for {dv}: not enough complete subjects (N={len(df_wide_clean)}).")
        return

    print(f"(Running Friedman on {len(df_wide_clean)} complete subjects)")

    # Unpack the columns as separate arguments
    try:
        stat, p = friedmanchisquare(*[df_wide_clean[col] for col in df_wide_clean.columns])
        print(f"Friedman Test for {dv}: Chi-Squared = {stat:.3f}, p = {p:.4f}")
        
        if p < 0.05:
            print(f"Non-parametric main effect for {dv} is significant. Running post-hoc.")
            run_non_parametric_post_hoc(df, dv=dv)
        else:
            print(f"No significant non-parametric main effect for {dv}. Skipping post-hoc.")
    except Exception as e:
        print(f"Error during Friedman test for {dv}: {e}")


def pairwise_comparison(df: pd.DataFrame, dv="Error", alpha=0.05):
    """
    Runs the classic Tukey's HSD post-hoc test.
    """
    print(f"\n--- Classic Tukey HSD Post-Hoc for {dv} ---")
    df = df.copy()
    
    df_agg = df.groupby(["Subject", "Layout"], as_index=False)[dv].mean()

    try:
        tukey_results = pairwise_tukeyhsd(
            endog=df_agg[dv],        
            groups=df_agg["Layout"],
            alpha=alpha
        )
        
        print(f"\nTukey HSD Results for {dv}:\n")
        print(tukey_results.summary())
        
    except Exception as e:
        print(f"Error running Tukey HSD: {e}")


# NEW: save wide-format CSV for R analysis like bastian
def save_wide_format_for_R(df: pd.DataFrame, dv="Error"):
    """
    Aggregates data and pivots to a single wide-format CSV 
    for the R script (tukeySEM).
    
    This version creates ONE file with ALL layouts as columns,
    as required by the "Performance of Layout Algorithms" paper.
    """
    print(f"\n--- Saving Wide-Format CSV for R ({dv}) ---")
    
    df_agg = df.groupby(["Subject", "Layout"], as_index=False)[dv].mean()

    
    try:
        # Index: Subject
        # Columns: the 8 Layouts
        # Values: error means
        df_wide = df_agg.pivot(index="Subject", columns="Layout", values=dv)
        
        filename = f"{dv.lower()}_per_subject_all_layouts.csv"
        out_path = os.path.join("./", filename) 
        
        df_wide.to_csv(out_path, index=False)
        
        print(f"Successfully saved wide-format data to: {out_path}")
        print(f"You can now use this file in the R script for Tukey.")

    except Exception as e:
        print(f"Error pivoting or saving wide format: {e}")


if __name__ == "__main__":
    master_data_frame = load_and_aggregate_results()
    
    if isinstance(master_data_frame, pd.DataFrame) and not master_data_frame.empty:
        
        # Transform (clean) the data, create Subjects
        df_transformed = pre_transform(master_data_frame)
        
        # Check statistical assumptions (Normality)
        print("=" * 80)
        print("STEP 1: CHECKING ASSUMPTIONS (NORMALITY)")
        print("=" * 80)
        
        is_error_normal = check_normality(df_transformed.copy(), dv="Error")
        is_tokens_normal = check_normality(df_transformed.copy(), dv="Output_Tokens")
        
        # Run the main PARAMETRIC analyses (ANOVA + Post-Hoc)
        #     (This is run ALWAYS to replicate the paper--> is it correct tho?)
        run_main_parametric_analysis(df_transformed.copy())
        
        # Run the NON-PARAMETRIC fallback tests
        # (This is run ONLY if normality was VIOLATED)
        print("\n\n" + "=" * 80)
        print("STEP 4: NON-PARAMETRIC FALLBACK ANALYSIS")
        print("=" * 80)
        
        if not is_error_normal:
            print("-> Normality violated for Error. Running non-parametric tests.")
            run_non_parametric_analysis(df_transformed.copy(), dv="Error")
        else:
            print("-> Normality met for Error. Non-parametric test skipped.")
            
        if not is_tokens_normal:
            print("\n-> Normality violated for Output_Tokens. Running non-parametric tests.")
            run_non_parametric_analysis(df_transformed.copy(), dv="Output_Tokens")
        else:
            print("\n-> Normality met for Output_Tokens. Non-parametric test skipped.")


        # NEW: RUN TUKEY HSD POST-HOC ---
        print("\n\n" + "=" * 80)
        print("STEP 5: TUKEY HSD PAIRWISE COMPARISONS")
        print("=" * 80)
        
        # Run the Tukey HSD test for the 'Error' variable
        pairwise_comparison(df_transformed.copy(), dv="Error")

        # New: save wide-format CSV for R analysis
        print("\n\n" + "=" * 80)
        print("STEP 6: EXPORTING DATA FOR R (TukeySEM)")
        print("=" * 80)
        save_wide_format_for_R(df_transformed.copy(), dv="Error")
        
        print("\n\n" + "=" * 80)
        print("Analysis complete.")
        print("=" * 80)
        
    else:
        print(f"Error: No data loaded. Check path: {RESULTS_DIR}")