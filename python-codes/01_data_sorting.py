from pathlib import Path
import pandas as pd
 

REQUIRED = [
    "patent_id", "YearOfPatentGrant", "female_ratio", "male_ratio",
    "unknown_gender_ratio", "team_size", "Uses_Science", "use_knownscience",
    "avg_prop_F", "avg_prop_M", "Originality", "Generality",
    "ForwardCitations5Years", "ForwardCitations7Years", "CPC_4digit",
    "human_necessities", "Transporting", "Chemistry", "Textiles",
    "Constructions", "Mechanical_engineering", "Physics", "Electricity",
]


def main():
    if not DATA.exists():
        raise FileNotFoundError(
            f"Cannot find {DATA}. Put genderpatent_with_gender_ratios.csv "
            "inside a folder named 'data' beside this script."
        )
    print("Reading source data...")
    df = pd.read_csv(DATA, low_memory=False)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Required columns missing from source file: {missing}")

    # Convert model/descriptive variables to numeric, but do not clip, cap,
    # rescale, or delete out-of-range gender-ratio values automatically.
    numeric = [c for c in REQUIRED if c != "patent_id"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Preserve the full sample. Each later analysis applies its own explicit
    # complete-case/sample-selection rule.
    out_file = OUT / "prepared_green_patents.csv"
    df.to_csv(out_file, index=False)
    print(f"Saved: {out_file}")
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Year range: {df['YearOfPatentGrant'].min():.0f}–{df['YearOfPatentGrant'].max():.0f}")
    print("Note: gender-ratio values were not clipped or silently modified.")


if __name__ == "__main__":
    main()
