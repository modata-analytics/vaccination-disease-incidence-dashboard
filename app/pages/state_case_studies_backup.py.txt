
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# BIOT 670I CAPSTONE PROJECT - GROUP 1
# STATE CASE STUDIES
# California and Florida Measles Analysis
# ============================================================


# ------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

STATE_CONFIG = {
    "California": {
        "code": "CA",
        "analysis_file": "california_measles_analysis.csv",
        "lag_file": "california_measles_lag_results.csv",
    },
    "Florida": {
        "code": "FL",
        "analysis_file": "florida_measles_analysis.csv",
        "lag_file": "florida_measles_lag_results.csv",
    },
}

COLORS = {
    "coverage": "#70BDF2",
    "incidence": "#087CE5",
    "positive": "#49BFA0",
    "negative": "#E18A8A",
}


# ------------------------------------------------------------
# 2. DATA LOADING
# ------------------------------------------------------------

@st.cache_data
def load_state_data(analysis_file, lag_file):

    analysis = pd.read_csv(DATA_DIR / analysis_file)
    lag_results = pd.read_csv(DATA_DIR / lag_file)

    required_analysis = [
        "year",
        "measles_coverage_pct",
        "measles_cases_per_100k",
    ]

    required_lag = [
        "lag_years",
        "pearson_r",
        "p_value",
        "n",
    ]

    for name, df, required in [
        ("Analysis", analysis, required_analysis),
        ("Lag analysis", lag_results, required_lag),
    ]:
        missing = set(required) - set(df.columns)

        if missing:
            raise ValueError(
                f"{name} file is missing columns: {sorted(missing)}"
            )

    analysis = analysis.copy()
    lag_results = lag_results.copy()

    for column in required_analysis:
        analysis[column] = pd.to_numeric(
            analysis[column],
            errors="coerce",
        )

    for column in required_lag:
        lag_results[column] = pd.to_numeric(
            lag_results[column],
            errors="coerce",
        )

    analysis = analysis.sort_values("year")
    lag_results = lag_results.dropna(
        subset=required_lag
    ).sort_values("lag_years")

    return analysis, lag_results


# ------------------------------------------------------------
# 3. CHART FORMATTING
# ------------------------------------------------------------

def format_year_chart(fig, y_title, first_year, last_year):

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=25, t=20, b=110),
        font=dict(size=12),
        hovermode="closest",
    )

    # Remove Plotly titles entirely.
    # Streamlit provides the chart headings.
    fig.layout.title = None

    fig.update_xaxes(
        title_text="Year",
        type="linear",
        tickmode="linear",
        tick0=first_year,
        dtick=1,
        tickangle=60,
        tickfont=dict(size=10),
        range=[first_year - 0.5, last_year + 0.5],
        showgrid=False,
        automargin=True,
    )

    fig.update_yaxes(
        title_text=y_title,
        showgrid=True,
        gridcolor="rgba(150,150,150,0.20)",
        automargin=True,
        rangemode="tozero" if "Cases" in y_title else "normal",
    )

    return fig


def consecutive_segments(df):
    """Split observations when calendar years are missing."""

    df = df.sort_values("year").copy()

    if df.empty:
        return []

    groups = (
        df["year"].diff().fillna(1).ne(1).cumsum()
    )

    return [
        section for _, section in df.groupby(groups)
    ]


# ------------------------------------------------------------
# 4. PAGE HEADER
# ------------------------------------------------------------

st.title("State Case Studies")

st.caption("BIOT 670I Capstone Project | Group 1")

st.markdown(
    """
    Explore the relationship between vaccination coverage
    and measles incidence across California and Florida.

    This ecological analysis examines historical patterns,
    time-lagged associations, data completeness, and
    methodological uncertainty.
    """
)

st.divider()


# ------------------------------------------------------------
# 5. STATE SELECTION
# ------------------------------------------------------------

selected_state = st.selectbox(
    "Select a State",
    list(STATE_CONFIG.keys()),
)

config = STATE_CONFIG[selected_state]

try:
    analysis_df, lag_df = load_state_data(
        config["analysis_file"],
        config["lag_file"],
    )

except (FileNotFoundError, ValueError, pd.errors.EmptyDataError) as error:
    st.error(
        "The selected state's data could not be loaded. "
        "Check the CSV files in app/data."
    )
    st.exception(error)
    st.stop()

# Check state identifiers when present
if "state" in analysis_df.columns:
    analysis_df = analysis_df[
        analysis_df["state"] == config["code"]
    ].copy()

if "state" in lag_df.columns:
    lag_df = lag_df[
        lag_df["state"] == config["code"]
    ].copy()

valid_trends = analysis_df.dropna(
    subset=[
        "year",
        "measles_coverage_pct",
        "measles_cases_per_100k",
    ]
).copy()

