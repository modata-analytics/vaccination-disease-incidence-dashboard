
<div align="center">

# Vaccination Coverage & Disease Incidence Dashboard

### Interactive Public Health Data Analytics

**BIOT 670I Capstone Project | University of Maryland Global Campus | 2026**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)

<p>
  <a href="https://biot670i-group1.streamlit.app/">
    <strong>Live Group Dashboard</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="https://github.com/FusRaDa/biot670i_capstone_vaccination_project">
    <strong>Original Team Repository</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="Moira_Overly_Capstone_Contributions.ipynb">
    <strong>My Contribution Notebook</strong>
  </a>
</p>

<p><em>Independent Streamlit deployment: Coming soon</em></p>

</div>

---

## Project Overview

This project investigates population-level associations between vaccination coverage and the incidence of three vaccine-preventable diseases:

- **Measles**
- **Mumps**
- **Pertussis**

Developed collaboratively for the BIOT 670I Capstone Project at the University of Maryland Global Campus, the application brings together vaccination coverage, infectious disease surveillance, and population data in an interactive analytical environment.

The dashboard enables users to explore historical trends, compare geographic patterns, investigate time-lagged associations, and assess data completeness.

### Research Question

> How are changes in vaccination coverage associated with the incidence of vaccine-preventable diseases across geographic regions and time?

The project uses an ecological observational approach. Findings are exploratory and should not be interpreted as evidence of causation.

---

## Project Information

<table>
  <tr>
    <th align="left">Category</th>
    <th align="left">Details</th>
  </tr>
  <tr>
    <td>Institution</td>
    <td>University of Maryland Global Campus</td>
  </tr>
  <tr>
    <td>Course</td>
    <td>BIOT 670I — Capstone Project</td>
  </tr>
  <tr>
    <td>Year</td>
    <td>2026</td>
  </tr>
  <tr>
    <td>Team</td>
    <td>Group 1</td>
  </tr>
  <tr>
    <td>My Role</td>
    <td>Dashboard Development, Data Visualization, and Data Quality Integration</td>
  </tr>
  <tr>
    <td>Technologies</td>
    <td>Python, Streamlit, pandas, Plotly, Git, GitHub</td>
  </tr>
  <tr>
    <td>Featured Case Studies</td>
    <td>California and Florida</td>
  </tr>
  <tr>
    <td>Historical Period</td>
    <td>1995–2017</td>
  </tr>
</table>

---

## My Technical Contributions

My primary responsibility was developing and refining the interactive Streamlit dashboard, integrating team-produced data and statistical results, and improving data-quality reporting and scientific communication.

### 1. MMP Master Dataset Explorer

Developed an interactive interface allowing users to explore vaccination coverage and disease incidence across California and Florida.

**Features implemented:**

- Interactive selection of measles, mumps, and pertussis.
- California and Florida comparisons.
- Historical vaccination coverage trends.
- Disease incidence visualizations normalized per 100,000 residents.
- Disease-specific data-completeness summaries.
- Identification of incomplete state-year observations.
- Dynamic chart scaling and improved visualization formatting.
- Preservation of missing observations without interpolation.

### 2. California and Florida Measles Case Studies

Developed and expanded state-specific analytical interfaces to present historical measles trends and the team's time-lagged analyses.

**Features implemented:**

- Historical vaccination coverage and measles incidence charts.
- Interactive selection of 0–5-year lag periods.
- Display of Pearson correlation coefficients.
- Statistical p-values and observation counts.
- Integration of updated California and Florida analytical results.
- Dynamic interpretation of positive and negative correlations.
- Sample-size warnings and statistical uncertainty explanations.
- Historical context and methodological limitations.

The underlying correlation analyses were developed through the team's statistical workflow, including updated California and Florida results prepared by Kalkidan Perin.

### 3. Data Quality and Analytical Transparency

Implemented features to help users evaluate the completeness and reliability of the observations supporting the statistical findings.

These features include:

- Identification of missing annual observations.
- Calculation of data completeness percentages.
- Calendar-year lag-pair validation.
- Comparison of available and reported statistical sample sizes.
- Expandable tables displaying underlying observations.
- Explanations of confounding, ecological fallacy, and statistical uncertainty.

A primary objective was ensuring that missing observations were not interpreted as zero reported cases and that calendar-year gaps were handled appropriately.

