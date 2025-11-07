import os
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, probplot, shapiro, ttest_rel, wilcoxon  # noqa: F401
from statsmodels.stats.anova import AnovaResults, AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests

BASE_PATH = "aesthetic_effect_human_performance"

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
        return ValueError("no csv files found")

    return pd.concat(all_data_frames, ignore_index=True)


def pre_transform(df: pd.DataFrame):
    """
    Required as the Anova library does not/cannot handle column names with spaces.
    """
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

    return df


def error_rate_for_subjects(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # combine Model, Shots and Prompt into a single Model identifier
    df["Model"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )

    # per task normal distribution
    # df = df[df["Task"].astype(str).str.startswith("task1", na=False)]

    # as we want error rate and not accuracy, flip the bool and convert to int
    df["Correct"] = df["Correct"].apply(lambda x: not x).astype(int)
    agg = df.groupby(["Model", "Layout"], as_index=False)["Correct"].mean()
    agg.rename(columns={"Correct": "mean_error_rate"}, inplace=True)

    return pd.DataFrame(agg)

def save_error_rate_wide_csv(df: pd.DataFrame) -> str:
    err_df = error_rate_for_subjects(df)
    df_wide = err_df.pivot(index="Model", columns="Layout", values="mean_error_rate")

    filename = "error_rate_per_subject_all.csv"
    out_path = os.path.join("./", filename)
    df_wide.to_csv(out_path, index=False)

    for sign in ["-", "+"]:
        subset = err_df[err_df["Layout"].astype(str).str.endswith(sign, na=False)]
        subset_wide = subset.pivot(index="Model", columns="Layout", values="mean_error_rate")

        filename = f"error_rate_per_subject_type_{sign}.csv"
        out_path = os.path.join("./", filename)
        subset_wide.to_csv(out_path, index=False)

def plot_combined_error_rate_per_layout(df: pd.DataFrame):
    df = error_rate_for_subjects(df)
    agg = df.groupby(["Layout"], as_index=False)["mean_error_rate"].mean()
    print(agg)
    plt.figure()
    plt.title("error per layout")
    plt.bar(agg["Layout"], agg["mean_error_rate"])
    plt.show()


def normality_of_error_rate(df: pd.DataFrame):
    df = error_rate_for_subjects(df)

    print("")
    stat, p = shapiro(df["mean_error_rate"])
    print(f"all: W={stat:.3f}, p={p:.3f}{'     <--- oarg' if p < 0.05 else ''}\n")
    # probplot(df["mean_error_rate"], dist="norm", plot=plt)
    # plt.title("Q-Q Plot for all")
    # plt.show()

    data = df["mean_error_rate"].dropna()
    if data.empty:
        print("no data to plot")
    else:
        mu, sigma = data.mean(), data.std(ddof=0)
        padding = 0.1 * (data.max() - data.min() if data.max() != data.min() else 1.0)
        xs = np.linspace(data.min() - padding, data.max() + padding, 200)

        plt.figure()
        plt.hist(data, bins=20, density=True, alpha=0.6, color="C0", edgecolor="k")
        plt.plot(
            xs,
            norm.pdf(xs, loc=mu, scale=sigma),
            "r-",
            lw=2,
            label=f"Normal PDF (μ={mu:.3f}, σ={sigma:.3f})",
        )
        plt.title("Histogram of mean_error_rate with fitted normal (bell curve)")
        plt.xlabel("mean_error_rate")
        plt.ylabel("Density")
        plt.legend()
        plt.show()

    for cond, subset in df.groupby("Layout"):
        stat, p = shapiro(subset["mean_error_rate"])
        print(
            f"{cond}: W={stat:.3f}, p={p:.3f}{'     <--- oarg' if p < 0.05 else ''}\n"
        )
    print("")

    # for cond, subset in df.groupby("Layout"):
    #    probplot(subset["mean_error_rate"], dist="norm", plot=plt)
    #    plt.title(f"Q-Q Plot for {cond}")
    #    plt.show()


def calculate_anovaRM(df: pd.DataFrame) -> tuple[AnovaResults, AnovaResults]:
    df = df.copy()

    # combine Model, Shots and Prompt into a single Model identifier
    df["Model"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )

    # Uncomment this if you want to see the dataframe that goes into the Anova
    # print(df)

    # Aggregation is required!
    #
    # If the data set contains more than a single observation per subject and cell of the specified model,
    # this function will be used to aggregate the data before running the Anova.
    # An exception will be raised if aggregation is required, but no aggregation function was specified.
    return (
        AnovaRM(
            data=df,
            depvar="Correct",
            subject="Model",
            within=["Layout"],
            aggregate_func="mean",
        ).fit(),
        AnovaRM(
            data=df,
            depvar="Output_Tokens",
            subject="Model",
            within=["Layout"],
            aggregate_func="mean",
        ).fit(),
    )


def effect_plusminus(df: pd.DataFrame):
    # Ugly ahh hack to get + or -
    df["Layout"] = df["Layout"].astype(str).apply(lambda x: x[1])

    r = calculate_anovaRM(df)
    print("\n\nEffect of + / - across all aesthetic for Error\n")
    print(r[0])

    print("Effect of + / - across all aesthetic for Output_Tokens\n")
    print(r[1])


def effect_hypotheses_certain_aesthetic(df: pd.DataFrame, aesthetic: str):
    # filter for certain aesthetic, e.g. 'b' filters for b+ and b-
    df = df[df["Layout"].astype(str).str.startswith(aesthetic, na=False)]

    r = calculate_anovaRM(df)
    print(f"\n\nEffect of {aesthetic} + / - for Error\n")
    print(r[0])

    print(f"Effect of {aesthetic} + / - for Output_Tokens\n")
    print(r[1])


def pairwise_comparison(df: pd.DataFrame, alpha: float = 0.05):
    df = df.copy()

    df["Model"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )

    err_df = error_rate_for_subjects(df)
    for sign in ["-", "+"]:
        subset = err_df[err_df["Layout"].astype(str).str.endswith(sign, na=False)]
        tuk = pairwise_tukeyhsd(
            endog=subset["mean_error_rate"], groups=subset["Layout"], alpha=alpha
        )
        print(f"\nTukey HSD for mean_error_rate across layouts ending with '{sign}'\n")
        print(tuk.summary())

    # aggregate output tokens per Model/Layout (mean)
    out_df = (
        df.groupby(["Model", "Layout"], as_index=False)["Output_Tokens"]
        .mean()
        .rename(columns={"Output_Tokens": "mean_output_tokens"})
    )
    for sign in ["-", "+"]:
        subset = out_df[out_df["Layout"].astype(str).str.endswith(sign, na=False)]
        tuk = pairwise_tukeyhsd(
            endog=subset["mean_output_tokens"], groups=subset["Layout"], alpha=alpha
        )
        print(
            f"\nTukey HSD for mean_output_tokens across layouts ending with '{sign}'\n"
        )
        print(tuk.summary())


# copied from aurora
def run_parametric_post_hoc(df: pd.DataFrame, dv="mean_error_rate", alpha=0.05):
    """
    Performs PARAMETRIC post-hoc tests (paired t-tests + Holm correction).
    This replicates the "Tukey's WSD" logic from the paper.
    """

    for sign in ["-", "+"]:
        err_df = error_rate_for_subjects(df)
        subset = err_df[err_df["Layout"].astype(str).str.endswith(sign, na=False)]

        print(
            f"\n--- Parametric Post-Hoc for {dv} (Paired T-tests + Holm Correction) ---"
        )

        df_agg = subset.groupby(["Model", "Layout"], as_index=False)[dv].mean()
        df_wide = df_agg.pivot(index="Model", columns="Layout", values=dv)

        layouts = df_wide.columns
        comparisons = list(combinations(layouts, 2))
        p_values = []
        results = []

        for layout_a, layout_b in comparisons:
            data_a = df_wide[layout_a]
            data_b = df_wide[layout_b]

            common_data = pd.concat([data_a, data_b], axis=1, keys=["a", "b"]).dropna()

            if len(common_data) < 2:
                print(f"Skipping {layout_a} vs {layout_b}: insufficient paired data")
                continue

            stat, p = ttest_rel(common_data["a"], common_data["b"])  # Paired T-test
            p_values.append(p)
            results.append((layout_a, layout_b, stat, p))

        if not p_values:
            print("No post-hoc comparisons were performed.")
            return

        reject, p_values_corrected, _, _ = multipletests(
            p_values, alpha=alpha, method="holm"
        )

        print(
            "Layout A       | Layout B       |   T-Stat |  p-unc | p-adj (Holm) | Significant"
        )
        print("-" * 75)
        for i, (layout_a, layout_b, stat, p) in enumerate(results):
            sig_str = "YES" if reject[i] else "no"
            print(
                f"{layout_a:<14} | {layout_b:<14} | {stat:>8.3f} | {p:>6.3f} | {p_values_corrected[i]:>12.3f} | {sig_str}"
            )


# copied from aurora
def run_non_parametric_post_hoc(df: pd.DataFrame, dv="mean_error_rate", alpha=0.05):
    """
    Performs NON-PARAMETRIC post-hoc tests (Wilcoxon + Bonferroni correction).
    """

    for sign in ["-", "+"]:
        err_df = error_rate_for_subjects(df)
        subset = err_df[err_df["Layout"].astype(str).str.endswith(sign, na=False)]

        print(
            f"\n--- Non-Parametric Post-Hoc for {dv} (Wilcoxon + Bonferroni Correction) ---"
        )

        df_agg = subset.groupby(["Model", "Layout"], as_index=False)[dv].mean()
        df_wide = df_agg.pivot(index="Model", columns="Layout", values=dv)

        layouts = df_wide.columns
        comparisons = list(combinations(layouts, 2))
        p_values = []
        results = []

        for layout_a, layout_b in comparisons:
            data_a = df_wide[layout_a]
            data_b = df_wide[layout_b]

            common_data = pd.concat([data_a, data_b], axis=1, keys=["a", "b"]).dropna()

            if len(common_data) < 2:
                print(f"Skipping {layout_a} vs {layout_b}: insufficient paired data")
                continue

            # Wilcoxon signed-rank test for paired samples --> should it be Nemenyi instead?
            try:
                stat, p = wilcoxon(
                    common_data["a"], common_data["b"], zero_method="wilcox"
                )
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
        reject, p_values_corrected, _, _ = multipletests(
            p_values, alpha=alpha, method="bonferroni"
        )

        print(
            "Layout A       | Layout B       |   W-Stat |  p-unc | p-adj (Bonf) | Significant"
        )
        print("-" * 75)
        for i, (layout_a, layout_b, stat, p) in enumerate(results):
            sig_str = "YES" if reject[i] else "no"
            print(
                f"{layout_a:<14} | {layout_b:<14} | {stat:>8.3f} | {p:>6.3f} | {p_values_corrected[i]:>12.3f} | {sig_str}"
            )


def effect_aesthetic(df: pd.DataFrame):
    # Ugly ahh hack to get only b c m o s
    df["Layout"] = df["Layout"].astype(str).apply(lambda x: x[0])

    r = calculate_anovaRM(df)
    print("\n\nEffect of the aesthetic b/c/m/o/s across + and - for Error\n")
    print(r[0])

    print("Effect of the aesthetic b/c/m/o/s across + and - for Output_Tokens\n")
    print(r[1])


def effect_aesthetic_for_plus_or_minus(df: pd.DataFrame, plus_or_minus: str):
    # filter for certain + or -, e.g. '+' filters for b+, c+, m+, ...
    df = df[df["Layout"].astype(str).str.endswith(plus_or_minus, na=False)]

    r = calculate_anovaRM(df)
    print(f"\n\nEffect of the {plus_or_minus} aesthetics for Error\n")
    print(r[0])

    print(f"Effect of the {plus_or_minus} aesthetics for Output_Tokens\n")
    print(r[1])


if __name__ == "__main__":
    master_data_frame = load_and_aggregate_results()
    df_pre = pre_transform(master_data_frame)

    print("=" * 80)
    print("Testing normality of error rates")
    print("=" * 80)

    normality_of_error_rate(df_pre)

    # Purchase's Hypotheses under section 3.1
    print("=" * 80)
    print(
        "Replicated results from section 3.1 - Testing the Five Individual Hypotheses"
    )
    print("=" * 80)

    effect_plusminus(df_pre.copy())

    for ae in ["b", "c", "m", "o", "s"]:
        effect_hypotheses_certain_aesthetic(df_pre.copy(), ae)

    # Purchase's Prioritising the Aesthetics under section 3.2
    print("=" * 80)
    print("Replicated results from section 3.2 - Prioritising the Aesthetics")
    print("=" * 80)

    effect_aesthetic(df_pre.copy())

    for pm in ["-", "+"]:
        effect_aesthetic_for_plus_or_minus(df_pre.copy(), pm)

    # plot_combined_error_rate_per_layout(df_pre)

    # save_error_rate_wide_csv(df_pre)

    pairwise_comparison(df_pre)

    # auroras
    run_parametric_post_hoc(df_pre)
    run_non_parametric_post_hoc(df_pre)
