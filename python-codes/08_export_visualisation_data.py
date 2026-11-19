"""Export annual data and regression estimates; update the supplied HTML file."""
from pathlib import Path
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
TEMPLATE = ROOT / "green_innovation_interactive_data_visualisations.html"


def clean_records(df):
    return json.loads(df.to_json(orient="records"))


def main():
    pfile = OUT / "annual_patent_indicators.csv"
    sfile = OUT / "annual_science_indicators.csv"
    rfile = OUT / "regression_results.json"
    for p in [pfile, sfile, rfile]:
        if not p.exists():
            raise FileNotFoundError(f"Missing {p.name}. Run scripts 02, 04 and 07 first.")
    patents = clean_records(pd.read_csv(pfile))
    science = clean_records(pd.read_csv(sfile))
    regression = json.loads(rfile.read_text(encoding="utf-8"))
    data = {"patents": patents, "science": science}
    (OUT / "visualisation_data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    # Translate the statsmodels result structure into the schema consumed by
    # the existing interactive HTML's coefficient explorer.
    reg_for_html = {}
    for stage in ["first", "second"]:
        item = regression[stage]
        reg_for_html[stage] = {
            "n": item["n"], "r2": f"{item['pseudo_r2']:.4f}",
            "coef": [[x["name"], x["estimate"], x["std_error"], x["z"],
                      x["p_value"], x["ci_low"], x["ci_high"]] for x in item["coefficients"]],
            "me": [[x["name"], x["estimate"], x["std_error"], x["z"],
                    x["p_value"], x["ci_low"], x["ci_high"]] for x in item["marginal_effects"]],
        }
    (OUT / "visualisation_regression_data.json").write_text(json.dumps(reg_for_html, indent=2), encoding="utf-8")

    if not TEMPLATE.exists():
        print("Data exports created. To update the HTML, put the existing HTML file beside this script as:")
        print(TEMPLATE.name)
        return
    html = TEMPLATE.read_text(encoding="utf-8")
    html, n1 = re.subn(r"const D = \{.*?\};\s*const P = D\.patents, S = D\.science;",
                       "const D = " + json.dumps(data, separators=(",", ":")) + ";\nconst P = D.patents, S = D.science;",
                       html, count=1, flags=re.S)
    html, n2 = re.subn(r"const REG=\{.*?\};\s*function renderRegression\(\)",
                       "const REG=" + json.dumps(reg_for_html, separators=(",", ":")) + ";\nfunction renderRegression()",
                       html, count=1, flags=re.S)
    if n1 != 1 or n2 != 1:
        raise RuntimeError("Could not locate the expected data blocks in the HTML template. No HTML was written.")
    target = ROOT / "green_innovation_interactive_data_visualisations_updated.html"
    target.write_text(html, encoding="utf-8")
    print(f"Updated interactive visualisation saved to: {target}")
    print(f"Annual data: {len(patents)} years; regression stages: {len(reg_for_html)}")


if __name__ == "__main__":
    main()
