"""Produce annual science-use and cited-science gender indicators."""
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

    # The science-gender averages are calculated only among observations
    # with Uses_Science == 1; missing values are not interpreted as zero.
    sci = df[df["Uses_Science"] == 1].copy()
    annual = sci.groupby("YearOfPatentGrant").agg(
        science_patent_count=("patent_id", "size"),
        mean_female_science_share=("avg_prop_F", "mean"),
        mean_male_science_share=("avg_prop_M", "mean"),
    ).reset_index().rename(columns={"YearOfPatentGrant": "year"})
    annual.to_csv(OUT / "annual_science_indicators.csv", index=False)

    all_annual = df.groupby("YearOfPatentGrant").agg(
        patent_count=("patent_id", "size"),
        science_using_patents=("Uses_Science", lambda s: int((s == 1).sum())),
    ).reset_index().rename(columns={"YearOfPatentGrant": "year"})
    all_annual["science_using_patent_share"] = all_annual.science_using_patents / all_annual.patent_count
    all_annual.to_csv(OUT / "science_use_by_year.csv", index=False)
    print("Saved annual_science_indicators.csv and science_use_by_year.csv")


if __name__ == "__main__":
    main()
