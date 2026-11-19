"""Produce annual inventor-gender representation tables."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
INFILE = ROOT / "outputs" / "prepared_green_patents.csv"
OUT = ROOT / "outputs"


def main():
    if not INFILE.exists():
        raise FileNotFoundError("Run 01_data_preparation.py first.")
    df = pd.read_csv(INFILE, low_memory=False)
    df = df.dropna(subset=["YearOfPatentGrant"]).copy()
    df["YearOfPatentGrant"] = df["YearOfPatentGrant"].astype(int)
    result = df.groupby("YearOfPatentGrant").agg(
        patent_count=("patent_id", "size"),
        mean_female_ratio=("female_ratio", "mean"),
        mean_male_ratio=("male_ratio", "mean"),
        mean_unknown_gender_ratio=("unknown_gender_ratio", "mean"),
        patents_with_female_inventors=("female_ratio", lambda s: int((s > 0).sum())),
        patents_with_male_inventors=("male_ratio", lambda s: int((s > 0).sum())),
    ).reset_index().rename(columns={"YearOfPatentGrant": "year"})
    result["female_inventor_patent_share"] = result.patents_with_female_inventors / result.patent_count
    result["male_inventor_patent_share"] = result.patents_with_male_inventors / result.patent_count
    result.to_csv(OUT / "gender_representation_by_year.csv", index=False)
    print(f"Saved {OUT / 'gender_representation_by_year.csv'}")


if __name__ == "__main__":
    main()
