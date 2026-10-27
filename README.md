
<div align="center">

# Vaccination Coverage & Disease Incidence Dashboard

### Interactive Public Health Data Analytics

**BIOT 670I Capstone Project | University of Maryland Global Campus | 2026**

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-Data_Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Collaborative_Development-181717?logo=github&logoColor=white)

<p>
  <a href="https://biot670i-group1.streamlit.app/">
    <strong>Live Group Dashboard</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="https://github.com/FusRaDa/biot670i_capstone_vaccination_project">
    <strong>Original Group Repository</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="Moira_Overly_Capstone_Contributions.ipynb">
    <strong>My Contributions</strong>
  </a>
</p>

<p><em>Independent Streamlit deployment: Coming soon</em></p>

</div>

---

## Project Overview

This project explores the relationship between vaccination coverage and reported incidence of three vaccine-preventable diseases:

- **Measles**
- **Mumps**
- **Pertussis**

Developed collaboratively for the BIOT 670I Capstone Project, the application integrates vaccination coverage, disease surveillance, and population data into interactive visualizations and exploratory analytical tools.

The dashboard enables users to examine historical disease trends, compare geographic patterns, investigate time-lagged associations, and assess data completeness.

### Research Question

> How are changes in vaccination coverage associated with the incidence of vaccine-preventable diseases across geographic regions and time?

The project uses an ecological observational approach. Its findings are exploratory and do not establish causal relationships.

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
    <td>Dashboard Development, Data Visualization, Data Quality Integration</td>
  </tr>
  <tr>
    <td>Technologies</td>
    <td>Python, Streamlit, pandas, Plotly, Git, GitHub</td>
  </tr>
  <tr>
    <td>Primary Case Studies</td>
    <td>California and Florida</td>
  </tr>
  <tr>
    <td>Historical Data</td>
    <td>1995–2017</td>
  </tr>
</table>

---

## My Technical Contributions

My primary responsibility was developing and refining the user-facing Streamlit dashboard, integrating team-produced analytical outputs, and improving the presentation of statistical uncertainty and data quality.

### 1. MMP Master Dataset Explorer

Developed an interactive Streamlit interface for exploring vaccination coverage and disease incidence across California and Florida.

**Key features:**

- Interactive measles, mumps, and pertussis selection.
- California and Florida state comparisons.
- Historical vaccination coverage visualizations.
- Disease incidence rates per 100,000 residents.
- Disease-specific data-completeness reporting.
- Missing-observation identification.
- Dynamic chart scaling and improved readability.

### 2. California and Florida Measles Case Studies

Developed and expanded dedicated state-level analytical interfaces.

**Key features:**

- Historical vaccination coverage and measles incidence charts.
- Interactive selection of 0–5-year lag periods.
- Display of Pearson correlation coefficients.
- Statistical p-values and observation counts.
- Integration of revised team-generated lag results.
- Sample-size warnings and statistical interpretation.
- Historical policy context and methodological limitations.

### 3. Data Quality and Analytical Transparency

Implemented data-quality features to help users assess the completeness and reliability of the observations supporting each analysis.

These features include:

- Identification of missing annual observations.
- Calculation of data completeness percentages.
- Calendar-year lag-pair validation.
- Comparison of available and reported statistical sample sizes.
- Explanations of confounding and ecological fallacy.
- Distinction between correlation and causation.

### 4. Visualization and Application Integration

Used Python, pandas, Plotly, and Streamlit to integrate datasets and statistical results into an interactive application.

Additional contributions included improving application usability, troubleshooting chart-rendering issues, standardizing visualizations, and developing features through GitHub branches and pull requests.

---

## Dashboard Screenshots

<div align="center">

### MMP Master Dataset Explorer

<img src="images/mmp_explorer.png" alt="MMP Master Dataset Explorer" width="850">

<em>Interactive exploration of vaccination coverage and disease incidence across California and Florida.</em>

<br><br>

### California and Florida Comparison

<img src="images/state_comparison.png" alt="California and Florida vaccination comparison" width="850">

<em>Comparative visualization of state-level epidemiological trends.</em>

<br><br>

