import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Placebo: Cancer Deaths & Vaccine Coverage", page_icon="✅")

st.markdown("Placebo: Cancer Deaths & Vaccine Coverage: 1995 to 2017")
st.sidebar.header("Placebo: Cancer Deaths & Vaccine Coverage")
st.write(
    """
    ### Cancer Deaths & Vaccine Coverage

    This placebo check tests whether vaccination coverage is associated with an unrelated outcome: cancer deaths. 
    Since vaccination coverage is not expected to affect overall cancer mortality, we should not observe a consistent relationship between the two. 
    A lack of association provides support that relationships observed for vaccine-preventable diseases are not simply due to general state or year trends.
    """
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

vacc_coverage_df = pd.read_csv(DATA_DIR / "nis_vacc_coverage.csv")
cancer_deaths_df = pd.read_csv(DATA_DIR / "cancer_deaths.csv")
panel_df = pd.merge(cancer_deaths_df, vacc_coverage_df, on=['year', 'state'])


def graph_cancer_vaccination_coverage(df, state):

    # Filter to selected state
    state_df = (
        df[df["state"] == state]
        .sort_values("year")
    )

    fig = go.Figure()

    # Cancer deaths
    fig.add_trace(
        go.Bar(
            x=state_df["year"],
            y=state_df["cancer_death_count"],
            name="Cancer deaths",
            opacity=0.65,
            hovertemplate=(
                "Year: %{x}<br>"
                "Cancer deaths: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    # Measles coverage
    fig.add_trace(
        go.Scatter(
            x=state_df["year"],
            y=state_df["measles_coverage_pct"],
            name="Measles coverage",
            mode="lines+markers",
            yaxis="y2",
            hovertemplate=(
                "Year: %{x}<br>"
                "Measles coverage: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    # Mumps coverage
    fig.add_trace(
        go.Scatter(
            x=state_df["year"],
            y=state_df["mumps_coverage_pct"],
            name="Mumps coverage",
            mode="lines+markers",
            yaxis="y2",
            hovertemplate=(
                "Year: %{x}<br>"
                "Mumps coverage: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    # Pertussis coverage
    fig.add_trace(
        go.Scatter(
            x=state_df["year"],
            y=state_df["pertussis_coverage_pct"],
            name="Pertussis coverage",
            mode="lines+markers",
            yaxis="y2",
            hovertemplate=(
                "Year: %{x}<br>"
                "Pertussis coverage: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=f"Annual Vaccination Coverage and Cancer Deaths In {state}",

        xaxis=dict(
            title="Year",
            dtick=1
        ),

        yaxis=dict(
            title="Cancer Death Count"
        ),

        yaxis2=dict(
            title="Vaccination Coverage (%)",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),

        template="plotly_white",
        height=600,
        hovermode="x unified",
        legend_title="Measure",
        bargap=0.20
    )

    return fig


selected_state = st.selectbox(
    "Select a state",
    sorted(panel_df["state"].dropna().unique())
)

filtered_df = panel_df[panel_df["state"] == selected_state]

fig = graph_cancer_vaccination_coverage(filtered_df, selected_state)
st.plotly_chart(fig, width="stretch")