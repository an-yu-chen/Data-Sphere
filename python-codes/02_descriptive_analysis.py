"""Create annual descriptive indicators used by the interactive visualisation."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
INFILE = ROOT / "outputs" / "prepared_green_patents.csv"
OUT = ROOT / "outputs"


def main():
    if not INFILE.exists():
        raise FileNotFoundError("Run 01_data_preparation.py first.")
    df = pd.read_csv(INFILE, low_memory=False)
    year = "YearOfPatentGrant"
    df = df.dropna(subset=[year]).copy()
    df[year] = df[year].astype(int)

    # A patent is counted as having female/male inventors when the relevant
    # recorded inventor share is greater than zero.
    grouped = df.groupby(year, dropna=True)
    annual = grouped.agg(
        patent_count=("patent_id", "size"),
        mean_female_ratio=("female_ratio", "mean"),
        mean_male_ratio=("male_ratio", "mean"),
        mean_unknown_gender_ratio=("unknown_gender_ratio", "mean"),
        patents_with_female_inventors=("female_ratio", lambda s: int((s > 0).sum())),
        patents_with_male_inventors=("male_ratio", lambda s: int((s > 0).sum())),
        average_team_size=("team_size", "mean"),
        average_originality=("Originality", "mean"),
        average_generality=("Generality", "mean"),
        average_forward_citations_5yr=("ForwardCitations5Years", "mean"),
        average_forward_citations_7yr=("ForwardCitations7Years", "mean"),
        science_using_patents=("Uses_Science", lambda s: int((s == 1).sum())),
    ).reset_index().rename(columns={year: "year"})
    annual["female_inventor_patent_share"] = annual["patents_with_female_inventors"] / annual["patent_count"]
    annual["science_using_patent_share"] = annual["science_using_patents"] / annual["patent_count"]
    annual.to_csv(OUT / "annual_patent_indicators.csv", index=False)

    # Save a concise text summary as a quick reproducibility check.
    lines = [
        f"Total patent observations: {len(df):,}",
        f"Year range: {annual.year.min()}–{annual.year.max()}",
        f"Overall female-inventor patent share: {(df.female_ratio > 0).mean():.4f}",
        f"Overall science-use share: {(df.Uses_Science == 1).mean():.4f}",
    ]
    (OUT / "descriptive_summary.txt").write_text("\n".join(lines), encoding="utf-8")
    print("Saved annual_patent_indicators.csv and descriptive_summary.txt")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
