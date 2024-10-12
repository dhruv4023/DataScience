import pandas as pd


def cleandata(df: pd.DataFrame):
    if "Time" not in df:
        df["Time"] = "-"

    df["Time"] = df["Time"].replace("-", "12:00:00 AM")
    df["Time"] = df["Time"].fillna("12:00:00 AM")

    return df