valid_trends["year"] = valid_trends["year"].astype(int)

if valid_trends.empty or lag_df.empty:
    st.error("No valid data were found for this state.")
    st.stop()

# Guard against repeated years
if valid_trends["year"].duplicated().any():
    st.error(
        "Duplicate state-year observations were found. "
        "Please validate the input dataset."
    )
    st.stop()

first_year = int(analysis_df["year"].min())
last_year = int(analysis_df["year"].max())


# ------------------------------------------------------------
# 6. STATE OVERVIEW
# ------------------------------------------------------------

st.header(f"{selected_state}: Measles Analysis")

st.info(
    "Charts and statistics use the selected state's "
    "measles analysis files. Missing observations "
    "are not interpolated."
)

st.subheader("Dataset Overview")

overview1, overview2, overview3 = st.columns(3)

with overview1:
    st.metric(
        "Complete Annual Observations",
        len(valid_trends),
    )

with overview2:
    st.metric(
        "Mean Vaccination Coverage",
        f"{valid_trends['measles_coverage_pct'].mean():.2f}%",
    )

with overview3:
    st.metric(
        "Lag Periods",
        lag_df["lag_years"].nunique(),
    )

st.caption(
    "Mean coverage is an unweighted average of the "
    "available yearly estimates, not a population-weighted "
    "vaccination estimate."
)


# ------------------------------------------------------------
# 7. HISTORICAL CONTEXT
# ------------------------------------------------------------

st.subheader("Historical Context")

if selected_state == "California":

    st.markdown(
        """
        California's historical school-entry vaccination
        requirements provide policy context for examining
        measles trends.

        Requirements introduced around 1999 affected
        students entering seventh grade.

        **Population limitation:** NIS-Child estimates
        represent younger children than those directly
        affected by the seventh-grade requirements.

        These data cannot independently establish
        the effectiveness of that policy.
        """
    )

else:

    st.markdown(
        """
        Florida provides a second geographic case study
        for exploring vaccination coverage and measles
        incidence over time.

        State-specific demographic characteristics,
        immunization policies, population movement,
        and reporting practices may influence observed
        patterns.

        Policy effects are not estimated in this analysis.
        """
    )


# ------------------------------------------------------------
# 8. VACCINATION AND INCIDENCE TRENDS
# ------------------------------------------------------------

st.divider()

st.subheader("Vaccination Coverage and Disease Incidence")

st.caption(
    "Only observed years are plotted. Lines break across "
    "missing years; missing incidence is not treated as zero."
)

# Coverage may be available where incidence is missing.
coverage_df = analysis_df.dropna(
    subset=["year", "measles_coverage_pct"]
).copy()

coverage_df["year"] = coverage_df["year"].astype(int)

incidence_df = analysis_df.dropna(
    subset=["year", "measles_cases_per_100k"]
).copy()

incidence_df["year"] = incidence_df["year"].astype(int)


# CHART 1: VACCINATION COVERAGE

st.markdown(
    f"#### {selected_state} Measles Vaccination Coverage"
)

coverage_fig = go.Figure()