### 4. Visualization and Application Integration

Used Python, pandas, Plotly, and Streamlit to integrate collaborative research outputs into an accessible application.

Additional contributions included:

- Improving dashboard navigation and usability.
- Developing reusable visualization components.
- Correcting Plotly title and labeling issues.
- Improving annual x-axis readability.
- Implementing dynamic vaccination coverage axis scaling.
- Integrating new state-level datasets.
- Developing and testing features through GitHub branches and pull requests.

---

## Dashboard Screenshots

The following screenshots demonstrate the interactive visualization, statistical interpretation, and data-quality features implemented within the application.

<div align="center">

<h3>MMP Master Dataset Explorer</h3>

<img
  src="images/MMP%20Master%20Dataset%20Explorer.png"
  alt="MMP Master Dataset Explorer"
  width="850"
/>

<p>
  <em>
    The Streamlit interface allows users to select diseases and states,
    explore historical trends, and examine data availability.
  </em>
</p>

<hr>

<h3>California and Florida Comparison</h3>

<img
  src="images/California%20and%20Florida%20Comparison.png"
  alt="California and Florida vaccination and measles incidence comparison"
  width="850"
/>

<p>
  <em>
    Comparative visualization of measles vaccination coverage and
    reported incidence across California and Florida from 1995–2017.
  </em>
</p>

<hr>

<h3>Florida Time-Lagged Analysis</h3>

<img
  src="images/Florida%20Time-Lagged%20Analysis.png"
  alt="Florida measles lag analysis"
  width="850"
/>

<p>
  <em>
    Interactive presentation of lagged Pearson correlations,
    p-values, sample sizes, and statistical interpretation.
  </em>
</p>

<hr>

<h3>Data Quality and Completeness</h3>

<img
  src="images/Data%20Quality%20and%20Completeness.png"
  alt="Data quality and completeness dashboard"
  width="850"
/>

<p>
  <em>
    State-level data completeness reporting with
    available measurements and underlying observations.
  </em>
</p>

</div>

---

## Data and Analytical Methodology

The collaborative project uses publicly available vaccination coverage, disease surveillance, and population data to examine vaccine-preventable disease patterns.

The analytical workflow includes two complementary components.

### Descriptive MMP Exploration

The MMP Master Explorer presents historical vaccination coverage and incidence trends for measles, mumps, and pertussis.

Users can compare California and Florida, inspect annual observations, and examine missing-data summaries.

This component is descriptive and does not independently calculate lagged correlations.

### State-Specific Measles Lag Analysis

The California and Florida State Case Studies present exploratory time-lagged associations between vaccination coverage and measles incidence.

The analysis compares vaccination coverage in year *t* with measles incidence in year *t + lag*, using lag periods from zero to five years.

Statistical results include:

- Pearson correlation coefficient (*r*).
- Statistical p-value.
- Number of matched observations (*n*).

The correlations are generated through the broader team's analytical workflow and incorporated into the dashboard for interactive examination.

### Data Sources

The project's master dataset integrates information derived from:

- CDC National Immunization Survey-Child (NIS-Child).
- Project Tycho disease surveillance data.
- Supplemental infectious disease surveillance records.
- Population estimates used to calculate incidence per 100,000 residents.

For detailed data transformations, analytical methodology, and source documentation, consult the original collaborative repository.

---

## Methodological Limitations

<table>
  <tr>
    <th align="left">Consideration</th>
    <th align="left">Interpretation</th>
  </tr>
  <tr>
    <td>Ecological Fallacy</td>
    <td>State-level associations cannot establish individual vaccination outcomes.</td>
  </tr>
  <tr>
    <td>Population Differences</td>
    <td>Vaccination coverage estimates and disease incidence measurements may represent different age groups.</td>
  </tr>
  <tr>
    <td>Missing Observations</td>
    <td>Missing values are not equivalent to zero reported cases.</td>
  </tr>
  <tr>
    <td>Sample Size</td>
    <td>Small analytical samples can produce unstable correlation estimates.</td>
  </tr>
  <tr>
    <td>Confounding</td>
    <td>Population characteristics, healthcare access, vaccination policies, surveillance practices, and temporal trends may influence observed associations.</td>
  </tr>
  <tr>
    <td>Statistical Significance</td>
    <td>P-values should be interpreted alongside effect sizes, sample sizes, and exploratory multiple-lag comparisons.</td>
  </tr>
  <tr>
    <td>Causation</td>
    <td>Observational correlations do not establish causal relationships.</td>
  </tr>
