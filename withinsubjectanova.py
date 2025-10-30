import os

import pandas as pd
from statsmodels.stats.anova import AnovaRM

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


def effect_plusminus(df: pd.DataFrame):
    # Ugly ahh hack to get + or -
    df["Layout"] = df["Layout"].astype(str).apply(lambda x: x[1])

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

    print("Effect of + / -:\n")
    print(df_agg)

    print("\nEffect of + / - on Error\n")
    print(
        AnovaRM(
            data=df_agg,
            depvar="Error",
            subject="Model",
            within=["Layout"],
        ).fit()
    )

    print("Effect of + / - on Output_Tokens\n")
    print(
        AnovaRM(
            data=df_agg,
            depvar="Output_Tokens",
            subject="Model",
            within=["Layout"],
        ).fit()
    )


if __name__ == "__main__":
    master_data_frame = load_and_aggregate_results()
    df_pre = pre_aggregate(master_data_frame)

    effect_plusminus(df_pre)
