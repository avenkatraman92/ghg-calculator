import streamlit as st
import json

st.title("Scope 3 Emissions Calculator")

st.markdown("""
Scope 3 emissions include all indirect emissions that occur in a company’s 
value chain.
""")

# Load JSON data
with open("scope3_emission_factors.json") as f:
    data = json.load(f)

# Select main category
category = st.selectbox("Choose a Scope 3 Category", list(data.keys()))

# Select sub-category
subcategory = st.selectbox("Select a sub-category", 
list(data[category].keys()))

# Input quantity
quantity = st.number_input("Enter activity data (e.g. km, kg, units)", 
min_value=0.0)

# Calculate emissions
emission_factor = data[category][subcategory]
emissions = quantity * emission_factor

# Output result
st.success(f"Estimated Scope 3 Emissions: {emissions:.2f} kg CO₂e")
st.caption(f"Emission factor used: {emission_factor} kg CO₂e per unit for 
{subcategory}")

