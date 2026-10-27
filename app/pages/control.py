import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Project Tycho Level 1 Control", page_icon="⚙️")

st.markdown("Project Tycho Measles Control: 1931 to 1992")
st.sidebar.header("Project Tycho Measles Control")
st.write(
    """
    ### Positive Control

    Reproduce the well-established collapse in **measles incidence after the 1963 vaccine introduction** using Project Tycho data.

    Article: https://academic.oup.com/ofid/article/5/7/ofy137/5039595
    Tycho Dataset Version 1.0.0: https://zenodo.org/records/12608992

    **Table 1. Observed and Prevented Measles Cases, Deaths, and Related Costs in the United States, With 80% Uncertainty Range**

    | | Prevaccination (1931–1963) | Introduction (1964–1970) | 1-dose Vaccine (1971–1989) |
    |---|---|---|---|
    | **Cases, millions** | | | |
    | Observed| 16.81 | 1.14 | 0.39 |

    If the analysis pipeline cannot recover this established historical pattern, it suggests a problem with the data processing or analysis.
    """
)

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data" / "tycho_measles_control.csv")
def compare_control_measles_dates(df):
    columns = [
    "Period",
    "Years",
    "Our Results",
    "Paper",
    "Difference",
    "% Difference"
    ]

    full_df = pd.DataFrame(columns=columns)

    prevaccination = df[(df['year'] >= 1931) & (df['year'] <= 1963)]
    prevaccination_cases = round(prevaccination['cases'].sum(), 2)

    introduction = df[(df['year'] >= 1964) & (df['year'] <= 1970)]
    introduction_cases = round(introduction['cases'].sum(), 2)

    one_dose_vaccine = df[(df['year'] >= 1971) & (df['year'] <= 1989)]
    one_dose_vaccine_cases = round(one_dose_vaccine['cases'].sum(), 2)

    prevaccination_control_cases = 16810000
    introduction_control_cases = 1140000
    one_dose_vaccine_control_case = 390000

    prevaccination_diff = abs(prevaccination_cases - prevaccination_control_cases)
    introduction_diff = abs(introduction_cases - introduction_control_cases)
    one_dose_vaccine_diff = abs(one_dose_vaccine_cases - one_dose_vaccine_control_case)

    prevaccination_diff_per = round(prevaccination_diff / prevaccination_control_cases * 100, 2)
    introduction_diff_per = round(introduction_diff / introduction_control_cases * 100, 2)
    one_dose_vaccine_diff_per = round(one_dose_vaccine_diff / one_dose_vaccine_control_case * 100, 2)

    full_df.loc[len(full_df)] = pd.Series(
        ["Prevaccination", "1931–1963", prevaccination_cases, prevaccination_control_cases, 
            prevaccination_diff, prevaccination_diff_per],
        index=columns
    )

    full_df.loc[len(full_df)] = pd.Series(
        ["Introduction", "1964–1970", introduction_cases, introduction_control_cases, 
            introduction_diff, introduction_diff_per],
        index=columns
    )

    full_df.loc[len(full_df)] = pd.Series(
        ["1-dose vaccine", "1971–1989", one_dose_vaccine_cases, one_dose_vaccine_control_case, 
            one_dose_vaccine_diff, one_dose_vaccine_diff_per],
        index=columns
    )

    return full_df

compared_df = compare_control_measles_dates(df)


def table_control_measles_compare(df):
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    align="left"
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],
                    align="left"
                )
            )
        ]
    )
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, width="stretch")


table_control_measles_compare(compared_df)

def graph_comparisons_measles_control(df):

    fig = px.line(
        df,
        x="Period",
        y=["Our Results", "Paper"],
        markers=True,
        title="Comparison of Our Results with the Paper"
    )

    fig.update_layout(
        xaxis_title="Vaccination Period",
        yaxis_title="Measles Cases",
        legend_title="Source"
    )

    st.plotly_chart(fig, width="stretch")

graph_comparisons_measles_control(compared_df)



st.write(
    """
    ### Placebo Check

    Correlate **vaccination coverage** with a **non-vaccine-preventable health outcome**.

    A strong association with an unrelated outcome may indicate **confounding, spurious correlation, or problems in the analysis pipeline**.
    """
)

