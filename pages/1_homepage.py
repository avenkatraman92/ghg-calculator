import streamlit as st

# Set the page config (Optional)
st.set_page_config(page_title="GHG Emissions Calculator", page_icon="🌍")

# Homepage
def homepage():
    # Display the homepage title and message
    st.title("Welcome to the GHG Emissions Calculator")
    st.write("This tool helps you calculate GHG emissions for Scope 1 & 2 and Scope 3. Select which page you'd like to visit below.")
    
    # Dropdown to select the page
    page = st.selectbox("Select a page", ["Scope 1 & 2", "Scope 3"])

    # Button to go to the selected page
    if st.button("Go"):
        if page == "Scope 1 & 2":
            # Redirect to Scope 1 & 2 page
            st.experimental_set_query_params(page="scope1_2")
            st.write(f"Redirecting to Scope 1 & 2 page...")
            st.experimental_rerun()  # To reload the page if needed
        elif page == "Scope 3":
            # Redirect to Scope 3 page
            st.experimental_set_query_params(page="scope3")
            st.write(f"Redirecting to Scope 3 page...")
            st.experimental_rerun()  # To reload the page if needed

# Call homepage function to run the app
homepage()

# Check the query parameter and display the appropriate page (this is handled on the homepage)
query_params = st.experimental_get_query_params()
if query_params.get("page") == ["scope1_2"]:
    # Redirect to Scope 1 & 2 page (use your pre-existing logic for this page)
    st.experimental_set_query_params(page="scope1_2")
    st.experimental_rerun()  # Navigate to the scope1_2 page URL directly
elif query_params.get("page") == ["scope3"]:
    # Redirect to Scope 3 page (use your pre-existing logic for this page)
    st.experimental_set_query_params(page="scope3")
    st.experimental_rerun()  # Navigate to the scope3 page URL directly
