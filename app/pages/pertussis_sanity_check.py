from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.stats import pearsonr


st.set_page_config(
    page_title="Pertussis Sanity Check",
    page_icon=":material/person_search:",
    layout="wide",
)

st.title("Pertussis Sanity Check")


st.write(
    """
    ### Pertussis Vaccination Coverage and Incidence Analysis

    This analysis examines the relationship between **DTaP vaccination coverage**
    and **pertussis incidence among young children in the United States**
    from **1995 through 2017**.

    **Pertussis Incidence**

    Pertussis incidence is analyzed for children **1–6 years of age**. Incidence is reported as the number of
    cases per 100,000 children within this age group.

    These age-specific incidence rates were obtained from
    [CDC Pertussis Surveillance and Trends](https://www.cdc.gov/pertussis/php/surveillance/index.html),
    which uses data from the **National Notifiable Diseases Surveillance
    System (NNDSS)**. Because the data are already expressed as incidence
    rates, no additional population normalization is performed.

    **DTaP Vaccination Coverage**

    State-level DTaP vaccination coverage for children aged **19–35 months**
    was obtained from the
    [CDC National Immunization Survey–Child (NIS-Child)](https://www.cdc.gov/childvaxview/).

    Annual vaccination coverage is summarized using the **unweighted average**
    of available state-level vaccination coverage percentages. Each state
    contributes equally to the average.

    **Time-Lagged Correlation Analysis**

    To investigate whether vaccination coverage is associated with
    pertussis incidence in the same or subsequent years, the analysis
    evaluates time lags of **0 through 5 years**.

    Six scatterplots compare vaccination coverage in year **t − lag**
    with pertussis incidence in year **t**, for children aged 1–6 years.

    Pearson correlation coefficients (r) and p-values are calculated
    for each lag to evaluate the strength, direction,
    and statistical significance of the observed associations.

    **Interpretation and Limitations**

    This is an ecological analysis using population-level vaccination
    coverage and disease incidence data. The vaccination coverage
    population (19–35 months) differs from the pertussis incidence
    age group (1–6 years).

    The unweighted state average is not equivalent to a nationally
    population-weighted vaccination coverage estimate.

    Correlation does not establish causation, and observed associations
    may be influenced by other factors, including vaccination schedules,
    waning immunity, disease outbreaks, and changes in surveillance.
    """
)

# Resolve data paths relative to this Streamlit page/repository rather than the
# process working directory. Adjust DATA_DIR if this page lives elsewhere.
PAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PAGE_DIR.parent / "data" if PAGE_DIR.name == "pages" else PAGE_DIR / "data"


@st.cache_data
def load_data():
    pertussis_df = pd.read_csv(DATA_DIR / "pertussis_age.csv")
    ms_df = pd.read_csv(DATA_DIR / "cases_coverage_ms.csv")
    return pertussis_df, ms_df


@st.cache_data
def build_sanity_df(pertussis_df, ms_df):
    vacc_coverage_df = ms_df[["year", "pertussis_coverage_pct"]].copy()

    avg_vacc_coverage_df = (
        vacc_coverage_df.groupby("year", as_index=False)["pertussis_coverage_pct"]
        .mean()
        .rename(columns={"pertussis_coverage_pct": "avg_pertussis_coverage_pct"})
    )

    min_vacc_coverage_df = (
        vacc_coverage_df.groupby("year", as_index=False)["pertussis_coverage_pct"]
        .min()
        .rename(columns={"pertussis_coverage_pct": "min_pertussis_coverage_pct"})
    )

    max_vacc_coverage_df = (
        vacc_coverage_df.groupby("year", as_index=False)["pertussis_coverage_pct"]
        .max()
        .rename(columns={"pertussis_coverage_pct": "max_pertussis_coverage_pct"})
    )

    child_pertussis_cases_df = pertussis_df[["Year", "1-6 yrs"]].copy()
    child_pertussis_cases_df = child_pertussis_cases_df.rename(columns={"Year": "year"})

    sanity_df = (
        avg_vacc_coverage_df
        .merge(max_vacc_coverage_df, on="year", how="outer")
        .merge(min_vacc_coverage_df, on="year", how="outer")
        .merge(child_pertussis_cases_df, on="year", how="outer")
        .sort_values("year")
        .reset_index(drop=True)
    )

    return sanity_df


def graph_pertussis_age_coverage(df):
    df = df.sort_values("year")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    colors = {
        "1-6 yrs": "#F39C12",
    }

    for age_group, color in colors.items():
        fig.add_trace(
            go.Bar(
                x=df["year"],
                y=df[age_group],
                name=age_group,
                marker_color=color,
                hovertemplate=(
                    "Year: %{x}<br>"
                    f"Age group: {age_group}<br>"
                    "Incidence: %{y:.2f}"
                    "<extra></extra>"
                ),
            ),
            secondary_y=False,
        )

    coverage_lines = {
        "avg_pertussis_coverage_pct": {
            "name": "Average DTaP Coverage (%)",
            "color": "#3498DB",
            "dash": "solid",
        },
    }

    for column, settings in coverage_lines.items():
        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=df[column],
                name=settings["name"],
                mode="lines+markers",
                line=dict(
                    color=settings["color"],
                    width=3,
                    dash=settings["dash"],
                ),
                marker=dict(size=7),
                hovertemplate=(
                    "Year: %{x}<br>"
                    f"{settings['name']}: %{{y:.2f}}%"
                    "<extra></extra>"
                ),
            ),
            secondary_y=True,
        )

    fig.update_yaxes(
        title_text="Pertussis Incidence (Cases per 100K)",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Vaccination Coverage (%)",
        range=[0, 100],
        secondary_y=True,
    )
    fig.update_xaxes(title_text="Year", dtick=1)

    fig.update_layout(
        title="National Pertussis Incidence (Ages 1–6) & DTaP Coverage",
        barmode="group",
        height=550,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(t=110),
    )

    return fig


