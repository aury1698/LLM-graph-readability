import os
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import (  # noqa: F401
    friedmanchisquare,
    norm,
    probplot,
    shapiro,
    wilcoxon,
)
import scikit_posthocs as sp
from statsmodels.stats.anova import AnovaResults, AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests  # noqa: F401

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
    agg = df.groupby(["Model", "Layout"], as_index=False).agg(
        mean_error_rate=("Correct", "mean"),
        mean_output_tokens=("Output_Tokens", "mean"),
    )

    return pd.DataFrame(agg)


def save_wide_csv(df: pd.DataFrame) -> str:
    err_df = error_rate_for_subjects(df)

    df_wide_error = err_df.pivot(
        index="Model", columns="Layout", values="mean_error_rate"
    )
    filename = "error_rate_per_subject_all.csv"
    out_path = os.path.join("./", filename)
    df_wide_error.to_csv(out_path, index=False)

    df_wide_out = err_df.pivot(
        index="Model", columns="Layout", values="mean_output_tokens"
    )
    filename = "output_tokens_per_subject_all.csv"
    out_path = os.path.join("./", filename)
    df_wide_out.to_csv(out_path, index=False)

    for sign in ["-", "+"]:
        subset = err_df[err_df["Layout"].astype(str).str.endswith(sign, na=False)]

        subset_wide_error = subset.pivot(
            index="Model", columns="Layout", values="mean_error_rate"
        )
        filename = f"error_rate_per_subject_type_{sign}.csv"
        out_path = os.path.join("./", filename)
        subset_wide_error.to_csv(out_path, index=False)

        subset_wide_output_tokens = subset.pivot(
            index="Model", columns="Layout", values="mean_output_tokens"
        )
        filename = f"output_tokens_per_subject_type_{sign}.csv"
        out_path = os.path.join("./", filename)
        subset_wide_output_tokens.to_csv(out_path, index=False)


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


def purchase_effect_plusminus(df: pd.DataFrame):
    # Ugly ahh hack to get + or -
    df["Layout"] = df["Layout"].astype(str).apply(lambda x: x[1])

    r = calculate_anovaRM(df)
    print("\n\nEffect of + / - across all aesthetic for Error\n")
    print(r[0])

    print("Effect of + / - across all aesthetic for Output_Tokens\n")
    print(r[1])


def purchase_effect_hypotheses_certain_aesthetic(df: pd.DataFrame, aesthetic: str):
    # filter for certain aesthetic, e.g. 'b' filters for b+ and b-
    df = df[df["Layout"].astype(str).str.startswith(aesthetic, na=False)]

    r = calculate_anovaRM(df)
    print(f"\n\nEffect of {aesthetic} + / - for Error\n")
    print(r[0])

    print(f"Effect of {aesthetic} + / - for Output_Tokens\n")
    print(r[1])


def purchase_pairwise_comparison(df: pd.DataFrame, alpha: float = 0.05):
    df = error_rate_for_subjects(df)

    for sign in ["-", "+"]:
        subset = df[df["Layout"].astype(str).str.endswith(sign, na=False)]
        tuk = pairwise_tukeyhsd(
            endog=subset["mean_error_rate"], groups=subset["Layout"], alpha=alpha
        )
        print(f"\nTukey HSD for mean_error_rate across layouts ending with '{sign}'\n")
        print(tuk.summary())

    for sign in ["-", "+"]:
        subset = df[df["Layout"].astype(str).str.endswith(sign, na=False)]
        tuk = pairwise_tukeyhsd(
            endog=subset["mean_output_tokens"], groups=subset["Layout"], alpha=alpha
        )
        print(
            f"\nTukey HSD for mean_output_tokens across layouts ending with '{sign}'\n"
        )
        print(tuk.summary())


def purchase_effect_aesthetic(df: pd.DataFrame):
    # Ugly ahh hack to get only b c m o s
    df["Layout"] = df["Layout"].astype(str).apply(lambda x: x[0])

    r = calculate_anovaRM(df)
    print("\n\nEffect of the aesthetic b/c/m/o/s across + and - for Error\n")
    print(r[0])

    print("Effect of the aesthetic b/c/m/o/s across + and - for Output_Tokens\n")
    print(r[1])


def purchase_effect_aesthetic_for_plus_or_minus(df: pd.DataFrame, plus_or_minus: str):
    # filter for certain + or -, e.g. '+' filters for b+, c+, m+, ...
    df = df[df["Layout"].astype(str).str.endswith(plus_or_minus, na=False)]

    r = calculate_anovaRM(df)
    print(f"\n\nEffect of the {plus_or_minus} aesthetics for Error\n")
    print(r[0])

    print(f"Effect of the {plus_or_minus} aesthetics for Output_Tokens\n")
    print(r[1])


