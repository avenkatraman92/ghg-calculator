import streamlit as st

# Set the page config (Optional)
st.set_page_config(page_title="GHG Emissions Calculator", page_icon="🌍")

# Homepage
def homepage():
    # Display the homepage title and message
    st.title("Welcome to the GHG Emissions Calculator")
    st.write("This tool helps you calculate GHG emissions for Scope 1 & 2 
and Scope 3. Select which page you'd like to visit below.")
    
    # Dropdown to select the page
    page = st.selectbox("Select a page", ["Scope 1 & 2", "Scope 3"])

    # Button to go to the selected page
    if st.button("Go"):
        if page == "Scope 1 & 2":
            # Change the query parameter for Scope 1 & 2
            st.experimental_set_query_params(page="scope1_2")
        elif page == "Scope 3":
            # Change the query parameter for Scope 3
            st.experimental_set_query_params(page="scope3")

# Call homepage function to run the app
homepage()

# Check the query parameter and display the appropriate page
query_params = st.experimental_get_query_params()