for segment in consecutive_segments(coverage_df):

    coverage_fig.add_trace(
        go.Scatter(
            x=segment["year"],
            y=segment["measles_coverage_pct"],
            mode="lines+markers",
            showlegend=False,
            line=dict(
                color=COLORS["coverage"],
                width=3,
            ),
            marker=dict(size=8),
            hovertemplate=(
                "Year: %{x}<br>"
                "Coverage: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

format_year_chart(
    coverage_fig,
    "Vaccination Coverage (%)",
    first_year,
    last_year,
)

st.plotly_chart(
    coverage_fig,
    use_container_width=True,
    key=f"{config['code']}_coverage",
)


# CHART 2: MEASLES INCIDENCE

st.markdown(
    f"#### {selected_state} Measles Incidence"
)

incidence_fig = go.Figure()

incidence_fig.add_trace(
    go.Bar(
        x=incidence_df["year"],
        y=incidence_df["measles_cases_per_100k"],
        showlegend=False,
        marker_color=COLORS["incidence"],
        width=0.75,
        hovertemplate=(
            "Year: %{x}<br>"
            "Incidence: %{y:.4f} cases per 100,000"
            "<extra></extra>"
        ),
    )
)

format_year_chart(
    incidence_fig,
    "Cases per 100,000 Population",
    first_year,
    last_year,
)

st.plotly_chart(
    incidence_fig,
    use_container_width=True,
    key=f"{config['code']}_incidence",
)

st.caption(
    "These visualizations describe ecological trends. "
    "They cannot establish individual-level vaccine effects."
)


# ------------------------------------------------------------
# 9. INTERACTIVE LAG ANALYSIS
# ------------------------------------------------------------

st.divider()

st.subheader("Time-Lagged Association Analysis")

st.markdown(
    """
    Select a lag to examine the reported relationship
    between vaccination coverage and measles incidence.

    A **0-year lag** compares measurements in the same
    calendar year.

    A **1-year lag** compares coverage in year *t*
    with incidence in year *t + 1*.
    """
)

lag_options = sorted(
    lag_df["lag_years"].astype(int).unique().tolist()
)

selected_lag = st.select_slider(
    "Lag Period (Years)",
    options=lag_options,
    value=lag_options[0],
)

result = lag_df.loc[
    lag_df["lag_years"] == selected_lag
].iloc[0]

r = float(result["pearson_r"])
p = float(result["p_value"])
n = int(result["n"])

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("Pearson r", f"{r:.3f}")

with metric2:
    st.metric("P-value", f"{p:.4f}")

with metric3:
    st.metric("Observations (n)", n)


# ------------------------------------------------------------
# 10. DYNAMIC INTERPRETATION
# ------------------------------------------------------------

st.markdown("#### Statistical Interpretation")

if r < 0:
    direction = "negative"
    description = (
        "higher vaccination coverage corresponds to "
        "lower measured incidence in the analyzed pairs"
    )
elif r > 0:
    direction = "positive"
    description = (
        "higher vaccination coverage corresponds to "
        "higher measured incidence in the analyzed pairs"
    )
else:
    direction = "zero"
    description = "no linear association was observed"

st.write(
    f"The {selected_lag}-year lag has a {direction} "
    f"Pearson correlation (r = {r:.3f}, n = {n}). "
    f"Descriptively, {description}."
)

if n < 5:
    st.warning(
        "Very small sample size. The correlation estimate "
        "may be highly unstable."
    )
elif n < 10:
    st.info(
        "Limited observations are available. "
        "Interpret the correlation cautiously."
    )

if p >= 0.05:
    st.caption(
        "The reported association does not reach the "
        "conventional p < 0.05 threshold."
    )
else:
    st.caption(
        "The reported association meets p < 0.05. "
        "This does not establish causation."
    )

st.caption(
    "Associations may be influenced by confounding, "
    "temporal trends, missing observations, and "
    "differences in sampled populations."
)


# ------------------------------------------------------------
# 11. ALL LAG CORRELATIONS
# ------------------------------------------------------------

st.divider()

st.subheader("Comparison Across All Lag Periods")

correlation_fig = go.Figure()

bar_colors = [
    COLORS["negative"] if value < 0
    else COLORS["positive"]
    for value in lag_df["pearson_r"]
]

correlation_fig.add_trace(
    go.Bar(
        x=lag_df["lag_years"],
        y=lag_df["pearson_r"],
        marker_color=bar_colors,
        customdata=lag_df[
            ["p_value", "n"]
        ].to_numpy(),
        showlegend=False,
        hovertemplate=(
            "Lag: %{x} years<br>"
            "Pearson r: %{y:.3f}<br>"
            "P-value: %{customdata[0]:.4f}<br>"
            "Observations: %{customdata[1]:.0f}"
            "<extra></extra>"
        ),
    )
)

correlation_fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    height=420,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=55, r=25, t=20, b=65),
    xaxis=dict(
        title="Lag Period (Years)",
        dtick=1,
    ),
    yaxis=dict(
        title="Pearson Correlation (r)",
        range=[-1, 1],
        gridcolor="rgba(150,150,150,0.20)",
    ),
)

correlation_fig.layout.title = None

correlation_fig.add_hline(
    y=0,
    line_color="gray",
    line_dash="dash",
)

st.plotly_chart(
    correlation_fig,
    use_container_width=True,
    key=f"{config['code']}_lag_comparison",
)

st.caption(
    "Lag coefficients are loaded from the group's "
    "state-specific analysis files. They have not "
    "been recalculated by this dashboard."
)


# ------------------------------------------------------------
# 12. DATA QUALITY AND COMPLETENESS
# ------------------------------------------------------------

st.divider()

st.subheader("Data Quality & Completeness")

st.markdown(
    "Data availability is assessed separately for "
    "the selected state."
)

observed_years = sorted(
    valid_trends["year"].unique().tolist()
)

all_years = set(
    range(first_year, last_year + 1)
)

missing_years = sorted(
    all_years - set(observed_years)
)

completeness = (
    len(observed_years) / len(all_years) * 100
)

q1, q2, q3 = st.columns(3)

with q1:
    st.metric("Complete Years", len(observed_years))

with q2:
    st.metric("Incomplete Years", len(missing_years))

with q3:
    st.metric("Year Coverage", f"{completeness:.1f}%")

st.caption(
    "A complete year has both vaccination coverage "
    "and measles incidence available."
)

with st.expander("View Incomplete Years"):

    if missing_years:
        st.write(", ".join(map(str, missing_years)))
    else:
        st.success(
            "All years in the selected period have "
            "both measurements."
        )


# ------------------------------------------------------------
# 13. CALENDAR-YEAR LAG PAIR VALIDATION
# ------------------------------------------------------------

available_years = set(observed_years)

lag_rows = []

for lag in lag_options:

    valid_pairs = [
        (year, year + lag)
        for year in observed_years
        if year + lag in available_years
    ]

    lag_rows.append({
        "Lag (Years)": lag,
        "Calendar-Year Pairs": len(valid_pairs),
        "Year Pairs": ", ".join(
            f"{start} to {end}"
            for start, end in valid_pairs
        ),
    })

quality_df = pd.DataFrame(lag_rows)

reported = lag_df[
    ["lag_years", "n"]
].rename(
    columns={
        "lag_years": "Lag (Years)",
        "n": "Reported Pairs",
    }
)

comparison_df = quality_df.merge(
    reported,
    on="Lag (Years)",
    how="left",
)

comparison_df["Counts Match"] = (
    comparison_df["Calendar-Year Pairs"]
    == comparison_df["Reported Pairs"]
)

st.markdown("#### Available Observations by Lag")

quality_fig = go.Figure()

quality_fig.add_trace(
    go.Bar(
        x=comparison_df["Lag (Years)"],
        y=comparison_df["Calendar-Year Pairs"],
        marker_color=COLORS["coverage"],
        showlegend=False,
        hovertemplate=(
            "Lag: %{x} years<br>"
            "Available pairs: %{y}"
            "<extra></extra>"
        ),
    )
)

quality_fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    height=360,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=55, r=25, t=20, b=60),
    xaxis=dict(
        title="Lag Period (Years)",
        dtick=1,
    ),
    yaxis=dict(
        title="Calendar-Year Pairs",
        rangemode="tozero",
    ),
)

