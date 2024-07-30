import mysql.connector
import pandas as pd
import streamlit as st

# Function to fetch data from MySQL database with filters
def fetch_data(bus_type, route, price_range, star_rating, seat_availability):
    query = "SELECT * FROM bus_details WHERE 1=1"
    params = []

    if bus_type:
        query += " AND Bus_Type=%s"
        params.append(bus_type)

    if route:
        query += " AND Route_Name LIKE %s"
        params.append(f"%{route}%")

    if price_range:
        query += " AND Price BETWEEN %s AND %s"
        params.extend(price_range)

    if star_rating is not None:
        query += " AND Star_Rating>=%s"
        params.append(star_rating)

    if seat_availability:
        query += " AND Seat_Availability BETWEEN %s AND %s"
        params.extend(seat_availability)

    print("SQL Query:", query)  # Debugging information
    print("Params:", params)    # Debugging information

    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='6381167213',
        database='redbus'
    )
    try:
        df = pd.read_sql_query(query, connection, params=params)
    except Exception as e:
        print("SQL Error:", e)  # Debugging information
        df = pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        connection.close()
    
    return df

# Main function to run the Streamlit app
def main():
    st.title("Bus Details")

    st.sidebar.header("Filters")

    # Initialize session state variables if not already set
    if 'bus_type' not in st.session_state:
        st.session_state.bus_type = ""
    if 'route' not in st.session_state:
        st.session_state.route = ""
    if 'price_range' not in st.session_state:
        st.session_state.price_range = (0, 5000)
    if 'star_rating' not in st.session_state:
        st.session_state.star_rating = 0.0
    if 'seat_availability' not in st.session_state:
        st.session_state.seat_availability = (0, 100)

    # Sidebar widgets
    st.session_state.bus_type = st.sidebar.selectbox("Bus Type", options=[
        "", "AMARAVATHI (VOLVO / SCANIA A.C Multi Axle)", "Super Luxury (Non AC Seater 2+2 Push Back)",
        "NIGHT RIDER (SEATER CUM SLEEPER)", "INDRA(A.C. Seater)", "STAR LINER(NON-AC SLEEPER 2+1)",
        "VENNELA (A.C. SLEEPER)", "A/C Sleeper (2+1)", "A/C Seater / Sleeper (2+1)",
        "Bharat Benz A/C Seater /Sleeper (2+1)", "Electric A/C Seater (2+2)", "Electric A/C Seater/Sleeper (2+1)",
        "Non A/C Seater / Sleeper (2+1)", "METRO LUXURY A/C", "ULTRA DELUXE (NON-AC, 2+2 PUSH BACK)",
        "NON A/C Push Back (2+2)", "Express(Non AC Seater)", "NON A/C Seater (2+3)",
        "Scania Multi-Axle AC Semi Sleeper (2+2)", "NON A/C Seater/ Sleeper (2+1)", "NON A/C Semi Sleeper / Sleeper (2+1)",
        "A/C Seater/Sleeper (2+1)", "Volvo Multi Axle A/C Sleeper I-Shift B11R (2+1)", 
        "Volvo Multi-Axle I-Shift A/C Semi Sleeper (2+2)", "Scania AC Multi Axle Sleeper (2+1)", 
        "Volvo A/C B11R Multi Axle Semi Sleeper (2+2)", "VE A/C Sleeper (2+1)", "Bharat Benz A/C Sleeper (2+1)", 
        "SAPTAGIRI EXPRESS", "A/C Semi Sleeper / Sleeper (2+1)", "Scania A/C Semi Sleeper (2+2)", 
        "Bharat Benz NON A/C sleeper (2+1)", "Volvo Multi Axle Sleeper B11R (2+1)", "NON AC Seater / Sleeper 2+1", 
        "NON A/C Seater Push Back (2+2)", "NON A/C Semi Sleeper (2+2)", "DOLPHIN CRUISE (VOLVO / SCANIA A.C Multi Axle)", 
        "NON A/C Hi-Tech Push Back (2+2)", "Volvo Multi-Axle A/C Sleeper (2+1)", "Volvo Multi-Axle Sleeper A/C (2+1)", 
        "Volvo 9600 Multi-Axle A/C Sleeper (2+1)", "Volvo A/C Sleeper (2+1)", "Mercedes Benz Multi-Axle A/C Sleeper (2+1)", 
        "Volvo 9600 A/C Seater/Sleeper (2+1)", "A/C Volvo B11R Multi-Axle Sleeper (2+1)", 
        "Volvo Multi-Axle A/C Semi Sleeper (2+2)", "Non AC Seater (2+2)", "NON A/C Executive (2+1)", 
        "Volvo Multi Axle B9R A/C Sleeper (2+1)", "VE Executive A/C Sleeper (1+1)", "NON A/C Seater PushBack (2+2)", 
        "NON A/C Hi-Tech (2+2)", "NON A/C Seater (2+2)", "A/C Seater Push Back (2+2)", 
        "RAJADHANI AC (CONVERTED METRO LUXURY)", "RAJDHANI (A.C. Semi Sleeper)", "Lahari A/C sleeper", 
        "Lahari Non A/C Sleeper Cum Seater", "Bharat Benz A/C Seater (2+2)", "NON A/C Airbus (2+2)", 
        "AC Seater (2+2)", "LAHARI A/C SLEEPER CUM SEATER", "Deluxe (Non AC Seater 2+2)", 
        "Volvo Multi-Axle A/C seater/sleeper (2+1)", "Ordinary Non AC Seater 2+3", "Shatabdi AC Seater 2+2", 
        "Volvo AC Seater 2+2", "Janrath AC Seater 2+3", "Janrath AC Seater 2+2", "Rajdhani Non AC Seater 2+3", 
        "AshokLeyland Stile A/C", "A/C Seater (2+2)", "Pink Express AC Seater 2+2", "VE A/C Seater / Sleeper (2+1)", 
        "A/C Seater / Sleeper (2+2)", "VE A/C Seater / Sleeper (2+2)", "A/C Sleeper (2+2)", "VE A/C Seater (2+2)", 
        "A/C Semi Sleeper (2+2)", "Bharat Benz A/C Semi Sleeper (2+2)", "VE A/C Semi Sleeper (2+2)", 
        "NON A/C Seater / Sleeper (3+1)", "Volvo AC Seater (2+2)", "Express Non AC Seater 2+3", 
        "Volvo A/C Seater / Sleeper (2+1)", "AC Seater (2+3)", "NON A/C Sleeper (1+2)", "Volvo A/C Seater / Sleeper (2+2)", 
        "A/C Seater Tempo Traveller (2+1)", "Non AC Seater (2+3)", "Volvo AC Semi Sleeper (2+2)", 
        "Non A/C Seater Push Back (2+2)", "Ashok Leyland Stile A/C", "Volvo A/C Seater (2+2)", 
        "Volvo A/C Multi Axle Sleeper (2+1)", "Volvo A/C Multi Axle (2+1)", "Volvo B11R Multi Axle Semi Sleeper (2+2)", 
        "Mercedes Multi-Axle Semi Sleeper (2+2)", "Super Luxury Volvo AC Seater Pushback 2+2", 
        "Himmani Deluxe 2+2 Non AC Seater", "Volvo Multi-Axle A/C Semisleeper (2+2)", 
        "Volvo Multi-Axle B9R A/c Semi Sleeper (2+2)", "Super Deluxe Non AC Seater Air Bus (2+2)", 
        "Swift Deluxe Non AC Air Bus (2+2)", "SWIFT-GARUDA A/C SEATER BUS", "Super Fast Non AC Seater (2+3)", 
        "Low Floor AC Seater 2+2", "2+1 Air Suspension A/C Seater / Sleeper", "AC MULTI AXLE", 
        "A/C Seater Hi-Tech Push Back (2+2)", "A/C Seater / Sleeper (3+1)"
    ])

    st.session_state.route = st.sidebar.text_input("Route")
    st.session_state.price_range = st.sidebar.slider("Price Range", 0, 5000, (0, 5000))
    st.session_state.star_rating = st.sidebar.slider("Star Rating", 0.0, 5.0, 0.0)
    st.session_state.seat_availability = st.sidebar.slider(
        "Seat Availability", 
        min_value=0, 
        max_value=100, 
        value=(0, 100), 
        step=1
    )

    # Button to apply filters
    if st.sidebar.button("Apply Filters"):
        data = fetch_data(
            bus_type=st.session_state.bus_type,
            route=st.session_state.route,
            price_range=st.session_state.price_range,
            star_rating=st.session_state.star_rating,
            seat_availability=st.session_state.seat_availability 
        )
        st.dataframe(data)
    else:
        st.write("Apply filters to see the results.")

    # Button to reset filters
    if st.sidebar.button("Reset Filters"):
        st.session_state.bus_type = ""
        st.session_state.route = ""
        st.session_state.price_range = (0, 5000)
        st.session_state.star_rating = 0.0
        st.session_state.seat_availability = (0, 100)
        st.experimental_rerun()

if __name__ == "__main__":
    try:
        import pyarrow  # Check if pyarrow is installed
        print("pyarrow version:", pyarrow.__version__)
    except ImportError:
        print("pyarrow is not installed.")
    except OSError as e:
        print(f"OS error: {e}")
    
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {e}")
