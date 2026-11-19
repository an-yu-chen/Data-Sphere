"""Estimate the second-stage Probit with a generated inverse Mills ratio."""
from pathlib import Path
import pickle
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
TECH = ["human_necessities", "Transporting", "Chemistry", "Textiles",
        "Constructions", "Mechanical_engineering", "Physics", "Electricity"]
PREDICTORS = ["male_ratio", "YearOfPatentGrant", "team_size", "Originality", "CPC_4digit"] + TECH + ["IMR"]


def main():
    sample_file = OUT / "first_stage_sample.csv"
    model_file = OUT / "first_stage_probit.pkl"
    if not sample_file.exists() or not model_file.exists():
        raise FileNotFoundError("Run 05_first_stage_probit.py first.")
    df = pd.read_csv(sample_file, low_memory=False)
    with open(model_file, "rb") as f:
        first_model = pickle.load(f)

    # IMPORTANT: statsmodels predict() returns probabilities by default.
    # linear=True is required to obtain the latent index for the IMR.
    X1 = sm.add_constant(df[[c for c in PREDICTORS if c != "IMR"]].astype(float), has_constant="add")
    xb = first_model.predict(X1, linear=True)
    log_imr = norm.logpdf(xb) - norm.logcdf(xb)
    df["IMR"] = np.exp(np.clip(log_imr, -700, 700))
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["IMR"])

    # Keep the outcome sample definition used in the submitted code.
    selected = df[(df["Uses_Science"] == 1) & (df["use_knownscience"] == 1)].copy()
    selected["female_science_binary"] = (selected["avg_prop_F"] > 0).astype(int)
    selected = selected.dropna(subset=PREDICTORS + ["female_science_binary"])
    X2 = sm.add_constant(selected[PREDICTORS].astype(float), has_constant="add")
    y2 = selected["female_science_binary"].astype(int)
    if y2.nunique() != 2:
        raise ValueError("Second-stage outcome must contain both 0 and 1.")

    print("Estimating second-stage Probit...")
    model = sm.Probit(y2, X2).fit(disp=True)
    with open(OUT / "second_stage_probit.pkl", "wb") as f:
        pickle.dump(model, f)
    selected.to_csv(OUT / "second_stage_sample.csv", index=False)
    (OUT / "second_stage_summary.txt").write_text(model.summary().as_text(), encoding="utf-8")
    print(model.summary())
    print(f"Saved model and {len(selected):,} second-stage observations.")
    print("Caution: conventional second-stage standard errors do not account for generated-IMR uncertainty.")


if __name__ == "__main__":
    main()
