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
            st.write("Here you can recharge RFID cards. (Functionality not implemented yet.)")
            st.markdown('<a href="https://feedback-dtsqucs9rfckhzrzu648uq.streamlit.app/" target="_blank">Open Recharge Card Page</a>', unsafe_allow_html=True)

        if st.button("Check Traveled History"):
            st.subheader("Check Traveled History")
            st.write("Here you can check travel history. (Functionality not implemented yet.)")
            st.markdown('<a href="https://busrfrecharge-aqupzmfkxy3xbvpoq7hybm.streamlit.app/" target="_blank">Open Traveled History Page</a>', unsafe_allow_html=True)

        if st.button("View All Users"):
            st.subheader("View All Users")
            st.write("Here is a list of all users. (Functionality not implemented yet.)")
            st.markdown('<a href="https://livebus-itkuyksb6plr5pbzgxhop7.streamlit.app/" target="_blank">Open Users Page</a>', unsafe_allow_html=True)

        # New button to register a passenger
        if st.button("Register Passenger"):
            st.subheader("Register New Passenger")
            st.write("Here you can register a new passenger. (Functionality not implemented yet.)")
            st.markdown('<a href="https://regesterpassanger-9iu2puyfxmh9hts5azkwdv.streamlit.app/" target="_blank">Open Register Passenger Page</a>', unsafe_allow_html=True)

    else:
        st.sidebar.error("Invalid username or password. Please try again.")
else:
    st.write("Please log in from the sidebar to access the system.")
