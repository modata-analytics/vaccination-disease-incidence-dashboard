import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Measles, Mumps, Pertussis Incidence & Coverage",
    page_icon="🇺🇸"
)

st.markdown(
    "Measles, Mumps, Pertussis Incidence & Coverage Per State: 1995 - 2017"
)

st.sidebar.header(
    "Measles, Mumps, Pertussis Incidence & Coverage Per State"
)

st.write(
    """
    ### Suggested States for Analysis

    **California** is useful for examining major pertussis epidemics in 2010
    and 2014 alongside vaccination coverage and subsequent policy changes.

    **Minnesota** experienced a major measles outbreak in 2017 associated with
    reduced MMR vaccination in a localized community.

    **Ohio** experienced a large measles outbreak in an underimmunized Amish
    community in 2014.

    **Washington** experienced a major pertussis epidemic in 2012, making it
    useful for examining changes in disease incidence alongside vaccination
    coverage.

    **New York** experienced a large mumps outbreak beginning in 2009,
    particularly within close-knit communities.

    **Arkansas** experienced a large mumps outbreak during 2016–2017.

    Disease incidence is shown as **cases per 100,000 population** rather than
    raw case counts. This adjusts for differences in state population and makes
    incidence more comparable across states and years.
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
# Merge datasets
# -------------------------

yearly_coverage_cases_df = pd.merge(
    cases_df,
    coverage_df,
    on=["year", "state"]
)

yearly_coverage_cases_df = pd.merge(
    yearly_coverage_cases_df,
    population_df,
    on=["year", "state"],
    how="left"
)


# -------------------------
# Calculate cases per 100K
# -------------------------

diseases = [
    "measles",
    "mumps",
    "pertussis"
]

for disease in diseases:

    yearly_coverage_cases_df[
        f"{disease}_cases_per_100k"
    ] = (
        yearly_coverage_cases_df[f"{disease}_cases"]
        / yearly_coverage_cases_df["population"]
        * 100_000
    )


# -------------------------
# State selection
# -------------------------

selected_state = st.selectbox(
    "Select a state",
    sorted(
        yearly_coverage_cases_df[
            "state"
        ].dropna().unique()
    )
)

filtered_df = yearly_coverage_cases_df[
    yearly_coverage_cases_df["state"] == selected_state
].copy()


# -------------------------
# Graph
# -------------------------

def graph_coverage_cases_df(df):

    diseases = [
        "measles",
        "mumps",
        "pertussis"
    ]

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": True}]
        ],
        subplot_titles=[
            "Measles",
            "Mumps",
            "Pertussis"
        ],
        vertical_spacing=0.10
    )

    colors = {
        "measles": "#E74C3C",
        "mumps": "#3498DB",
        "pertussis": "#2ECC71"
    }

    for row, disease in enumerate(
        diseases,
        start=1
    ):

        # Annual cases per 100K
        fig.add_trace(
            go.Bar(
                x=df["year"],
                y=df[
                    f"{disease}_cases_per_100k"
                ],
                name=(
                    f"{disease.title()} "
                    "cases per 100K"
                ),
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
                x=df["year"],
                y=df[
                    f"{disease}_coverage_pct"
                ],
                name=(
                    f"{disease.title()} coverage"
                ),
                mode="lines+markers",
                line=dict(
                    color="black",
                    width=2
                ),
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
        title=(
            f"Annual Vaccination Coverage "
            f"and Disease Incidence — {selected_state}"
        ),
        template="plotly_white",
        height=900,
        hovermode="x unified",
        legend_title="Measure",
        bargap=0.20
    )

    return fig


fig = graph_coverage_cases_df(
    filtered_df
)

st.plotly_chart(
    fig,
    width="stretch"
)