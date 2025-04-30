import streamlit as st
import mysql.connector
from mysql.connector import OperationalError, IntegrityError
import io
from PIL import Image, UnidentifiedImageError
import time

# App config
st.set_page_config(page_title="RFID-Based Bus Ticket System", layout="wide")

# MySQL Database Config
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Maintain login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
# Function to insert data into BusPassangers table
def insert_data_into_buspassangers(name, gender, age, rfid, balance, photo_data):
    try:
        # Establishing connection to the database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Query to insert data into BusPassangers table
        query = """INSERT INTO BusPassangers (Name, Gender, Age, RFID, Balance, photo)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, gender, age, rfid, balance, photo_data))
        
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success("Registration successful!")
    except Error as e:
        st.error(f"Database error: {e}")
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")

def RegesterPassMain():
    # Streamlit app
    st.title("BusPassangers Registration Form")
    
    # Streamlit form for registration
    with st.form(key='registration_form'):
        name = st.text_input("Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=1, max_value=120)
        rfid = st.text_input("RFID")
        balance = st.number_input("Balance", min_value=0.0, step=0.01)
        
        # Upload photo (either from camera or file)
        photo = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
        if photo is not None:
            st.image(photo, caption="Uploaded Photo", use_column_width=True)
    
        # Submit button for form
        submit_button = st.form_submit_button(label="Register")
    
    # Handle the form submission
    if submit_button:
        if name and gender and age and rfid and balance and photo:
            # Convert image to binary for storage in database
            img_data = photo.read()
    
            # Insert the data into the BusPassangers table
            insert_data_into_buspassangers(name, gender, age, rfid, balance, img_data)
        else:
            st.warning("Please fill out all fields and upload a photo.")
def fetch_data_from_buspassangers(rfid):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        query = "SELECT Name, Gender, Age, RFID, Balance, Photo FROM BusPassangers WHERE RFID = %s"
        cursor.execute(query, (rfid,))
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        photo_data = rows[0][-1] if rows else None
        cursor.close()
        conn.close()
        return col_names[:-1], [row[:-1] for row in rows], photo_data
    except (OperationalError, IntegrityError) as e:
        st.error(f"Database error: {e}")
        return None, None, None

def fetch_data_from_buspass():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        query = "SELECT * FROM BusPass"
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return col_names, rows
    except (OperationalError, IntegrityError) as e:
        st.error(f"Database error: {e}")
        return None, None

def LiveBusMain():
    st.title("Live Bus Passengers")
    col_names, rows = fetch_data_from_buspass()
    if col_names and rows:
        st.subheader("Current Passengers from Bus")
        buspass_df = [dict(zip(col_names, row)) for row in rows]
        st.table(buspass_df)
        rfid_numbers = [row[2] for row in rows]  # Assuming RFID is at index 2
        selected_rfid = st.selectbox("Select RFID No", rfid_numbers)
        if selected_rfid:
            st.subheader(f"Data for RFID {selected_rfid}")
            col_names, data_rows, photo_data = fetch_data_from_buspassangers(selected_rfid)
            if data_rows:
                df = [dict(zip(col_names, row)) for row in data_rows]
                st.table(df)
                if photo_data:
                    try:
                        image = Image.open(io.BytesIO(photo_data))
                        image.verify()
                        image = Image.open(io.BytesIO(photo_data))
                        st.image(image, caption="Passenger Photo", use_container_width=True)
                    except Exception:
                        st.error("Error loading image.")
            else:
                st.warning("No data found.")

    # Refresh without logout
    time.sleep(3)
    st.rerun()

# Sidebar login form
st.sidebar.title("RFID-Based Bus Ticket System")
if not st.session_state.logged_in:
    with st.sidebar.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.sidebar.success("Login successful!")
            else:
                st.sidebar.error("Invalid credentials.")
else:
    st.sidebar.success("You are logged in.")

# Main content
if st.session_state.logged_in:
    tabs = st.tabs(["Recharge Card", "Check Live Status", "Check History", "Register Passenger"])

    with tabs[0]:
        st.subheader("Recharge Card")
        st.markdown('<a href="https://busrfrecharge-aqupzmfkxy3xbvpoq7hybm.streamlit.app/" target="_blank">Click here</a>', unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("Live Bus Status")
        LiveBusMain()

    with tabs[2]:
        st.subheader("Check Travel History")
        st.markdown('<a href="https://bushistory-3ujwysudfgvcpbfdnhexah.streamlit.app/" target="_blank">Click here</a>', unsafe_allow_html=True)

    with tabs[3]:
        st.subheader("Register Passenger")
        RegesterPassMain()
        #st.markdown('<a href="https://regesterpassanger-9iu2puyfxmh9hts5azkwdv.streamlit.app/" target="_blank">Click here</a>', unsafe_allow_html=True)
else:
    st.write("Please log in from the sidebar to access the system.")
