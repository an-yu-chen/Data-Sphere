"""Export coefficient estimates, confidence intervals and marginal effects."""
from pathlib import Path
import json
import pickle
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"


def model_payload(model):
    ci = model.conf_int()
    coef = []
    for name in model.params.index:
        if name == "const":
            continue
        coef.append({
            "name": name, "estimate": float(model.params[name]),
            "std_error": float(model.bse[name]), "z": float(model.tvalues[name]),
            "p_value": float(model.pvalues[name]),
            "ci_low": float(ci.loc[name, 0]), "ci_high": float(ci.loc[name, 1]),
        })
    me = model.get_margeff(at="overall").summary_frame()
    marginal = []
    for name, row in me.iterrows():
        marginal.append({
            "name": str(name), "estimate": float(row["dy/dx"]),
            "std_error": float(row["Std. Err."]), "z": float(row["z"]),
            "p_value": float(row["Pr(>|z|)"]),
            "ci_low": float(row["Conf. Int. Low"]),
            "ci_high": float(row["Cont. Int. Hi"]),
        })
    return {
        "n": int(model.nobs), "pseudo_r2": float(model.prsquared),
        "log_likelihood": float(model.llf), "coefficients": coef,
        "marginal_effects": marginal,
    }


def main():
    paths = [OUT / "first_stage_probit.pkl", OUT / "second_stage_probit.pkl"]
    if not all(p.exists() for p in paths):
        raise FileNotFoundError("Run scripts 05 and 06 before script 07.")
    models = []
    for path in paths:
        with open(path, "rb") as f:
            models.append(pickle.load(f))
    results = {"first": model_payload(models[0]), "second": model_payload(models[1])}
    (OUT / "regression_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    for i, model in enumerate(models, start=1):
        print(f"\nSTAGE {i}: N={int(model.nobs):,}; pseudo-R2={model.prsquared:.4f}")
        print(model.summary())
        print("\nAverage marginal effects:")
        print(model.get_margeff(at="overall").summary())
    print(f"Saved {OUT / 'regression_results.json'}")


if __name__ == "__main__":
    main()
