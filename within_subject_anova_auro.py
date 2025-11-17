import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Import for parametric tests (Purchase's replication)
from statsmodels.stats.anova import AnovaResults, AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Import for non-parametric tests (Our correct analysis)
from scipy.stats import (
    norm, probplot, shapiro, 
    friedmanchisquare, wilcoxon
)
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm


BASE_PATH = "layout_algorithms_performance"

RESULTS_DIR = os.path.join(BASE_PATH, "results")
MODELS_TO_LOAD = ["gemini-2.5-flash", "mistral-small-3.1-24b", "gpt-5", "glm-4.5v-106b"]
SHOT_TYPES = ["zero_shot", "few_shot"]
COT_TYPES = ["cot", "no_cot"]


def load_and_aggregate_results():
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


def pre_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Required as the Anova library does not/cannot handle column names with spaces.
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
    # as we want error rate and not accuracy
    df["Error"] = 1 - df["Correct"]
    df = df.drop(columns=["Correct Prediction (True/False)", "Correct"])

    df["Subject"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )

    return df


def error_rate_for_subjects(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates the 'Subject' ID and aggregates by Subject and Layout.
    """
    df = df.copy()
    
    # per task normal distribution
    # df = df[df["Task"].astype(str).str.startswith("task1", na=False)]

    agg = df.groupby(["Subject", "Layout"], as_index=False).agg(
        mean_error_rate=("Error", "mean"),
        mean_output_tokens=("Output_Tokens", "mean"),
    )
    return pd.DataFrame(agg)


def save_wide_csv(df_agg: pd.DataFrame):
    """
    Saves the aggregated data in wide format (one row per subject).
    """
    df_wide_error = df_agg.pivot(
        index="Subject", columns="Layout", values="mean_error_rate"
    )
    filename_err = "error_rate_per_subject_task3_layouts_auro.csv"  # CHANGE HERE IF FILTERING BY TASK IS ACTIVE (e.g.: error_rate_per_subject_task1_layouts_auro)
    out_path_err = os.path.join("./", filename_err)
    df_wide_error.to_csv(out_path_err, index=True)

    df_wide_out = df_agg.pivot(
        index="Subject", columns="Layout", values="mean_output_tokens"
    )
    filename_out = "output_tokens_per_subject_task3_layouts_auro.csv" # CHANGE HERE IF FILTERING BY TASK IS ACTIVE (e.g.: error_rate_per_subject_task1_layouts_auro)
    out_path_out = os.path.join("./", filename_out)
    df_wide_out.to_csv(out_path_out, index=True)


def plot_combined_error_rate_per_layout(df_agg: pd.DataFrame):
    """
    Creates a bar plot of the mean error rate per layout, averaged over all subjects.
    """
    agg_plot = df_agg.groupby(["Layout"], as_index=False)["mean_error_rate"].mean()
    
    plt.figure()
    plt.bar(agg_plot["Layout"], agg_plot["mean_error_rate"])
    plt.title("Mean Error Rate per Layout (All Subjects)")
    plt.xlabel("Layout Algorithm")
    plt.ylabel("Mean Error Rate")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("mean_error_rate_per_layout.png")
    plt.close()


def normality_of_error_rate(df_agg: pd.DataFrame, dv="mean_error_rate"):
    """
    Checks normality using Shapiro-Wilk, Q-Q Plot, and Histogram.
    Takes the AGGREGATED DataFrame.
    """
    print(f"\n--- Normality Check for {dv} --- \n")
    
    data = df_agg[dv].dropna()
    if data.empty or len(data) < 3:
        print(f"No data for {dv} to check.")
        return False

    # Visual inspection: decomment if needed for plots

    # probplot(data, dist="norm", plot=plt)
    # plt.title(f"Q-Q Plot for {dv}")
    # plt.show() 

    # Global Shapiro-Wilk
    stat, p = shapiro(data)
    print(f"Global Normality (Shapiro-Wilk): W={stat:.3f}, p={p:.3f}{'    <--- NOT NORMAL' if p < 0.05 else ''}\n")
    is_normal = p > 0.05

    # Per-Group Shapiro-Wilk
    print("Per-Layout Normality (Shapiro-Wilk):\n")
    for cond, subset in df_agg.groupby("Layout"):
        subset_data = subset[dv].dropna()
        if len(subset_data) < 3:
            print(f"{cond}: SKIPPED (N={len(subset_data)})")
            continue
        stat, p = shapiro(subset_data)
        print(f"{cond}: W={stat:.3f}, p={p:.3f}{'    <--- NOT NORMAL' if p < 0.05 else ''}\n")
        if p < 0.05:
            is_normal = False
            
    return is_normal


def calculate_anovaRM(df: pd.DataFrame) -> tuple[AnovaResults, AnovaResults]:
    """
    Runs the AnovaRM for both DVs (Error and Output_Tokens) at once.
    Takes the LONG (pre-transformed) DataFrame.
    """
    df = df.copy()

    # Uncomment this if you want to see the dataframe that goes into the Anova
    # print(df) 

    # Aggregation is required!
    # If the data set contains more than a single observation per subject and cell of the specified model,
    # this function will be used to aggregate the data before running the Anova.
    # An exception will be raised if aggregation is required, but no aggregation function was specified.
    return (
        AnovaRM(
            data=df,
            depvar="Error", # Tu usi 'Error', lui 'Correct'
            subject="Subject",
            within=["Layout"],
            aggregate_func="mean",
        ).fit(),
        AnovaRM(
            data=df,
            depvar="Output_Tokens",
            subject="Subject",
            within=["Layout"],
            aggregate_func="mean",
        ).fit(),
    )

def purchase_parametric_analysis(df: pd.DataFrame):
    """
    PURCHASE'S REPLICATION: Runs the main PARAMETRIC analysis (ANOVA) anyways.
    This function calls calculate_anovaRM once.
    """
    print("\n\n" + "=" * 80)
    print("Purchase's Parametric Analysis (ANOVA)")
    print("=" * 80)
    
    error_p_value = 1.0
    tokens_p_value = 1.0

    try:
        # Call the single function that returns both results
        aov_error, aov_tokens = calculate_anovaRM(df) 

        print("\n--- Main Effect of Layout on Error (ANOVA) ---")
        print(aov_error)
        error_p_value = aov_error.anova_table["Pr > F"].iloc[0]

        print("\n--- Main Effect of Layout on Output_Tokens (ANOVA) ---")
        print(aov_tokens)
        tokens_p_value = aov_tokens.anova_table["Pr > F"].iloc[0]
        
    except Exception as e:
        print(f"AnovaRM Error: {e}")
        
    return error_p_value, tokens_p_value


def purchase_pairwise_comparison(df_agg: pd.DataFrame, dv="mean_error_rate", alpha=0.05):
    """
    PURCHASE'S REPLICATION: Runs the classic Tukey's HSD post-hoc test.
    Takes the AGGREGATED DataFrame.
    """
    print(f"\n--- Parametric Post-Hoc for {dv} (Tukey HSD) ---")
    try:
        tukey_results = pairwise_tukeyhsd(
            endog=df_agg[dv],        
            groups=df_agg["Layout"],
            alpha=alpha
        )
        print(f"\nTukey HSD Results for {dv}:\n")
        print(tukey_results.summary())
    except Exception as e:
        print(f"Tukey HSD Error: {e}")

#END OF PURCHASE'S REPLICATION

#START OF OUR NON-PARAMETRIC ANALYSIS
def our_main_effect_test(df_agg: pd.DataFrame):
    """
    OUR ANALYSIS: Runs the NON-PARAMETRIC main analysis (Friedman Test).
    equivalent to bastian's `our_prioritizing_aesthetics_effect`.
    """
    print("\n\n" + "=" * 80)
    print("NON-Parametric Main Test (Friedman)")
    print("=" * 80)
    
    error_p_value = 1.0
    tokens_p_value = 1.0
    
    for dv, name in [("mean_error_rate", "Error"), ("mean_output_tokens", "Output Tokens")]:
        print(f"\n--- Friedman Test for {name} ---")
        df_wide = df_agg.pivot(index="Subject", columns="Layout", values=dv).dropna()
        
        if len(df_wide) < 2:
            print(f"Skipping Friedman: not enough complete subjects (N={len(df_wide)}).")
            continue
        
        try:
            data_to_test = [df_wide[col] for col in df_wide.columns]
            stat, p = friedmanchisquare(*data_to_test)
            print(f"Friedman Test for {name}: Chi-Squared = {stat:.3f}, p = {p:.4f}")
            if dv == "mean_error_rate": error_p_value = p
            else: tokens_p_value = p
        except Exception as e:
            print(f"Friedman Error: {e}")
            
    return error_p_value, tokens_p_value


def our_pairwise_comparison(df_agg: pd.DataFrame, dv="mean_error_rate", alpha=0.05):
    """
    OUR ANALYSIS: Performs NON-PARAMETRIC post-hoc tests (Wilcoxon + Bonferroni).
    Takes the AGGREGATED DataFrame.
    """
    print(f"\n--- NON-Parametric Post-Hoc for {dv} (Wilcoxon + Bonferroni) ---")
    
    df_wide = df_agg.pivot(index="Subject", columns="Layout", values=dv)
    comparisons = list(combinations(df_wide.columns, 2))
    p_values = []
    results = []

    for layout_a, layout_b in comparisons:
        common_data = df_wide[[layout_a, layout_b]].dropna()
        if len(common_data) < 2:
            continue
        try:
            stat, p = wilcoxon(common_data[layout_a], common_data[layout_b], zero_method='wilcox')
        except ValueError:
             stat, p = 0.0, 1.0 # All differences are zero
        p_values.append(p)
        results.append((layout_a, layout_b, stat, p))

    if not p_values:
        print("No post-hoc comparisons were performed.")
        return

    reject, p_values_corrected, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')
    
    print("Layout A       | Layout B       |   W-Stat |   p-unc | p-adj (Bonf) | Significant")
    print("-" * 75)
    for i, (layout_a, layout_b, stat, p) in enumerate(results):
        sig_str = "YES" if reject[i] else "no"
        print(f"{layout_a:<14} | {layout_b:<14} | {stat:>8.3f} | {p:>7.4f} | {p_values_corrected[i]:>12.4f} | {sig_str}")

def gee_pairwise_tests(res):
    """
    Perform pairwise Wald tests between all levels of Layout
    from a fitted GEE model. Copied from Bastian.
    """
    # Extract all layout categories used
    params = res.params
    cov = res.cov_params()

    # Parse names: baseline is usually the first alphabetical layout
    levels = []
    # The intercept represents the baseline, other params are comparisons against it
    # But to do all-vs-all we need to extract names properly.
    
    # Get variable names from the model parameters
    param_names = params.index.tolist()
    
    # Let's extract the explicit levels found in params
    explicit_levels = []
    for k in param_names:
        if k.startswith("C(Layout)[T."):
            lvl = k.split("[T.")[1].split("]")[0]
            explicit_levels.append(lvl)
    
    levels = ["(baseline)"] + explicit_levels # Placeholder name for baseline

    print("\nPairwise comparisons (GEE Wald tests:")
    print("Note: Comparisons are relative to the model's reference layout.")
    print("----------------------------------------")

    # Helper to get index
    def index_for(lvl_name):
        if lvl_name == "(baseline)":
            return None
        name = f"C(Layout)[T.{lvl_name}]"
        if name in params.index:
            return params.index.get_loc(name)
        return None

    # Generate all combinations of explicit levels
    # (Comparing everything against everything that has a coefficient)
    for a, b in combinations(explicit_levels, 2):
        ia = index_for(a)
        ib = index_for(b)

        # Contrast vector
        L = np.zeros(len(params))
        L[ia] = 1
        L[ib] = -1

        # Wald test
        diff = float(L @ params)
        var = float(L @ cov @ L.T)
        se = np.sqrt(var)
        z = diff / se
        p = 2 * (1 - norm.cdf(abs(z)))

        print(f"{a} vs {b}:  diff={diff:+.4f},  z={z:+.3f},  p={p:.4g}")
    


def our_gee_analysis(df: pd.DataFrame):
    """
    Runs GEE (Generalized Estimating Equations) analysis.
    """
    print("\n\n" + "=" * 80)
    print("OUR ANALYSIS: GEE Logistic Regression (Validation)")
    print("=" * 80)

    df = df.copy()

    if "Correct" not in df.columns:
        df["Correct"] = 1 - df["Error"]
    
    print("\n--- GEE for Error Rate (Correct ~ Layout) ---")
    
    try:
        # Family=Binomial is crucial here (Logistic Regression)
        model = sm.GEE.from_formula(
            "Correct ~ C(Layout)",
            groups="Subject",  
            data=df,
            family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable(),
        )
        res = model.fit()
        print(res.summary())
        
        # Run manual pairwise contrasts
        gee_pairwise_tests(res)
        
    except Exception as e:
        print(f"GEE Analysis failed: {e}")
        print("Note: GEE might fail if there is perfect separation (e.g., a layout has 0 errors).")



if __name__ == "__main__":

    master_data_frame = load_and_aggregate_results()
    
    if isinstance(master_data_frame, pd.DataFrame) and not master_data_frame.empty:
        
        df_pre = pre_transform(master_data_frame)

        #Comment this line to avoid filtering per task; otherwise select the task here:
        #df_pre = df_pre[df_pre["Task"].astype(str).str.startswith("task3", na=False)]

        df_agg = error_rate_for_subjects(df_pre.copy()) # use copy to be safe
        
        # --- (Utility) ---
        #save_wide_csv(df_agg.copy())
        # plot_combined_error_rate_per_layout(df_agg.copy())
        
        # --- STEP 1: NORMALITY ---
        print("=" * 80)
        print("STEP 1: CHECKING ASSUMPTIONS (NORMALITY)")
        print("=" * 80)
        is_error_normal = normality_of_error_rate(df_agg.copy(), dv="mean_error_rate")
        is_tokens_normal = normality_of_error_rate(df_agg.copy(), dv="mean_output_tokens")
        
        # --- STEP 2: PARAMETRIC PURCHASE REPLICATION (ANOVA + TUKEY) ---
        # Run main ANOVA (takes "long" data)
        error_p_param, tokens_p_param = purchase_parametric_analysis(df_pre.copy())

        # Run post-hoc Tukey (takes AGGREGATED data)
        print("\n" + "=" * 80)
        print("Purchase's Parametric Post-Hoc (Tukey HSD)")
        print("=" * 80)
        if error_p_param < 0.05:
            purchase_pairwise_comparison(df_agg.copy(), dv="mean_error_rate")
        else:
            print("No significant main effect for Error, skipping Tukey HSD.")
        if tokens_p_param < 0.05:
            purchase_pairwise_comparison(df_agg.copy(), dv="mean_output_tokens")
        else:
            print("\nNo significant main effect for Output_Tokens, skipping Tukey HSD.")

        # --- STEP 3: NON-PARAMETRIC ANALYSIS (FRIEDMAN + WILCOXON) ---
        # Run main Friedman (takes AGGREGATED data)
        error_p_nonparam, tokens_p_nonparam = our_main_effect_test(df_agg.copy())

        # Run post-hoc Wilcoxon (takes AGGREGATED data)
        print("\n" + "=" * 80)
        print("OUR ANALYSIS: Non-Parametric Post-Hoc (Wilcoxon + Bonferroni)")
        print("=" * 80)
        if error_p_nonparam < 0.05:
            our_pairwise_comparison(df_agg.copy(), dv="mean_error_rate")
        else:
            print("No significant non-parametric main effect for Error, skipping post-hoc.")
        if tokens_p_nonparam < 0.05:
            our_pairwise_comparison(df_agg.copy(), dv="mean_output_tokens")
        else:
            print("\nNo significant non-parametric main effect for Output_Tokens, skipping post-hoc.")

        # --- STEP 4: GEE VALIDATION ---
        our_gee_analysis(df_pre.copy())
        
        print("\n\n" + "=" * 80)
        print("Analysis complete.")
        print("=" * 80)
    else:
        print(f"Error: No data loaded. Check path: {RESULTS_DIR}")