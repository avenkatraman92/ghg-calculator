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
            # Redirect to the Scope 1 & 2 page (app)
            st.markdown(f'<a href="https://ghg-calculator-fp76akmc4rqvwnchqddvdk.streamlit.app/#scope-1-and-2-ghg-emissions" target="_self">Go to Scope 1 & 2 Page</a>', unsafe_allow_html=True)
        elif page == "Scope 3":
            # Redirect to the Scope 3 page
            st.markdown(f'<a href="https://ghg-calculator-fp76akmc4rqvwnchqddvdk.streamlit.app/scope3" target="_self">Go to Scope 3 Page</a>', unsafe_allow_html=True)

# Call homepage function to run the app
homepage()
