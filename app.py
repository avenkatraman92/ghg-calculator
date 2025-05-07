import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

# Load emission factors
with open("emission_factors.json", "r") as f:
    factors = json.load(f)

st.title("GHG Emissions Calculator (Scope 1 & 2)")

# Display guidance paragraph
st.markdown("""
### What This App Does:
This tool helps calculate the **Greenhouse Gas (GHG)** emissions based on Scope 1 and Scope 2 activities. 
Scope 1 covers direct emissions from owned or controlled sources, while Scope 2 accounts for indirect emissions from the consumption of purchased electricity.

### How to Use:
1. **Select the Emission Scope** (Scope 1 or Scope 2).
2. **Choose a category** (e.g., Stationary Combustion, Mobile Combustion for Scope 1).
3. **Select an Activity Type** (e.g., Diesel, Petrol).
4. **Enter the quantity** of fuel or energy consumed.
5. **Click "Add Activity"** to calculate and add the entry to your results.
6. **Delete any incorrect entries** by clicking the "Delete" button.
""")

# Initialize session state to hold activities
if 'activities' not in st.session_state:
    st.session_state.activities = []

# Function to add an activity to the session state
def add_activity(scope, category, activity_type, quantity):
    if scope == "scope_1":
        emissions = quantity * factors['scope_1'][category][activity_type] if quantity > 0 else 0
    elif scope == "scope_2":
        emissions = quantity * factors['scope_2'][activity_type] if quantity > 0 else 0
    
    st.session_state.activities.append({
        'scope': scope,
        'category': category,
        'activity_type': activity_type,
        'quantity': quantity,
        'emissions': emissions
    })

# Function to delete an activity from session state
def delete_activity(index):
    del st.session_state.activities[index]

# Select scope
scope = st.selectbox("Select Emission Scope", list(factors.keys()))

if scope == "scope_1":
    # Choose category: Stationary Combustion, Mobile Combustion, Fugitive Emissions
    category = st.selectbox("Select Category", list(factors["scope_1"].keys()))

    # Choose specific fuel/refrigerant
    activity_type = st.selectbox("Select Activity Type", list(factors["scope_1"][category].keys()))

    # Enter quantity
    unit = activity_type.split('(')[-1].strip(')')
    quantity = st.number_input(f"Enter quantity ({unit})", min_value=0.0)

    if st.button('Add Activity'):
        add_activity(scope, category, activity_type, quantity)
        st.success(f"Activity added! {activity_type} with quantity {quantity} {unit}.")

elif scope == "scope_2":
    activity_type = st.selectbox("Select Activity Type", list(factors["scope_2"].keys()))
    unit = activity_type.split('(')[-1].strip(')')
    quantity = st.number_input(f"Enter quantity ({unit})", min_value=0.0)
    
    # Renewable energy input
    renewable_energy = st.number_input("Enter renewable energy (kWh) to subtract from Scope 2 emissions", min_value=0.0)

    if st.button('Add Activity'):
        add_activity(scope, "", activity_type, quantity)
        # Subtract renewable energy emissions
        renewable_emissions = renewable_energy * factors["scope_2"].get("Electricity (kWh)", 0)
        st.session_state.activities[-1]['emissions'] -= renewable_emissions
        st.success(f"Activity added! {activity_type} with quantity {quantity} {unit}.")

# Show summary of activities entered
st.subheader("Summary of Activities")
for idx, activity in enumerate(st.session_state.activities):
    cols = st.columns([3, 3, 3, 2, 3, 1])
    cols[0].write(activity['scope'])
    cols[1].write(activity.get('category', '-'))
    cols[2].write(activity['activity_type'])
    cols[3].write(activity['quantity'])
    cols[4].write(f"{activity['emissions']:.2f} kg CO₂e")

    # Generate unique key for the delete button based on activity's scope, type, and category
    unique_key = f"delete_{idx}_{activity['scope']}_{activity.get('category', '')}_{activity['activity_type']}"
    
    if cols[5].button("🗑", key=unique_key):
        delete_activity(idx)
        st.experimental_rerun()  # Refresh the UI after deletion

# Calculate cumulative emissions for Scope 1 and Scope 2
scope_1_emissions = sum([activity['emissions'] for activity in st.session_state.activities if activity['scope'] == 'scope_1'])
scope_2_emissions = sum([activity['emissions'] for activity in st.session_state.activities if activity['scope'] == 'scope_2'])

# Display cumulative emissions
st.subheader("Cumulative Emissions")
st.table({
    "Scope 1 Emissions (kg CO₂e)": [f"{scope_1_emissions:.2f}"],
    "Scope 2 Emissions (kg CO₂e)": [f"{scope_2_emissions:.2f}"],
    "Total Emissions (kg CO₂e)": [f"{scope_1_emissions + scope_2_emissions:.2f}"]
})

# Scope 1 Pie Chart
scope_1_data = [a for a in st.session_state.activities if a['scope'] == 'scope_1']
if scope_1_data:
    scope_1_emissions = sum(a['emissions'] for a in scope_1_data)
    labels = [f"{a['activity_type']} ({a.get('category', '-')})" for a in scope_1_data]
    sizes = [a['emissions'] for a in scope_1_data]

    st.subheader("Scope 1 Emissions Breakdown")
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# Scope 2 Bar Chart
scope_2_data = [a for a in st.session_state.activities if a['scope'] == 'scope_2']
if scope_2_data:
    scope_2_emissions = sum(a['emissions'] for a in scope_2_data)
    st.subheader("Scope 2 Emissions: Grid vs Renewable")
    re = sum([a['quantity'] for a in scope_2_data if "renewable" in a['activity_type'].lower()])
    grid = sum([a['quantity'] for a in scope_2_data if "renewable" not in a['activity_type'].lower()])
    
    fig2, ax2 = plt.subplots()
    ax2.bar(["Grid Electricity", "Renewable Energy"], [grid, re], color=["green", "orange"])
    ax2.set_ylabel("kWh")
    st.pyplot(fig2)

# Combined Pie Chart
if scope_1_emissions + scope_2_emissions > 0:
    st.subheader("Total Emissions by Scope")
    fig3, ax3 = plt.subplots()
    ax3.pie([scope_1_emissions, scope_2_emissions],
            labels=["Scope 1", "Scope 2"],
            autopct='%1.1f%%',
            colors=["#ff9999", "#66b3ff"],
            startangle=140)
    ax3.axis('equal')
    st.pyplot(fig3)
