import streamlit as st

# Set the title of the application
st.set_page_config(page_title="RFID-Based Bus Ticket System", layout="wide")

# Sidebar for the login page
st.sidebar.title("RFID-Based Bus Ticket System")
st.sidebar.write("Please log in to continue.")

# Login Form in Sidebar
with st.sidebar.form(key="login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.form_submit_button("Login")

# Main Page
if login_button:
    if username == "admin" and password == "admin":  # Example credentials
        st.sidebar.success(f"Welcome, {username}!")

        st.title("RFID-Based Bus Ticket System Dashboard")
        st.write("Choose an action below:")

        # Buttons for different actions
        if st.button("Recharge Card"):
            st.subheader("Recharge Card")
            st.write("Redirecting to Google...")
            st.markdown('<a href="https://www.google.com" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)
else:
    st.write("Please log in from the sidebar to access the system.")
