import streamlit as st
import time

# Track login state in session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function for login validation
def validate_login(username, password):
    # Check if the credentials are correct
    if username == "admin" and password == "admin":  # Example credentials
        st.session_state.logged_in = True
        return True
    return False

# Main content function
def LiveBusMain():
    if st.session_state.logged_in:
        st.title("Live Bus Passengers")
        
        # Fetch BusPass data to display RFID options
        col_names, rows = fetch_data_from_buspass()
        
        if col_names and rows:
            # Display the data from BusPass table
            st.subheader("Current Passengers from Bus")
            buspass_df = [dict(zip(col_names, row)) for row in rows]
            st.table(buspass_df)
        
            # Create a list of RFID numbers from BusPass table
            rfid_numbers = [row[2] for row in rows]  # Assuming RFID is the third column (index 2)
            selected_rfid = st.selectbox("Select RFID No", rfid_numbers)
            fetch_photo_by_rfid(selected_rfid)
            
            if selected_rfid:
                # Fetch and display BusPassangers data for the selected RFID
                st.subheader(f"Data for RFID {selected_rfid}")
                col_names, buspassangers_rows, photo_data = fetch_data_from_buspassangers(selected_rfid)
        
                if buspassangers_rows:
                    buspassangers_df = [dict(zip(col_names, row)) for row in buspassangers_rows]
                    st.table(buspassangers_df)
                    
                
                    if photo_data:
                        try:
                            image = Image.open(io.BytesIO(photo_data))
                            image.verify()  # Check image integrity
                            image = Image.open(io.BytesIO(photo_data))  # Reopen after verify
                            st.image(image, caption="Passenger Photo", use_container_width=True)
                        except UnidentifiedImageError:
                            st.error("The image format is not recognized or is corrupted.")
                        except OSError:
                            st.error("The image file is incomplete or unreadable.")
                        except Exception as e:
                            st.error(f"Unexpected error while loading image: {str(e)}")
                    else:
                        st.warning("No image data available for this passenger.")
                
                # Refresh the app every 3 seconds without logging out
                time.sleep(3)
                st.experimental_rerun()

    else:
        st.write("Please log in from the sidebar to access the system.")

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
    if validate_login(username, password):  # Validate credentials
        st.sidebar.success(f"Welcome, {username}!")

        # Tabs after login
        tabs = st.tabs(["Recharge Card", "Check Live Status", "Check History", "Register Passenger"])

        # 1st Tab: Recharge Card
        with tabs[0]:
            st.subheader("Recharge Card")
            st.write("Redirecting to Recharge Card...")
            st.markdown('<a href="https://busrfrecharge-aqupzmfkxy3xbvpoq7hybm.streamlit.app/" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)

        # 2nd Tab: Check Live Status
        with tabs[1]:
            st.subheader("Live Bus Status")
            LiveBusMain()

        # 3rd Tab: Check History
        with tabs[2]:
            st.subheader("Check Travel History")
            st.write("Redirecting to Recharge Card...")
            st.markdown('<a href="https://bushistory-3ujwysudfgvcpbfdnhexah.streamlit.app/" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)

        # 4th Tab: Register Passenger
        with tabs[3]:
            st.subheader("Regester Card")
            st.write("Redirecting to Reguster Passnger Card...")
            st.markdown('<a href="https://regesterpassanger-9iu2puyfxmh9hts5azkwdv.streamlit.app/" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)
    else:
        st.sidebar.error("Invalid credentials. Please try again.")
