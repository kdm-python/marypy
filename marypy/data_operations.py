from typing import Any
import pandas as pd
from icecream import ic

STRAINS_PATH = "./data/strains_cleaned.csv"


def get_strain_data(file_path: str = STRAINS_PATH) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def get_table_data(df: pd.DataFrame) -> list[dict]:
    """Read CSV file, extract name, type, rating and THC fields and return as a list of dicts."""
    df.drop(
        columns=[
            x for x in list(df.columns) if x not in ["Name", "Type", "Rating", "THC%"]
        ],
        inplace=True,
    )
    # This seems to be causing a JSON float error
    df["THC%"] = pd.to_numeric(
        df["THC%"].str.replace(r"\D", "", regex=True), downcast="integer"
    )

    dicts = df.to_dict(orient="records")

    return dicts


def search_strains(
    df: pd.DataFrame,
    target: Any,
    search_by: str = "Name",
) -> list[dict] | dict | None:
    """Search data by specified column looking for those that contain the target value."""
    if search_by not in df.columns:
        return {"error": f"Invalid column name '{search_by}'"}
    df.drop(
        columns=[
            x for x in list(df.columns) if x not in ["Name", "Type", "Rating", "THC%"]
        ],
        inplace=True,
    )
    results = df[df[search_by].str.contains(target, case=False, na=False, regex=False)]

    return results.to_dict(orient="records")


if __name__ == "__main__":
    df = get_strain_data()
    ic(df[:5])
    stripped_data = get_table_data(df)
    ic(stripped_data[:5])
    search_term = "Widow"
    ic(search_term)
    search_results = search_strains(df, search_term)
    ic(search_results)