def our_hypotheses_test_wilcoxon(df: pd.DataFrame):
    df = error_rate_for_subjects(df)
    wide_err = df.pivot(index="Model", columns="Layout", values="mean_error_rate")

    plus_cols = [c for c in wide_err.columns if str(c).endswith("+")]
    minus_cols = [c for c in wide_err.columns if str(c).endswith("-")]

    plus_mean_err = wide_err[plus_cols].mean(axis=1)
    minus_mean_err = wide_err[minus_cols].mean(axis=1)
    paired_err = pd.concat([plus_mean_err, minus_mean_err], axis=1)
    paired_err.columns = ["plus_mean_err", "minus_mean_err"]

    print("\n")
    stat, p = wilcoxon(
        paired_err["plus_mean_err"], paired_err["minus_mean_err"], alternative="less"
    )
    print(
        f"Wilcoxon (error): '+' vs '-':         n={len(paired_err)} | W={stat:.4f}, p={p:.6f}"
    )

    for aest in ["b", "c", "m", "o", "s"]:
        plus_cols = [
            c
            for c in wide_err.columns
            if str(c).endswith("+") and str(c).startswith(aest)
        ]
        minus_cols = [
            c
            for c in wide_err.columns
            if str(c).endswith("-") and str(c).startswith(aest)
        ]

        plus_mean_err = wide_err[plus_cols].mean(axis=1)
        minus_mean_err = wide_err[minus_cols].mean(axis=1)
        paired_err = pd.concat([plus_mean_err, minus_mean_err], axis=1)
        paired_err.columns = ["plus_mean_err", "minus_mean_err"]

        stat, p = wilcoxon(
            paired_err["plus_mean_err"],
            paired_err["minus_mean_err"],
            alternative="less",
        )
        print(
            f"Wilcoxon (error): '{aest}+' vs '{aest}-':         n={len(paired_err)} | W={stat:.4f}, p={p:.6f}"
        )


def our_prioritizing_aesthetics_effect(df: pd.DataFrame):
    df = error_rate_for_subjects(df)
    wide_err = df.pivot(index="Model", columns="Layout", values="mean_error_rate")

    # Ugly ahh hack to get only b c m o s
    wide_err = wide_err.T.groupby(by=lambda col: str(col)[0]).mean()

    stat, p = friedmanchisquare(*[wide_err[col].values for col in wide_err.columns])
    print(
        f"\n\nFriedman Chi Square (error) for aesthetics b/c/m/o/s across + and -:\n\nQ={stat:.4f}, p={p:.6f}\n"
    )

    for sign in ["-", "+"]:
        # only compare for all + and all -
        subset = df[df["Layout"].astype(str).str.endswith(sign, na=False)]

        subset_wide_err = subset.pivot(
            index="Model", columns="Layout", values="mean_error_rate"
        )

        stat, p = friedmanchisquare(
            *[subset_wide_err[col].values for col in subset_wide_err.columns]
        )
        print(f"Friedman Chi Square Effect of the {sign} aesthetics for Error\n")
        print(f"Q={stat:.4f}, p={p:.6f}\n")

        print(f"Pairwise Conover Friedman for {sign}:")
        print(sp.posthoc_conover_friedman(subset_wide_err, p_adjust="bonferroni"))


def gee_pairwise_tests(res, method="bonferroni"):
    params = res.params
    cov = res.cov_params()

    levels = ["b"]
    for k in params.index:
        if k.startswith("C(Layout)[T."):
            levels.append(k.split("[T.")[1].split("]")[0])

    comparisons = []
    effects = []
    pvals = []

    for a, b in combinations(levels, 2):
        L = np.zeros(len(params))

        def idx(x):
            if x == "b":
                return None
            return params.index.get_loc(f"C(Layout)[T.{x}]")

        ia, ib = idx(a), idx(b)
        if ia is not None:
            L[ia] = 1
        if ib is not None:
            L[ib] = -1

        diff = float(L @ params)
        var = float(L @ cov @ L.T)
        se = np.sqrt(var)
        z = diff / se
        p = 2 * (1 - norm.cdf(abs(z)))

        comparisons.append((a, b))
        effects.append(diff)
        pvals.append(p)

    reject, pvals_corrected, _, _ = multipletests(pvals, method=method)

    print(
        "\nPairwise comparisons (GEE Wald tests) with multiple-comparison correction:"
    )
    print(f"Correction method: {method}")
    print("--------------------------------------------------------")

    for (a, b), d, p_raw, p_corr, sig in zip(
        comparisons, effects, pvals, pvals_corrected, reject
    ):
        star = "*" if sig else ""
        print(
            f"{a} vs {b}: diff={d:+.4f}, raw p={p_raw:.5f}, corrected p={p_corr:.5f} {star}"
        )


