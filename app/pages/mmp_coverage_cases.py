import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Measles, Mumps, Pertussis Incidence & Coverage",
    page_icon="💉"
)

st.markdown("Measles, Mumps, Pertussis Incidence & Coverage: 1995 - 2017")
st.sidebar.header("Measles, Mumps, Pertussis Incidence & Coverage")

st.write(
    """
    ### Vaccine Coverage & Disease Incidence - Pooled Analysis

    Case Coverage Details
    - **Measles:** Project Tycho is used as the primary source for state-level measles case counts. Missing case data for **2003–2015** were supplemented using annual CDC MMWR/NNDSS surveillance reports.
    - **Mumps:** Project Tycho is used as the primary source for state-level mumps case counts. Missing case data for **2003–2010** were supplemented using annual CDC MMWR/NNDSS surveillance reports.
    - **Pertussis:** All state-level pertussis case counts are from **Project Tycho**. No additional MMWR/NNDSS case data were added for pertussis.
    
    When both Project Tycho and the supplemental MMWR/NNDSS dataset contain a value for the same state and year, the **Project Tycho value is retained**. MMWR/NNDSS values are used only to fill missing observations.

    Disease incidence is reported as **cases per 100,000 population**, allowing
    disease occurrence to be compared across years while accounting for changes
    in population size.

    Overall, the figure does not demonstrate a simple year-to-year relationship
    between national vaccination coverage and disease incidence. National estimates
    can conceal state-level differences, localized coverage gaps, and outbreaks.
    Therefore, this visualization is descriptive and should not be interpreted
    as evidence of a causal relationship.
    """
)


# -------------------------
# Load data
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

cases_df = pd.read_csv(DATA_DIR / "tycho_cases.csv")

missing_cases_df = pd.read_csv(DATA_DIR / "missing_cases.csv")

population_df = pd.read_csv(DATA_DIR / "population.csv")

coverage_df = pd.read_csv(DATA_DIR / "nis_vacc_coverage.csv")


# -------------------------
# Combine Tycho + MMWR cases
# -------------------------

cases_df = pd.merge(
    cases_df,
    missing_cases_df,
    on=["year", "state"],
    how="outer",
    suffixes=("_tycho", "_mmwr")
)


# Prefer Tycho values when available.
# Use MMWR to fill missing Tycho values.
cases_df["measles_cases"] = (
    cases_df["measles_cases_tycho"]
    .combine_first(
        cases_df["measles_cases_mmwr"]
    )
)

cases_df["mumps_cases"] = (
    cases_df["mumps_cases_tycho"]
    .combine_first(
        cases_df["mumps_cases_mmwr"]
    )
)


# Keep final case columns
cases_df = cases_df[
    [
        "year",
        "state",
        "measles_cases",
        "mumps_cases",
        "pertussis_cases"
    ]
]


# Sort
cases_df = cases_df.sort_values(
    ["state", "year"]
).reset_index(drop=True)


# -------------------------
# Merge population with cases
# -------------------------

cases_population_df = pd.merge(
    cases_df,
    population_df,
    on=["state", "year"],
    how="left"
)


# -------------------------
# Calculate national cases
# -------------------------

yearly_cases_df = (
    cases_population_df
    .groupby("year")[
        ["measles_cases", "mumps_cases", "pertussis_cases"]
    ]
    .sum(min_count=1)
    .reset_index()
)


# -------------------------
# Calculate national population
# -------------------------

yearly_population_df = (
    population_df
    .groupby("year")["population"]
    .sum(min_count=1)
    .reset_index()
)


# Merge cases and population
yearly_cases_df = pd.merge(
    yearly_cases_df,
    yearly_population_df,
    on="year",
    how="left"
)


# -------------------------
# Calculate cases per 100K
# -------------------------

diseases = ["measles", "mumps", "pertussis"]

for disease in diseases:

    yearly_cases_df[f"{disease}_cases_per_100k"] = (
        yearly_cases_df[f"{disease}_cases"]
        / yearly_cases_df["population"]
        * 100_000
    )


# -------------------------
# Calculate national coverage
# -------------------------

yearly_coverage_df = (
    coverage_df
    .groupby("year")[
        [
            "measles_coverage_pct",
            "mumps_coverage_pct",
            "pertussis_coverage_pct"
        ]
    ]
    .mean()
    .reset_index()
)


# -------------------------
# Merge coverage + incidence
# -------------------------

yearly_coverage_cases_df = pd.merge(
    yearly_cases_df,
    yearly_coverage_df,
    on="year"
)


# -------------------------
# Create figure
# -------------------------

fig = make_subplots(
    rows=3,
    cols=1,
    shared_xaxes=True,
    specs=[
        [{"secondary_y": True}],
        [{"secondary_y": True}],
        [{"secondary_y": True}]
    ],
    subplot_titles=["Measles", "Mumps", "Pertussis"],
    vertical_spacing=0.10
)

colors = {
    "measles": "#E74C3C",
    "mumps": "#3498DB",
    "pertussis": "#2ECC71"
}


for row, disease in enumerate(diseases, start=1):

    # Annual incidence per 100K
    fig.add_trace(
        go.Bar(
            x=yearly_coverage_cases_df["year"],
            y=yearly_coverage_cases_df[
                f"{disease}_cases_per_100k"
            ],
            name=f"{disease.title()} cases per 100K",
            marker_color=colors[disease],
            opacity=0.65,
            hovertemplate=(
                "Year: %{x}<br>"
                "Cases per 100K: %{y:.2f}"
                "<extra></extra>"
            )
        ),
        row=row,
        col=1,
        secondary_y=False
    )

    # Annual vaccination coverage
    fig.add_trace(
        go.Scatter(
            x=yearly_coverage_cases_df["year"],
            y=yearly_coverage_cases_df[
                f"{disease}_coverage_pct"
            ],
            name=f"{disease.title()} coverage",
            mode="lines+markers",
            line=dict(color="black", width=2),
            marker=dict(size=6),
            hovertemplate=(
                "Year: %{x}<br>"
                "Coverage: %{y:.2f}%"
                "<extra></extra>"
            )
        ),
        row=row,
        col=1,
        secondary_y=True
    )

    fig.update_yaxes(
        title_text="Cases per 100K",
        row=row,
        col=1,
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Coverage (%)",
        row=row,
        col=1,
        secondary_y=True
    )


fig.update_xaxes(
    title_text="Year",
    row=3,
    col=1,
    dtick=1
)


fig.update_layout(
    title="Annual Vaccination Coverage and Disease Incidence",
    template="plotly_white",
    height=900,
    hovermode="x unified",
    legend_title="Measure",
    bargap=0.20
)


st.plotly_chart(fig, width="stretch")