</table>

---

## Repository Structure

```text
vaccination-disease-incidence-dashboard/
│
├── README.md
├── Moira_Overly_Capstone_Contributions.ipynb
├── images/
│   ├── MMP Master Dataset Explorer.png
│   ├── California and Florida Comparison.png
│   ├── Florida Time-Lagged Analysis.png
│   └── Data Quality and Completeness.png
│
├── app/
│   ├── app.py
│   ├── data/
│   ├── pages/
│   ├── static/
│   └── .streamlit/
│
└── requirements.txt
```

The personal repository contains a copy of the collaborative Streamlit application, its supporting files, and documentation emphasizing my individual development contributions.

---

## Running the Application Locally

### 1. Clone the repository

```bash
git clone https://github.com/modata-analytics/vaccination-disease-incidence-dashboard.git

cd vaccination-disease-incidence-dashboard
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install project dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the application

```bash
python -m streamlit run app/app.py
```

The application requires the included datasets and supporting project files.

---

## Individual Contribution Documentation

My contribution notebook documents the technical work involved in developing and integrating the dashboard.

<a href="Moira_Overly_Capstone_Contributions.ipynb">
  <strong>View My Capstone Contributions Notebook</strong>
</a>

It provides additional information about implementation decisions, data quality, visualization development, and collaborative integration.

---

## Team Acknowledgment and Attribution

This project was developed collaboratively by **BIOT 670I Group 1 (2026)** at the University of Maryland Global Campus.

### Project Team

<table>
  <tr>
    <th align="left">Team Member</th>
    <th align="left">Project Affiliation</th>
  </tr>
  <tr>
    <td>Heba Bakry</td>
    <td>BIOT 670I Group 1</td>
  </tr>
  <tr>
    <td>Gloria Bukirwa</td>
    <td>BIOT 670I Group 1</td>
  </tr>
  <tr>
    <td>Moira Overly</td>
    <td>BIOT 670I Group 1</td>
  </tr>
  <tr>
    <td>Kalkidan Perin</td>
    <td>BIOT 670I Group 1</td>
  </tr>
  <tr>
    <td>Matthew Rada</td>
    <td>BIOT 670I Group 1</td>
  </tr>
</table>

I acknowledge my teammates for their contributions to the research, data preparation, statistical analyses, software development, and overall scientific direction of the project.

Our collective work included:

- Gathering and harmonizing public health datasets.
- Developing disease incidence and vaccination coverage measures.
- Investigating temporal and geographic trends.
- Conducting exploratory statistical analyses.
- Developing and maintaining the shared Streamlit application.
- Evaluating methodological limitations and scientific uncertainty.

**My individual contributions** focused on interactive dashboard development, MMP Master Explorer implementation, California and Florida measles case-study integration, data-quality reporting, visualization improvements, and scientific communication.

The underlying datasets, statistical results, and other application components reflect contributions from the broader team.

This repository is not intended to represent the complete project as independently developed work.

### Original Collaborative Repository

<a href="https://github.com/FusRaDa/biot670i_capstone_vaccination_project">
  <strong>BIOT 670I Group 1 — Original GitHub Repository</strong>
</a>

This personal repository preserves a copy of the collaborative application for educational and professional portfolio purposes, with an emphasis on my individual technical contributions.

---

## Project Purpose

This repository serves as a technical portfolio demonstrating experience with:

- Public health and epidemiological data.
- Python-based application development.
- Streamlit dashboard design.
- Interactive Plotly data visualization.
- Data-quality assessment.
- Statistical interpretation.
- Scientific communication.
- Git and collaborative software development.
- Integration of independently developed analytical components.

The application illustrates how epidemiological datasets and statistical results can be presented through interactive analytical tools while maintaining methodological transparency.

---

<div align="center">

### BIOT 670I Capstone Project — Group 1

**University of Maryland Global Campus | 2026**

*Collaborative research, reproducible analysis, and responsible scientific visualization.*

<p>
  <a href="https://github.com/FusRaDa/biot670i_capstone_vaccination_project">
    Original Project Repository
  </a>
</p>

</div>