### Florida Time-Lagged Analysis

<img src="images/florida_lag_analysis.png" alt="Florida measles time-lagged analysis" width="850">

<em>Interactive presentation of Pearson correlation, statistical significance, and sample size across lag periods.</em>

<br><br>

### Data Quality and Completeness

<img src="images/data_quality.png" alt="Data quality and completeness dashboard" width="850">

<em>Reporting of available observations, missing data, and calendar-year pair validation.</em>

</div>

---

## Data and Methodology

The collaborative project combines publicly available vaccination coverage, disease surveillance, and population datasets.

Its analytical workflow includes descriptive comparisons and exploratory time-lagged associations.

My dashboard contributions focus on integrating, validating, visualizing, and explaining these analytical outputs.

The **MMP Master Explorer** provides descriptive information for measles, mumps, and pertussis.

The **California and Florida State Case Studies** provide additional measles-specific lag analyses generated through the group's statistical workflow.

### Methodological Limitations

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
    <td>Vaccination coverage and disease incidence data may represent different age groups.</td>
  </tr>
  <tr>
    <td>Missing Data</td>
    <td>Missing observations are not equivalent to zero reported cases.</td>
  </tr>
  <tr>
    <td>Statistical Uncertainty</td>
    <td>Correlations must be interpreted alongside sample sizes and p-values.</td>
  </tr>
  <tr>
    <td>Confounding</td>
    <td>Population characteristics, policies, reporting practices, and temporal trends may influence results.</td>
  </tr>
  <tr>
    <td>Causation</td>
    <td>Observational correlations do not establish causal relationships.</td>
  </tr>
</table>

---

## Running the Application Locally

### 1. Clone the repository

```bash
git clone https://github.com/modata-analytics/vaccination-disease-incidence-dashboard.git
cd vaccination-disease-incidence-dashboard
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Launch Streamlit

```bash
python -m streamlit run app/app.py
```

The application requires the included datasets and supporting project files.

---

## Individual Contribution Documentation

For additional information about my dashboard development, implementation decisions, and validation procedures, see:

<a href="Moira_Overly_Capstone_Contributions.ipynb">
  <strong>Moira Overly — Capstone Contributions Notebook</strong>
</a>

The notebook provides supporting technical documentation for my individual role within the collaborative project.

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

I acknowledge my teammates for their contributions to the research, data preparation, statistical analyses, software development, and scientific direction of the project.

The collaborative work included:

- Gathering and harmonizing public health datasets.
- Developing analytical methods.
- Investigating vaccination coverage and disease incidence.
- Conducting exploratory time-lagged analyses.
- Developing and maintaining the shared Streamlit application.
- Evaluating methodological limitations and uncertainty.

My individual contributions focused primarily on dashboard development, the MMP Master Explorer, California and Florida measles case-study integration, data-quality reporting, and user-interface improvements.

The underlying datasets and statistical results reflect contributions from the broader team. This repository does not represent the entire project as independently developed work.

### Original Collaborative Project

<a href="https://github.com/FusRaDa/biot670i_capstone_vaccination_project">
  <strong>BIOT 670I Group 1 — Original GitHub Repository</strong>
</a>

This personal repository preserves a copy of the collaborative application for educational and portfolio purposes while highlighting my individual contributions. It is not intended to replace the original project or claim sole authorship.

---

## Project Purpose

This repository serves as a technical portfolio demonstrating experience with:

- Public health and epidemiological data.
- Python-based dashboard development.
- Interactive data visualization.
- Data-quality assessment.
- Statistical interpretation and scientific communication.
- Collaborative GitHub development.
- Integration of analytical results into user-facing applications.

The application demonstrates how epidemiological datasets and analytical outputs can be presented through accessible interactive tools while maintaining appropriate scientific transparency.

---

<div align="center">

### BIOT 670I Capstone Project — Group 1

**University of Maryland Global Campus | 2026**

<em>Collaborative research, reproducible analysis, and responsible scientific visualization.</em>

<br><br>

<a href="https://github.com/FusRaDa/biot670i_capstone_vaccination_project">
  Original Project Repository
</a>

</div>