def pearson_pertussis_age(df, start_year=None, end_year=None, lag_years=0):
    age_groups = ["1-6 yrs"]

    coverage_columns = {"avg_pertussis_coverage_pct": "Average"}

    if not isinstance(lag_years, int) or lag_years < 0:
        raise ValueError("lag_years must be a non-negative integer")

    results = []
    data = df.copy().sort_values("year")

    if start_year is not None:
        data = data[data["year"] >= start_year]
    if end_year is not None:
        data = data[data["year"] <= end_year]

    coverage_data = df[["year"] + list(coverage_columns)].copy()
    coverage_data["year"] = coverage_data["year"] + lag_years

    data = data[["year"] + age_groups].merge(
        coverage_data,
        on="year",
        how="left",
        validate="one_to_one",
    )

    for age_group in age_groups:
        for coverage_col, coverage_name in coverage_columns.items():
            valid = data[["year", coverage_col, age_group]].dropna()
            x = valid[coverage_col]
            y = valid[age_group]
            n = len(valid)

            if n >= 3 and x.nunique() > 1 and y.nunique() > 1:
                r, p = pearsonr(x, y)
            else:
                r, p = np.nan, np.nan

            results.append(
                {
                    "age_group": age_group,
                    "coverage_type": coverage_name,
                    "lag_years": lag_years,
                    "start_year": start_year,
                    "end_year": end_year,
                    "n": n,
                    "pearson_r": r,
                    "p_value": p,
                    "significant_0_05": bool(p < 0.05) if np.isfinite(p) else False,
                }
            )

    return pd.DataFrame(results)


def graph_correlation(df, coverage_col, coverage_label, lag, start_year, end_year):
    coverage = df[["year", coverage_col]].copy()
    coverage["year"] += lag
    incidence = df[df["year"].between(start_year, end_year)]
    paired = incidence[["year", "1-6 yrs"]].merge(
        coverage, on="year", how="left", validate="one_to_one"
    )
    fig = go.Figure()
    for age, color in [("1-6 yrs", "#F39C12")]:
        valid = paired[["year", coverage_col, age]].dropna()
        x, y = valid[coverage_col].astype(float), valid[age].astype(float)
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="markers", name=age,
            marker=dict(color=color, size=9),
            customdata=valid[["year"]].to_numpy(),
            hovertemplate="Incidence year: %{customdata[0]}<br>Coverage: %{x:.2f}%<br>Incidence: %{y:.2f} per 100K<extra></extra>",
        ))
        if len(valid) >= 3 and x.nunique() > 1 and y.nunique() > 1:
            r, p = pearsonr(x, y)
            slope, intercept = np.polyfit(x, y, 1)
            xs = np.linspace(x.min(), x.max(), 100)
            fig.add_trace(go.Scatter(
                x=xs, y=slope * xs + intercept, mode="lines",
                name=f"{age} trend (r={r:.3f}, p={p:.3g})",
                line=dict(color=color, dash="dash"), hoverinfo="skip",
            ))
    fig.update_layout(
        title=f"{coverage_label} DTaP Coverage vs Pertussis Incidence — {lag}-Year Lag",
        xaxis_title=f"{coverage_label} DTaP Coverage (%)",
        yaxis_title="Pertussis Incidence (Cases per 100K)",
        height=470,
        legend=dict(orientation="h", y=-0.25),
        margin=dict(b=110),
    )
    return fig


try:
    pertussis_df, ms_df = load_data()
    sanity_df = build_sanity_df(pertussis_df, ms_df)
except FileNotFoundError as exc:
    st.error(f"Unable to load required CSV: {exc}")
    st.stop()

available_years = sanity_df["year"].dropna().astype(int)
default_start = max(1995, int(available_years.min()))
default_end = min(2017, int(available_years.max()))

st.sidebar.header("Analysis Settings")
start_year, end_year = st.sidebar.slider(
    "Incidence year range",
    min_value=1995,
    max_value=2017,
    value=(default_start, default_end),
)

filtered_df = sanity_df[sanity_df["year"].between(start_year, end_year)].copy()

st.subheader("Pertussis Incidence & DTaP Coverage")
st.plotly_chart(
    graph_pertussis_age_coverage(filtered_df),
    width="stretch",
)

st.subheader("Average DTaP Coverage vs Pertussis: 0–5 Year Lags")
st.write(
    f"Six graphs compare average DTaP coverage in year **t − lag** with "
    f"pertussis incidence in year **t**, for incidence years "
    f"**{start_year}–{end_year}**. Each chart shows incidence among children aged 1–6 years."
)

all_results = pd.concat(
    [
        pearson_pertussis_age(
            sanity_df, start_year=start_year, end_year=end_year, lag_years=lag
        )
        for lag in range(6)
    ],
    ignore_index=True,
)

for lag in range(6):
    st.plotly_chart(
        graph_correlation(
            sanity_df, "avg_pertussis_coverage_pct", "Average",
            lag, start_year, end_year,
        ),
        width="stretch",
        key=f"pertussis_lag_{lag}",
    )

st.subheader("Pearson Correlation Summary (All Lags)")

st.dataframe(
    all_results.style.format(
        {"pearson_r": "{:.3f}", "p_value": "{:.4f}"},
        na_rep="—",
    ),
    width="stretch",
    hide_index=True,
)

st.caption(
    "Pertussis incidence source: CDC pertussis surveillance. "
    "Vaccination coverage is the unweighted mean of available state-level percentages."
)