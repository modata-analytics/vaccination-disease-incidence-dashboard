# Vaccination Coverage & Disease Incidence — Dashboard Portfolio

**Role:** Dashboard developer and data visualization contributor  
**Stack:** Python · Streamlit · pandas · Plotly · Git/GitHub  
**Team:** BIOT 670I Group 1 (2026) — Heba Bakry, Gloria Bukirwa, Moira Overly, Kalkidan Perin, and Matthew Rada

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

## Team acknowledgment and attribution

This dashboard was developed as part of **BIOT 670I Group 1**, a collaborative capstone project by:

- **Heba Bakry**
- **Gloria Bukirwa**
- **Moira Overly**
- **Kalkidan Perin**
- **Matthew Rada**

I am grateful for my teammates’ contributions to the project’s research, data preparation, analysis, and shared application. The work shown here builds on a team effort rather than an independently developed dataset or statistical pipeline.

In particular, the group’s work included harmonizing vaccination coverage, disease surveillance, and population data; developing a reusable master dataset; investigating time-lagged associations; and building and maintaining the shared Streamlit application. The original team repository documents the broader codebase and contributions. I do not attribute individual tasks beyond what is documented in that repository.

**My specific contributions** centered on the Streamlit dashboard: implementing the MMP Explorer, developing and extending the California and Florida measles case-study interfaces, adding data-completeness and lag-pair displays, and improving chart usability and methodological communication. The correlation estimates and source-data processing were produced within the broader team workflow; presenting them interactively does not imply that I independently generated all underlying analyses.

**Project credit:** BIOT 670I Group 1. This personal repository is a curated portfolio of my contributions, not a replacement for or claim of sole authorship of the group project. Please see the [original group repository](https://github.com/FusRaDa/biot670i_capstone_vaccination_project) for the complete collaborative work.

## Running the original group app
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app/app.py
```
This command applies only if the full original project dependencies and data files are present. The standalone contribution notebook can be viewed on GitHub without running Streamlit.
