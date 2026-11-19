"""Estimate the first-stage Probit selection equation and save its sample."""
from pathlib import Path
import pickle
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent
INFILE = ROOT / "outputs" / "prepared_green_patents.csv"
OUT = ROOT / "outputs"
TECH = ["human_necessities", "Transporting", "Chemistry", "Textiles",
        "Constructions", "Mechanical_engineering", "Physics", "Electricity"]
PREDICTORS = ["male_ratio", "YearOfPatentGrant", "team_size", "Originality", "CPC_4digit"] + TECH
REQUIRED = ["use_knownscience", "unknown_gender_ratio"] + PREDICTORS


def main():
    if not INFILE.exists():
        raise FileNotFoundError("Run 01_data_preparation.py first.")
    df = pd.read_csv(INFILE, low_memory=False)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df = df.dropna(subset=REQUIRED).copy()
    # This reproduces the sample restriction in the research code supplied:
    # observations with any unknown-gender inventor are excluded.
    df = df[df["unknown_gender_ratio"] == 0].copy()
    X = sm.add_constant(df[PREDICTORS].astype(float), has_constant="add")
    y = df["use_knownscience"].astype(int)
    if y.nunique() != 2:
        raise ValueError("First-stage dependent variable must contain both 0 and 1.")
    print("Estimating first-stage Probit...")
    model = sm.Probit(y, X).fit(disp=True)
    with open(OUT / "first_stage_probit.pkl", "wb") as f:
        pickle.dump(model, f)
    df.to_csv(OUT / "first_stage_sample.csv", index=False)
    (OUT / "first_stage_summary.txt").write_text(model.summary().as_text(), encoding="utf-8")
    print(model.summary())
    print(f"Saved model and {len(df):,} first-stage observations.")


if __name__ == "__main__":
    main()
