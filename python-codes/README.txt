 PROJECT FOLDER LAYOUT
---------------------
python_scripts/
  01_data_preparation.py
  02_descriptive_analysis.py
  03_gender_representation.py
  04_scientific_knowledge.py
  05_first_stage_probit.py
  06_second_stage_probit.py
  07_econometric_results.py
  08_export_visualisation_data.py
  requirements.txt
  data/
    genderpatent_with_gender_ratios.csv
  outputs/                       (created automatically)
  green_innovation_interactive_data_visualisations.html  (HTML template)

HOW TO RUN
----------
1. Put the original genderpatent_with_gender_ratios.csv in the data folder.
2. Put the current HTML visualisation file beside the Python scripts.
3. In PyCharm, open this folder as the project.
4. Install packages in the PyCharm terminal:
       python -m pip install -r requirements.txt
5. Run the scripts in this order:
       01_data_preparation.py
       02_descriptive_analysis.py
       03_gender_representation.py
       04_scientific_knowledge.py
       05_first_stage_probit.py
       06_second_stage_probit.py
       07_econometric_results.py
       08_export_visualisation_data.py
6. Open green_innovation_interactive_data_visualisations_updated.html in a browser.

IMPORTANT NOTES
---------------
- The scripts preserve the full patent sample for descriptive work.
- The regression scripts reproduce the stated sample restriction:
  unknown_gender_ratio == 0; Stage 2 additionally requires Uses_Science == 1
  and use_knownscience == 1.
- The scripts do NOT clip, cap, rescale or silently delete male_ratio values.
  If male_ratio is not a proportion in the underlying file, its substantive
  interpretation must be checked against the variable construction in the paper.
- Stage 2 includes an inverse Mills ratio estimated in Stage 1. Conventional
  Probit standard errors in Stage 2 do not account for generated-regressor
  uncertainty. Treat inference as provisional until the full selection model
  is estimated with an appropriate joint estimator or a bootstrap repeating
  both stages. The exclusion restriction also needs a substantive justification.
- The data file and resulting outputs may be confidential. Do not publish the
  raw data, model sample files or derived outputs unless the relevant data and
  co-author permissions allow it.
