import streamlit as st
import json

# Set the page config (Optional)
st.set_page_config(page_title="Individual Emissions Calculator", page_icon="🌍")

# Sidebar title
st.sidebar.title("Individual Emissions")

# Load the emission factors from the JSON file
with open('individual_emission_factors.json') as f:
    emission_factors = json.load(f)

# Your existing code to display the individual emissions page
st.title("Individual Emissions Calculator")

# Session state to store line items
if "individual_items" not in st.session_state:
    st.session_state.individual_items = []

# 1. Transportation Module
st.subheader("1. Transportation Emissions")
with st.form("transportation_form", clear_on_submit=True):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        air_travel = st.number_input("Air travel (km)", min_value=0, step=1)
    with col2:
        train_travel = st.number_input("Train travel (km)", min_value=0, step=1)
    with col3:
        bus_travel = st.number_input("Bus travel (km)", min_value=0, step=1)
    with col4:
        car_travel = st.number_input("Car travel (km)", min_value=0, step=1)
    with col5:
        bike_travel = st.number_input("Bike travel (km)", min_value=0, step=1)

    submitted = st.form_submit_button("Add Transportation Emissions")
    if submitted:
        emissions = (
            air_travel * emission_factors["Transportation"]["Air travel"] +
            train_travel * emission_factors["Transportation"]["Train travel"] +
            bus_travel * emission_factors["Transportation"]["Bus"] +
            car_travel * emission_factors["Transportation"]["Car"] +
            bike_travel * emission_factors["Transportation"]["Bike"]
        )
        st.session_state.individual_items.append({
            "Category": "Transportation",
            "Emissions (kg CO₂e)": emissions
        })

# 2. Power Consumption Module
st.subheader("2. Power Consumption Emissions")
with st.form("power_consumption_form", clear_on_submit=True):
    electricity_bill = st.number_input("Total electricity bill (kWh per year)", min_value=0, step=1)

    submitted = st.form_submit_button("Add Power Consumption Emissions")
    if submitted:
        emissions = electricity_bill * emission_factors["Power Consumption"]["Electricity"]
        st.session_state.individual_items.append({
            "Category": "Power Consumption",
            "Emissions (kg CO₂e)": emissions
        })

# 3. Amazon/Flipkart Delivery Module
st.subheader("3. Amazon/Flipkart Delivery Emissions")
with st.form("delivery_form", clear_on_submit=True):
    packages_received = st.number_input("Number of packages received per month", min_value=0, step=1)

    submitted = st.form_submit_button("Add Delivery Emissions")
    if submitted:
        emissions = packages_received * 12 * emission_factors["Amazon/Flipkart Delivery"]["Package"]
        st.session_state.individual_items.append({
            "Category": "Amazon/Flipkart Delivery",
            "Emissions (kg CO₂e)": emissions
        })

# 4. Clothes Module
st.subheader("4. Clothes Emissions")
with st.form("clothes_form", clear_on_submit=True):
    topwear = st.number_input("Topwear items bought per month", min_value=0, step=1)
    bottomwear = st.number_input("Bottomwear items bought per month", min_value=0, step=1)
    outerwear = st.number_input("Outerwear items bought per month", min_value=0, step=1)

    submitted = st.form_submit_button("Add Clothes Emissions")
    if submitted:
        emissions = (
            topwear * emission_factors["Clothes"]["Topwear"] +
            bottomwear * emission_factors["Clothes"]["Bottomwear"] +
            outerwear * emission_factors["Clothes"]["Outerwear"]
        )
        st.session_state.individual_items.append({
            "Category": "Clothes",
            "Emissions (kg CO₂e)": emissions
        })

# 5. Food Module
st.subheader("5. Food Emissions")
with st.form("food_form", clear_on_submit=True):
    home_meals = st.number_input("Meals cooked at home per month", min_value=0, step=1)
    ordered_meals = st.number_input("Meals ordered (Swiggy/Zomato) per month", min_value=0, step=1)

    submitted = st.form_submit_button("Add Food Emissions")
    if submitted:
        emissions = (
            home_meals * emission_factors["Food"]["Home-cooked"] +
            ordered_meals * emission_factors["Food"]["Ordered"]
        )
        st.session_state.individual_items.append({
            "Category": "Food",
            "Emissions (kg CO₂e)": emissions
        })

# Display line items in a table
st.subheader("Individual Emissions Line Items")
if st.session_state.individual_items:
    for item in st.session_state.individual_items:
        st.markdown(f"**{item['Category']}**: {item['Emissions (kg CO₂e)']:.2f} kg CO₂e")

    total_emissions = sum([item["Emissions (kg CO₂e)"] for item in st.session_state.individual_items])
    st.success(f"**Total Individual Emissions: {total_emissions:.2f} kg CO₂e**")
else:
    st.info("No emissions data added yet.")