quality_fig.layout.title = None

st.plotly_chart(
    quality_fig,
    use_container_width=True,
    key=f"{config['code']}_quality",
)

if comparison_df["Counts Match"].all():

    st.success(
        "Reported lag sample sizes match the "
        "available calendar-year observation counts."
    )

else:

    st.warning(
        "Some reported lag sample sizes differ from "
        "the calendar-year availability counts. "
        "This requires additional review."
    )

with st.expander("View Lag Pair Details"):

    st.dataframe(
        comparison_df.drop(columns=["Year Pairs"]),
        hide_index=True,
        use_container_width=True,
    )

    detail_lag = st.selectbox(
        "Inspect Lag Period",
        lag_options,
        key=f"{config['code']}_pair_inspector",
    )

    selected_pairs = comparison_df.loc[
        comparison_df["Lag (Years)"] == detail_lag,
        "Year Pairs",
    ].iloc[0]

    st.write(selected_pairs if selected_pairs else "No pairs")


# ------------------------------------------------------------
# 14. SOURCE DATA AND STATISTICAL TABLES
# ------------------------------------------------------------

st.divider()

st.subheader("Data and Statistical Results")

with st.expander("View Annual Observations"):

    st.dataframe(
        analysis_df,
        hide_index=True,
        use_container_width=True,
    )

with st.expander("View Reported Lag Results"):

    st.dataframe(
        lag_df,
        hide_index=True,
        use_container_width=True,
    )


# ------------------------------------------------------------
# 15. METHODOLOGICAL LIMITATIONS
# ------------------------------------------------------------

st.divider()

st.subheader("Methodological Considerations")

with st.expander("Study Limitations", expanded=True):

    st.markdown(
        """
        **Ecological Fallacy**

        State-level associations cannot establish
        individual-level vaccination outcomes.

        **Confounding**

        Population composition, access to healthcare,
        policies, outbreak dynamics, and surveillance
        practices may influence observed patterns.

        **Missing Data**

        Missing years are excluded from the relevant
        analyses rather than treated as zero incidence.

        **Lag Structure**

        Calendar-year offsets must be preserved.
        Nonconsecutive observations cannot be
        treated as consecutive years.

        **Survey Comparability**

        NIS-Child vaccination estimates and state-level
        disease incidence may represent different
        underlying age groups and populations.

        **Statistical Uncertainty**

        Small samples can generate unstable estimates.
        Pearson correlations and p-values should
        be considered with sample sizes.

        **Causation**

        These observational analyses do not demonstrate
        that changes in vaccination coverage caused
        changes in disease incidence.
        """
    )

st.caption(
    "BIOT 670I Capstone | Group 1 | "
    "Exploratory Ecological Analysis"
)
