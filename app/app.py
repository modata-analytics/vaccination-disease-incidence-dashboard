import streamlit as st

pages = {
    "Home": [
        st.Page(
            "pages/home.py",
            title="Home",
            icon="🏠",
            default=True
        )
    ],
    "Analysis": [
        st.Page(
            "pages/control.py",
            title="Control",
            icon="⚙️",
            url_path="control.py"
        ),
        st.Page(
            "pages/placebo.py",
            title="Placebo",
            icon="✅",
            url_path="placebo.py"
        ),
        st.Page(
            "pages/mmp_coverage_cases.py",
            title="MMP Coverage and Cases",
            icon="💉",
            url_path="mmp_coverage_cases.py"
        ),
        st.Page(
            "pages/mmp_coverage_cases_by_state.py",
            title="MMP Coverage and Cases Per State",
            icon="🇺🇸",
            url_path="mmp_coverage_cases_by_state.py"
        ),
        # st.Page(
        #     "pages/time_lagged_associations_by_state.py",
        #     title="Time Lagged Associations Per State",
        #     icon="⏳",
        #     url_path="time_lagged_associations_by_state.py"
        # ),
        st.Page(
            "pages/state_case_studies.py",
            title="State Case Studies",
            icon=":material/analytics:",
            url_path="state-case-studies"
        ),
        st.Page(
            "pages/references.py",
            title="References",
            icon=":material/menu_book:",
            url_path="references"
        ),
        st.Page(
            "pages/mmp_master_explorer.py",
            title="MMP Master Explorer",
            icon=":material/analytics:",
            url_path="mmp-master-explorer"
        ),
        st.Page(
            "pages/pertussis_sanity_check.py",
            title="Matthew Rada - Pertussis Sanity Check",
            icon=":material/person_search:",
            url_path="pertussis_sanity_check"
        ),
        st.Page(
            "pages/ca_fl_measles_lag_analysis.py",
            title="Kalkidan Perin - FL & CA Lag Phase Analysis",
            icon=":material/person_search:",
            url_path="ca_fl_measles_lag_analysis"
        ),

    ],
    "Notebooks": [
        st.Page(
            "pages/notebooks/control_notebook.py",
            title="control_notebook.py",
            icon="📄",
            url_path="control_notebook.py"
        ),
        st.Page(
            "pages/notebooks/mmp_cases_coverage_notebook.py",
            title="mmp_cases_coverage_notebook.py",
            icon="📄",
            url_path="mmp_cases_coverage_notebook.py"
        ),
        st.Page(
            "pages/notebooks/calculate_nis_coverage.py",
            title="calculate_nis_coverage.py",
            icon="📄",
            url_path="calculate_nis_coverage.py"
        ),
        st.Page(
            "pages/notebooks/analysis_engine_time_association.py",
            title="analysis_engine_time_association.py",
            icon="📄",
            url_path="analysis_engine_time_association.py"
        ),
        st.Page(
            "pages/notebooks/missing_years_cases.py",
            title="missing_years_cases.py",
            icon="📄",
            url_path="missing_years_cases.py"
        ),
        st.Page(
            "pages/notebooks/lag_phase_analysis.py",
            title="lag_phase_analysis.py",
            icon="📄",
            url_path="lag_phase_analysis.py"
        ),
    ]
}

page = st.navigation(pages)
page.run()

