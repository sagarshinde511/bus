import streamlit as st
import mysql.connector
from mysql.connector import OperationalError, IntegrityError
import io
from PIL import Image


host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"
def fetch_data_from_buspassangers(rfid):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Fetch only specific columns + photo
        query = "SELECT Name, Gender, Age, RFID, Balance, Photo FROM BusPassangers WHERE RFID = %s"
        cursor.execute(query, (rfid,))
        rows = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]

        photo_data = None
        if rows:
            photo_data = rows[0][-1]  # 'Photo' is expected to be the last selected column

        cursor.close()
        conn.close()

        return col_names[:-1], [row[:-1] for row in rows], photo_data  # Exclude 'Photo' from main table
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None, None, None
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
        return None, None, None
def fetch_data_from_buspass(rfid=None):
    try:
        # Establishing connection to the database using mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Query to fetch all data from BusPass table or filter by RFID
        if rfid:
            query = f"SELECT * FROM BusPass WHERE RFID = '{rfid}'"
        else:
            query = "SELECT * FROM BusPass"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Fetching column names
        col_names = [desc[0] for desc in cursor.description]
        
        # Closing the connection
        cursor.close()
        conn.close()
        
        return col_names, rows
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None, None
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
        return None, None

# Function to fetch data from BusPassangers table based on RFID and retrieve photo

def LiveBusMain():
    # Streamlit app
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
    
        if selected_rfid:
            # Fetch and display BusPassangers data for the selected RFID
            st.subheader(f"Data for RFID {selected_rfid}")
            col_names, buspassangers_rows, photo_data = fetch_data_from_buspassangers(selected_rfid)
    
            if buspassangers_rows:
                buspassangers_df = [dict(zip(col_names, row)) for row in buspassangers_rows]
                st.table(buspassangers_df)
                
                # Show the photo when the button is clicked
                if photo_data:
                    if st.button("View Photo"):
                        image = Image.open(io.BytesIO(photo_data))
                        st.image(image, caption="Passenger Photo", use_column_width=True)
            else:
                st.warning("No data found for the selected RFID.")
    else:
        st.warning("No data retrieved or there was an error.")
        
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
else:
    st.write("Please log in from the sidebar to access the system.")
