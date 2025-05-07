import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="Scope 3 Emissions", layout="wide")

st.title("Scope 3 Emissions Calculator")

# Load emission factors from scope3_emission_factors.json
with open("scope3_emission_factors.json", "r") as file:
    emission_factors = json.load(file)

# Session state to store line items
if "scope3_items" not in st.session_state:
    st.session_state.scope3_items = []

# Add line items for each subcategory within each Scope 3 category
for category, subcategories in emission_factors.items():
    st.subheader(category)

    for subcategory, emission_factor in subcategories.items():
        # Form to add new line item for each subcategory
        with st.form(f"{category}_{subcategory}_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1:
                quantity = st.number_input(f"Quantity for {subcategory}", min_value=0.0, step=0.1)
            with col2:
                unit = st.text_input(f"Unit for {subcategory} (e.g. kg, km, ₹)")

            submitted = st.form_submit_button(f"Add {subcategory} Entry")
            if submitted and quantity:
                emissions = quantity * emission_factor
                st.session_state.scope3_items.append({
                    "Category": category,
                    "Subcategory": subcategory,
                    "Quantity": quantity,
                    "Unit": unit,
                    "Emission Factor": emission_factor,
                    "Emissions (kg CO₂e)": emissions
                })

# Display line items in a table with delete option
st.subheader("Scope 3 Emissions Line Items")
if st.session_state.scope3_items:
    df = pd.DataFrame(st.session_state.scope3_items)
    for idx, row in df.iterrows():
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"**{row['Subcategory']}** — {row['Quantity']} {row['Unit']} × {row['Emission Factor']} EF = **{row['Emissions (kg CO₂e)']:.2f} kg CO₂e**")
        with col2:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.scope3_items.pop(idx)
                st.experimental_rerun()

    total_emissions = df["Emissions (kg CO₂e)"].sum()
    st.success(f"**Total Scope 3 Emissions: {total_emissions:.2f} kg CO₂e**")

    # Pie chart of emissions by category
    st.subheader("Emission Contribution by Category")
    pie_data = df.groupby("Category")["Emissions (kg CO₂e)"].sum()
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.info("No line items added yet.")
