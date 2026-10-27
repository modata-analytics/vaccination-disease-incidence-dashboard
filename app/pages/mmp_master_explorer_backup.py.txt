"""BIOT 670I — descriptive MMP master-data explorer for California and Florida.

Save this as app/pages/mmp_master_explorer.py and register it in app/app.py.
This page does not compute or present lag correlations.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / 'data' / 'cases_coverage_ms.csv'
STATE_CODES = {'California': 'CA', 'Florida': 'FL'}
DISEASES = {'Measles': 'measles', 'Mumps': 'mumps', 'Pertussis': 'pertussis'}
COLOR = {'California': '#71BCF4', 'Florida': '#30BDA5'}

@st.cache_data
def load_master():
    df = pd.read_csv(DATA)
    required = {'year', 'state'} | {
        f'{d}_{field}' for d in DISEASES.values()
        for field in ('coverage_pct', 'cases_per_100k', 'cases')
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f'Missing master-data columns: {sorted(missing)}')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    for column in required - {'state', 'year'}:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df[df['state'].isin(STATE_CODES.values())].dropna(subset=['year']).copy()
    df['year'] = df['year'].astype(int)
    if df.duplicated(['state', 'year']).any():
        raise ValueError('Master file contains duplicate state-year records.')
    return df


def plot_trend(frame, column, ylabel, chart_type='line'):
    fig = go.Figure()
    for name in STATE_CODES:
        state_df = frame[frame['state'] == STATE_CODES[name]].sort_values('year')
        if chart_type == 'bar':
            fig.add_trace(go.Bar(
                x=state_df['year'], y=state_df[column], name=name,
                marker_color=COLOR[name], opacity=.80,
                hovertemplate='Year: %{x}<br>Value: %{y:.3f}<extra></extra>'
            ))
        else:
            # Include NaN entries on a full-year grid so gaps break the line.
            years = pd.DataFrame({'year': range(int(frame.year.min()), int(frame.year.max()) + 1)})
            series = years.merge(state_df[['year', column]], on='year', how='left')
            fig.add_trace(go.Scatter(
                x=series['year'], y=series[column], mode='lines+markers',
                connectgaps=False, name=name, line={'color': COLOR[name], 'width': 2},
                marker={'size': 6},
                hovertemplate='Year: %{x}<br>Value: %{y:.3f}<extra></extra>'
            ))
    
    fig.update_layout(
        template="plotly_dark",
        title_text="",
        showlegend=False,
        height=410,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=20, t=20, b=100),
        xaxis=dict(
            title_text="Year",
            type="linear",
            tickmode="linear",
            tick0=1995,
            dtick=1,
            tickangle=60,
            range=[
                frame["year"].min() - 0.5,
                frame["year"].max() + 0.5
            ]
        ),
        yaxis=dict(
            title_text=ylabel
        ),
        barmode="group"
    )

    fig.update_traces(showlegend=False)

    return fig

st.title('MMP Explorer — Master Dataset (UPDATED)')
st.caption('BIOT 670I · Descriptive state-level analysis · 1995–2017')
st.write('Explore measles, mumps, and pertussis in California and Florida. '
         'This page describes reported observations; it does not calculate lagged associations.')

try:
    master = load_master()
except (OSError, ValueError, pd.errors.ParserError) as error:
    st.error('Unable to load the master CSV from app/data/cases_coverage_ms.csv.')
    st.exception(error)
    st.stop()

chosen = st.selectbox('Select disease', list(DISEASES), key='mmp_disease')
d = DISEASES[chosen]
coverage_col = f'{d}_coverage_pct'
incidence_col = f'{d}_cases_per_100k'
cases_col = f'{d}_cases'
selected_states = st.multiselect('Select states', list(STATE_CODES), default=list(STATE_CODES), key='mmp_states')
if not selected_states:
    st.info('Select at least one state to display data.')
    st.stop()
frame = master[master['state'].isin([STATE_CODES[s] for s in selected_states])].copy()
# Keep the ordering of the original dataset but do not impute missing outcomes.
years = sorted(frame.year.unique().tolist())
valid = frame[frame[coverage_col].notna() & frame[incidence_col].notna()]
c1, c2, c3 = st.columns(3)
c1.metric('State-year rows', f'{len(frame)}')
c2.metric('Complete measurement pairs', f'{len(valid)}')
c3.metric('Incomplete measurement pairs', f'{len(frame)-len(valid)}')

# Explicit labels avoid the Plotly 'undefined' legend-title issue.
state_key = '   |   '.join(
    f':blue[**California**]' if state == 'California' else f':green[**Florida**]'
    for state in selected_states
)
st.caption(f'States shown: {state_key}')

st.subheader(f'{chosen} Vaccination Coverage')
st.plotly_chart(plot_trend(frame, coverage_col, 'Vaccination Coverage (%)'), use_container_width=True, key='mmp_coverage_chart')
st.subheader(f'{chosen} Incidence')
st.plotly_chart(plot_trend(frame, incidence_col, 'Cases per 100,000'), use_container_width=True, key='mmp_incidence_chart')

st.subheader('Data Completeness by State')
rows = []
for name in selected_states:
    s = frame[frame['state'] == STATE_CODES[name]].sort_values('year')
    missing_years = s.loc[s[coverage_col].isna() | s[incidence_col].isna(), 'year'].tolist()
    rows.append({'State': name, 'Years in master': len(s),
                 'Coverage available': int(s[coverage_col].notna().sum()),
                 'Incidence available': int(s[incidence_col].notna().sum()),
                 'Both available': int((s[coverage_col].notna() & s[incidence_col].notna()).sum()),
                 'Missing either (years)': ', '.join(map(str, missing_years)) or 'None'})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
with st.expander('View underlying observations'):
    st.dataframe(frame[['year', 'state', coverage_col, incidence_col, cases_col]].sort_values(['state','year']),
                 use_container_width=True, hide_index=True)
with st.expander('Methods and interpretation', expanded=True):
    st.markdown('''
- **Ecological scope:** State-level relationships do not establish individual vaccine effects.
- **Different populations:** NIS-Child coverage estimates and state surveillance incidence may represent different age groups.
- **Missing observations:** Blank incidence values remain missing, not zero. Lines break at missing years.
- **Descriptive analysis:** This page makes no causal or time-lagged claims. For reported measles lag coefficients, use the existing State Case Studies page.
- **Data provenance:** The master CSV combines Project Tycho, supplemental disease reporting, NIS-Child coverage, and population information; consult the team methodology for exact transformations and survey weighting.
''')
