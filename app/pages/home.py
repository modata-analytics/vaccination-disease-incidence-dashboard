import streamlit as st

st.set_page_config(
    page_title="BIOT 670I Capstone Project - Group 1",
    page_icon="💉",
)

st.write("BIOT 670I Capstone Project - Group 1")

st.markdown(
    """
    This dashboard explores the relationship between **vaccination coverage**
    and the incidence of vaccine-preventable diseases across the United States
    over time.

    ### Diseases
    - **Measles**
    - **Pertussis**
    - **Mumps**

    ### What You Can Explore
    - Historical disease incidence by state and year
    - Changes in vaccination coverage over time
    - Geographic patterns using interactive maps
    - Associations between vaccination coverage and disease incidence
    - Changes within individual states over time

    ### Data Sources
    - **Project Tycho** — Historical U.S. notifiable disease incidence
    - **CDC NNDSS / WONDER** — Recent disease incidence
    - **CDC NIS** — Vaccination coverage estimates
    - **CDC SchoolVaxView** — Kindergarten vaccination coverage and exemption rates

    ### Important Considerations
    This is an **ecological analysis**. Associations observed at the state or
    population level should not be interpreted as evidence that vaccination
    coverage directly caused changes in disease incidence.

    Results should be considered alongside potential **confounding, reporting
    bias, missing data, reverse causation, and uncertainty**.

    ### Group Members
    - Bakry, Heba
    - Bukirwa, Gloria
    - Overly, Moira
    - Perin, Kalkidan
    - Rada, Matthew

    **👈 Use the sidebar to select a disease and explore the data.**
    """
)
