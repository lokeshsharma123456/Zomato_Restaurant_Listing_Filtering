import streamlit as st
import requests

# Define the base URL of your Flask API
base_url = 'http://localhost:5000'

# Define the endpoint URLs
restaurants_url = f'{base_url}/restaurants'
restaurant_url = f'{base_url}/restaurant/'

# Fetch restaurants from the API
response = requests.get(restaurants_url)
restaurants_data = response.json()

# Restaurant List Page
if st.button('Refresh Restaurant List'):
    response = requests.get(restaurants_url)
    restaurants_data = response.json()

st.header("Restaurant List")
page = st.number_input("Page number", min_value=1, value=1)
per_page = st.number_input("Restaurants per page", min_value=1, value=10)

st.title('Restaurant List')
for restaurant in restaurants_data['restaurants']:
    if st.button(restaurant['Restaurant Name']):
        # Navigate to Restaurant Detail Page
        restaurant_id = restaurant['Restaurant ID']
        response = requests.get(restaurant_url + str(restaurant_id))
        restaurant_detail = response.json()
        st.title('Restaurant Detail')
        st.write(f"Name: {restaurant_detail['Restaurant Name']}")
        st.write(f"Location: {restaurant_detail['Locality']}")
        st.write(f"Cuisine: {restaurant_detail['Cuisines']}")
        st.write(f"Rating: {restaurant_detail['Aggregate rating']}")


def get_restaurant_by_id(restaurant_id):
    response = requests.get(restaurant_url + str(restaurant_id))
    return response.json()

# Restaurant Detail Page
st.write("Restaurant Detail Page")
