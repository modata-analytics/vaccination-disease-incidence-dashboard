"""BIOT 670I Group 1 | Descriptive MMP master data explorer.

This page describes measles, mumps, and pertussis vaccination coverage and
incidence across California and Florida. It does not calculate lag correlations.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cases_coverage_ms.csv"
STATE_CODES = {"California": "CA", "Florida": "FL"}
DISEASES = {"Measles": "measles", "Mumps": "mumps", "Pertussis": "pertussis"}
COLORS = {"California": "#71BCF4", "Florida": "#30BDA5"}


@st.cache_data
def load_master():
    df = pd.read_csv(DATA_PATH)
    required = {"year", "state"} | {
        f"{disease}_{field}"
        for disease in DISEASES.values()
        for field in ("coverage_pct", "cases_per_100k", "cases")
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns from master dataset: {sorted(missing)}")

    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if df["year"].isna().any():
        raise ValueError("Master dataset contains missing or invalid years.")
    if (df["year"] % 1 != 0).any():
        raise ValueError("Master dataset contains non-integer years.")
    df["year"] = df["year"].astype(int)
    for column in required - {"year", "state"}:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[df["state"].isin(STATE_CODES.values())].copy()
    if df.empty:
        raise ValueError("No California or Florida records found.")
    if df.duplicated(["state", "year"]).any():
        raise ValueError("Duplicate state/year records in master dataset.")
    return df.sort_values(["state", "year"])


def trend_chart(frame, column, ylabel, selected_states):
    fig = go.Figure()
    first_year = int(frame["year"].min())
    last_year = int(frame["year"].max())
    full_years = pd.DataFrame({"year": range(first_year, last_year + 1)})

    for state_name in selected_states:
        state_code = STATE_CODES[state_name]
        state_data = frame.loc[frame["state"] == state_code, ["year", column]]
        series = full_years.merge(state_data, on="year", how="left")
        fig.add_trace(go.Scatter(
            x=series["year"],
            y=series[column],
            mode="lines+markers",
            connectgaps=False,
            name=state_name,
            line={"color": COLORS[state_name], "width": 2},
            marker={"size": 7},
            hovertemplate="Year: %{x}<br>Value: %{y:.3f}<extra>%{fullData.name}</extra>",
        ))

    # Use a tight, data-driven scale for coverage so annual differences are visible.
    # Preserve a zero-based scale for incidence counts/rates.
    if column.endswith("_coverage_pct"):
        observed = pd.to_numeric(frame[column], errors="coerce").dropna()
        if not observed.empty:
            low, high = float(observed.min()), float(observed.max())
            padding = max((high - low) * 0.15, 0.5)
            yaxis_range = [max(0.0, low - padding), min(100.0, high + padding)]
            if yaxis_range[0] >= yaxis_range[1]:
                yaxis_range = [max(0.0, low - 0.5), min(100.0, high + 0.5)]
        else:
            yaxis_range = None
    else:
        yaxis_range = None

    fig.update_layout(
        template="plotly_dark",
        title_text="",  # Avoids the unwanted 'undefined' heading
        showlegend=len(selected_states) > 1,
        legend={"orientation": "h", "y": 1.06, "x": 0},
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 55, "r": 25, "t": 35, "b": 105},
        hovermode="closest",
        xaxis={
            "title_text": "Year",
            "type": "linear",
            "tickmode": "linear",
            "tick0": first_year,
            "dtick": 1,
            "tickangle": 60,
            "tickfont": {"size": 10},
            "range": [first_year - 0.5, last_year + 0.5],
        },
        yaxis={
            "title_text": ylabel,
            "showgrid": True,
            "gridcolor": "rgba(150,150,150,0.20)",
            "range": yaxis_range,
            "rangemode": "tozero" if yaxis_range is None else "normal",
        },
    )
    return fig


st.title("MMP Master Explorer")
st.caption("BIOT 670I Capstone | Group 1 | Descriptive state-level analysis, 1995–2017")
st.write(
    "Explore measles, mumps, and pertussis vaccination coverage and disease "
    "incidence in California and Florida. This page presents descriptive data "
    "and does not calculate time-lagged correlations."
)

try:
    master = load_master()
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error("Unable to load the master dataset at app/data/cases_coverage_ms.csv.")
    st.exception(exc)
    st.stop()

chosen_disease = st.selectbox("Select disease", list(DISEASES), key="mmp_disease")
selected_states = st.multiselect(
    "Select states", list(STATE_CODES), default=list(STATE_CODES), key="mmp_states"
)
if not selected_states:
    st.info("Select at least one state to display data.")
    st.stop()

disease = DISEASES[chosen_disease]
coverage_col = f"{disease}_coverage_pct"
incidence_col = f"{disease}_cases_per_100k"
cases_col = f"{disease}_cases"
frame = master[master["state"].isin(STATE_CODES[name] for name in selected_states)].copy()
complete = frame[coverage_col].notna() & frame[incidence_col].notna()

col1, col2, col3 = st.columns(3)
col1.metric("State-year records", len(frame))
col2.metric("Complete measurement pairs", int(complete.sum()))
col3.metric("Incomplete measurement pairs", int((~complete).sum()))
st.caption(
    "Complete pairs contain both vaccination coverage and incidence for a "
    "state and calendar year; missing values are not interpreted as zero."
)

st.subheader(f"{chosen_disease} Vaccination Coverage")
st.plotly_chart(
    trend_chart(frame, coverage_col, "Vaccination Coverage (%)", selected_states),
    use_container_width=True,
    key="mmp_coverage_chart",
)

st.subheader(f"{chosen_disease} Incidence")
st.plotly_chart(
    trend_chart(frame, incidence_col, "Cases per 100,000", selected_states),
    use_container_width=True,
    key="mmp_incidence_chart",
)

st.subheader("Data Completeness by State")
summary_rows = []
for name in selected_states:
    state_rows = frame.loc[frame["state"] == STATE_CODES[name]].sort_values("year")
    valid_pairs = state_rows[coverage_col].notna() & state_rows[incidence_col].notna()
    incomplete_years = state_rows.loc[~valid_pairs, "year"].tolist()
    summary_rows.append({
        "State": name,
        "Years represented": len(state_rows),
        "Coverage available": int(state_rows[coverage_col].notna().sum()),
        "Incidence available": int(state_rows[incidence_col].notna().sum()),
        "Complete pairs": int(valid_pairs.sum()),
        "Completeness (%)": round(100 * valid_pairs.mean(), 1) if len(state_rows) else 0.0,
        "Incomplete years": ", ".join(map(str, incomplete_years)) or "None",
    })
st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

with st.expander("View underlying observations"):
    st.dataframe(
        frame[["year", "state", coverage_col, incidence_col, cases_col]].sort_values(["state", "year"]),
        use_container_width=True,
        hide_index=True,
    )

with st.expander("Methods and interpretation", expanded=True):
    st.markdown("""
- **Ecological scope:** State-level relationships do not establish individual-level vaccine effects.
- **Different populations:** NIS-Child coverage estimates and state surveillance incidence may cover different age groups.
- **Missing observations:** Unavailable incidence remains missing, not zero; the charts do not bridge missing years.
- **Descriptive purpose:** This explorer does not compute causal or lagged associations. See **State Case Studies** for the reported measles lag results.
- **Data provenance:** The master CSV integrates surveillance, vaccination coverage, and population data. See the team's methodology for exact source transformations and weighting.
- **Comparisons:** Similar patterns across the plotted series are not proof of causation and may reflect confounding and surveillance differences.
""")

st.caption(
    "BIOT 670I Capstone | Group 1 | Exploratory Ecological Analysis"
)

st.caption(
    "AI-assisted code generation was used to support data processing "
    "and visualization, but all interpretations and conclusions "
    "were made by the research team."
)

