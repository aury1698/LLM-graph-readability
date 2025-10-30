import os

import pandas as pd
from statsmodels.stats.anova import AnovaRM, AnovaResults

CURRENT_MODE = "bastian"  # aurora or bastian

if CURRENT_MODE == "aurora":
    BASE_PATH = "layout_algorithms_performance"
else:
    BASE_PATH = "aesthetic_effect_human_performance"

RESULTS_DIR = os.path.join(BASE_PATH, "results")
OUTPUT_CSV_FILE = f"average_accuracies_{CURRENT_MODE}_by_difficulty.csv"

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


def pre_aggregate(df: pd.DataFrame):
    df.rename(columns={"Model Name": "Model"}, inplace=True)
    df.rename(columns={"LLM Mode": "Shots"}, inplace=True)
    df.rename(columns={"COT Mode": "Prompt"}, inplace=True)

    df["Layout"] = df["Layout"].str.split("_").str[0]
    df["Correct"] = (
        df["Correct Prediction (True/False)"]
        .astype(str)
        .apply(lambda x: 1 if x.strip() == "True" else 0)
    )

    grouping_columns = [
        "Model",
        "Shots",
        "Prompt",
        "Layout",
    ]

    df_agg = (
        df.groupby(grouping_columns)
        .agg(
            Accuracy=("Correct", "mean"),
            Samples=("Correct", "count"),
            Correct=("Correct", "sum"),
            Output_Tokens=("Output Tokens", "mean"),
        )
        .reset_index()
    )

    # Purchase uses error rate instead of accuracy
    df_agg["Error"] = df_agg["Accuracy"].apply(lambda a: 1 - a)
    df_agg.drop("Accuracy", axis=1, inplace=True)

    return df_agg.sort_values(by=grouping_columns).reset_index(drop=True)


def calculate_anovaRM(df: pd.DataFrame) -> tuple[AnovaResults, AnovaResults]:
    grouping_columns = [
        "Model",
        "Layout",
    ]

    df_agg = (
        df.groupby(grouping_columns)
        .agg(
            Samples=("Samples", "sum"),
            Correct=("Correct", "sum"),
            Error=("Error", "mean"),
            Output_Tokens=("Output_Tokens", "mean"),
        )
        .reset_index()
    )

    # Uncomment this if you want to see the dataframe that goes into
    # the Anova
    # print(df_agg)

    return (
        AnovaRM(
            data=df_agg,
            depvar="Error",
            subject="Model",
            within=["Layout"],
        ).fit(),
        AnovaRM(
            data=df_agg,
            depvar="Output_Tokens",
            subject="Model",
            within=["Layout"],
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
    df_pre = pre_aggregate(master_data_frame)

    # Purchase's Hypotheses under section 3.1
    print("="*80)
    print("Replicated results from section 3.1 - Testing the Five Individual Hypotheses")
    print("="*80)

    effect_plusminus(df_pre.copy())

    for ae in ["b", "c", "m", "o", "s"]:
        effect_hypotheses_certain_aesthetic(df_pre.copy(), ae)

    # Purchase's Prioritising the Aesthetics under section 3.2
    print("="*80)
    print("Replicated results from section 3.2 - Prioritising the Aesthetics")
    print("="*80)

    effect_aesthetic(df_pre.copy())

    for pm in ["-", "+"]:
        effect_aesthetic_for_plus_or_minus(df_pre.copy(), pm)