def our_gee_hypotheses(df: pd.DataFrame):
    df = df.copy()

    # combine Model, Shots and Prompt into a single Model identifier
    df["Model"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )

    def gee_logistic(subdf):
        model = sm.GEE.from_formula(
            "Correct ~ C(Layout)",
            groups="Model",
            data=subdf,
            family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable(),
        )
        res = model.fit()
        return res

    for aest in ["b", "c", "m", "o", "s"]:
        print(f"\nGEE logistic regression for Error '{aest}+' vs '{aest}-':")

        subset = df[df["Layout"].isin([f"{aest}-", f"{aest}+"])]

        res = gee_logistic(subset)
        print(res.summary())


def our_gee_prioritizing_aesthetics_analysis(df: pd.DataFrame):
    df = df.copy()

    # combine Model, Shots and Prompt into a single Model identifier
    df["Model"] = (
        df["Model"].astype(str)
        + "_"
        + df["Shots"].astype(str).apply(lambda x: x.split("-")[0])
        + "_"
        + df["Cot"].astype(str)
    )

    def gee_logistic(subdf):
        model = sm.GEE.from_formula(
            "Correct ~ C(Layout)",
            groups="Model",
            data=subdf,
            family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable(),
        )
        res = model.fit()
        return res

    print(
        "\n\nGEE logistic regression for Error of aesthetics b/c/m/o/s across + and -\n"
    )

    just_aesthetic = df.copy()
    just_aesthetic["Layout"] = (
        just_aesthetic["Layout"].astype(str).apply(lambda x: x[0])
    )

    res = gee_logistic(just_aesthetic)
    print(res.summary())

    for sign in ["-", "+"]:
        print(
            f"\n\nGEE Effect of '{sign}' aesthetics (only layouts ending with {sign})\n"
        )

        subset = df[df["Layout"].astype(str).str.endswith(sign, na=False)]

        res = gee_logistic(subset)
        print(res.summary())
        gee_pairwise_tests(res)


if __name__ == "__main__":
    master_data_frame = load_and_aggregate_results()
    df_pre = pre_transform(master_data_frame)

    # Filter results for one task only and run equivalent analysis
    # df_pre = df_pre[df_pre["Task"].astype(str).str.startswith("task3", na=False)]

    print("=" * 80)
    print("Testing normality of error rates")
    print("=" * 80)

    # normality_of_error_rate(df_pre)

    # Purchase's Hypotheses under section 3.1
    print("=" * 80)
    print(
        "Replicated results from section 3.1 - Testing the Five Individual Hypotheses"
    )
    print("=" * 80)

    purchase_effect_plusminus(df_pre.copy())

    for ae in ["b", "c", "m", "o", "s"]:
        purchase_effect_hypotheses_certain_aesthetic(df_pre.copy(), ae)

    # Purchase's Prioritising the Aesthetics under section 3.2
    print("=" * 80)
    print("Replicated results from section 3.2 - Prioritising the Aesthetics")
    print("=" * 80)

    purchase_effect_aesthetic(df_pre.copy())

    for pm in ["-", "+"]:
        purchase_effect_aesthetic_for_plus_or_minus(df_pre.copy(), pm)

    # plot_combined_error_rate_per_layout(df_pre)

    # save_wide_csv(df_pre)

    purchase_pairwise_comparison(df_pre)

    # auroras
    # run_parametric_post_hoc(df_pre)
    # run_non_parametric_post_hoc(df_pre)

    print("\n" + "=" * 80)
    print("Non-parametric Tests")
    print("=" * 80)

    our_hypotheses_test_wilcoxon(df_pre)

    print("\n" + "=" * 80)
    print("Non-parametric Pair-wise Comparision")
    print("=" * 80)

    our_prioritizing_aesthetics_effect(df_pre)

    print("=" * 80)
    print("Generalized Estimating Equations")
    print("=" * 80)

    our_gee_hypotheses(df_pre)

    our_gee_prioritizing_aesthetics_analysis(df_pre)
