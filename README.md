# Vaccination Coverage & Disease Incidence — Dashboard Portfolio

**Role:** Dashboard developer and data visualization contributor  
**Stack:** Python · Streamlit · pandas · Plotly · Git/GitHub  
**Team:** BIOT 670I Group 1 (2026)

## Project
An interactive public-health dashboard exploring vaccination coverage and reported measles, mumps, and pertussis incidence in California and Florida. Descriptive trends from the master dataset are deliberately separated from precomputed, measles-specific lag analyses.

## What I built
- Streamlit **MMP Master Explorer**: disease/state selectors, coverage and incidence trends, missing-data summaries.
- **California and Florida measles case-study interfaces**: interactive 0–5-year lag selection, Pearson *r*, p-values, observation counts, and clear uncertainty warnings.
- **Data-quality interface**: observed/missing-year metrics, calendar-year pair checks, and methodological explanations.
- UI improvements: readable yearly ticks, responsive charts, and removal of erroneous Plotly labels.

## Evidence
- [Live team application](https://biot670i-group1.streamlit.app/)
- [Original team repository](https://github.com/FusRaDa/biot670i_capstone_vaccination_project)
- See `Moira_Overly_Capstone_Contributions.ipynb` for a concise walkthrough and reproducibility notes.
- Add screenshots under `images/` after local review.

## Analytical boundaries
This work does not claim individual-level causation. The all-disease explorer is descriptive; the state-specific lag models shown here concern **measles** and were produced within the team's analysis workflow. The project depends on surveillance and NIS-Child-derived data with different populations and possible missingness/confounding.

## Attribution
This portfolio showcases my **dashboard code and implementation contributions** in a collaborative university capstone. Original datasets, statistical notebooks, and other pages may have been prepared by other team members. Refer to the original group repository for the full project and contributors.

## Running the original group app
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app/app.py
```
This command applies only if the full original project dependencies and data files are present. The standalone contribution notebook can be viewed on GitHub without running Streamlit.
