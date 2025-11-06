import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, probplot, shapiro
from statsmodels.stats.anova import AnovaResults, AnovaRM


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


def normality_of_error_rate(df: pd.DataFrame):
    df = error_rate_for_subjects(df)

    print("")
    stat, p = shapiro(df["mean_error_rate"])
    print(f"all: W={stat:.3f}, p={p:.3f}{'     <--- oarg' if p < 0.05 else ''}\n")
    probplot(df["mean_error_rate"], dist="norm", plot=plt)
    plt.title("Q-Q Plot for all")
    plt.show()


    data = df["mean_error_rate"].dropna()
    if data.empty:
        print("no data to plot")
    else:
        mu, sigma = data.mean(), data.std(ddof=0)
        padding = 0.1 * (data.max() - data.min() if data.max() != data.min() else 1.0)
        xs = np.linspace(data.min() - padding, data.max() + padding, 200)

        plt.figure()
        plt.hist(data, bins=20, density=True, alpha=0.6, color="C0", edgecolor="k")
        plt.plot(xs, norm.pdf(xs, loc=mu, scale=sigma), "r-", lw=2, label=f"Normal PDF (μ={mu:.3f}, σ={sigma:.3f})")
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

    # Here we combine the No CoT/CoT and Zero/Few-shot results for each model
    # This May Not Be Wanted!
    #
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
