import streamlit as st
import requests
import math

# Flask API endpoints
API_BASE_URL = 'http://localhost:5000'  # Update with your Flask API base URL
restaurant_api_entry = '/restaurant'

# Navigation bar for Restaurant List Page
st.sidebar.header("Restaurant List Page")
navigation_list = st.sidebar.radio("Navigation", ["Resturant By Id", "Restaurant List"])

# Navigation bar for Restaurant Detail Page
st.sidebar.header("Additoinal Use ")
navigation_detail = st.sidebar.radio("Navigation", ["Home", "Restaurant Detail"])


if navigation_list == "Resturant By Id":
    st.header("Restaurant By Id")
    insert_id = st.number_input("Enter Restaurant ID:", value=6317637 )
    if st.button("Fetch Restaurant"):
        url = API_BASE_URL + restaurant_api_entry + "/id=" + str(insert_id)
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            st.header("Restaurant Details")
            table_data = []
            st.subheader(f"Name : {response_json['Restaurant Name']}")
            for key, value in response_json.items():
                table_data.append([f'{key}', value])

            st.table(table_data)
            # Display the JSON response in a formatted way
        else:
            st.error(f"Error fetching restaurant data: {response.status_code}")
            st.write("Please enter a valid ID. try 6317637 for testing.")
         
elif navigation_list == "Restaurant List":
    # Function to fetch restaurants based on page number and per page count
    def fetch_restaurants(page_number, per_page):
        url = f"{API_BASE_URL}/restaurant?page_number={page_number}&per_page={per_page}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    st.header("Restaurant List Page")
    per_page_options = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Customize as needed
    per_page = st.selectbox("Restaurants per page", per_page_options)

    # Fetch restaurants based on page number and per page count
    page_number = st.number_input("Page Number", min_value=1, value=1)
    restaurants_data = fetch_restaurants(page_number, per_page)

    if restaurants_data is not None:
        st.header("Restaurants")
        number_of_records = restaurants_data['total']
        max_page = math.ceil(number_of_records / per_page)
        

        for restaurant in restaurants_data['restaurant']:
            expander = st.expander(f"{restaurant['Restaurant Name']} (ID: {restaurant['Restaurant ID']})")
            with expander:
                table_data = []
                st.subheader(f"Restraunt Name : {restaurant['Restaurant Name']}")
                for key, value in restaurant.items():
                    table_data.append([f'{key}', value])
                st.table(table_data)