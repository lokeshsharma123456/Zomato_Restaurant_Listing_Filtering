import pandas as pd
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS, cross_origin
import math
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



# Load the data
file_path = 'archive/zomato.csv'
zomato_data = pd.read_csv(file_path, encoding='ISO-8859-1')
zomato_data = zomato_data.fillna('')
zomato_dict = zomato_data.set_index('Restaurant ID').T.to_dict()
# base page
@app.route('/')
def index():
    return send_from_directory('build', 'index.html')

# sending along with the build folder and index.html which runs 
@app.route('/static/js/<path:filename>')
def serve_static_js_file(filename):
    return send_from_directory('build/static/js', filename)


@app.route('/static/css/<path:filename>')
def serve_static_css_file(filename):
    return send_from_directory('build/static/css', filename)


@app.route('/static/media/<path:filename>')
def serve_static_media_file(filename):
    return send_from_directory('build/static/media', filename)


@app.route('/<path:filename>')
def serve_static_local_file(filename):
    return send_from_directory('build', 'index.html')


@cross_origin()
@app.route('/api/restaurant/<int:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    restaurant = zomato_dict.get(restaurant_id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found, please check once. for testing use id- 6317637'}), 404
    return jsonify(restaurant)



@cross_origin()
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    page_number = request.args.get('page_number', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    search_query = request.args.get('search_query', default='', type=str)
    cuisine = request.args.get('cuisine', default='', type=str)
    country = request.args.get('country', default='', type=str)
    filtered_data = zomato_data[
        (zomato_data['Restaurant Name'].str.contains(search_query, case=False)) &
        (zomato_data['Cuisines'].str.contains(cuisine, case=False))
    ]
    # print("country is " + country)
    if country:
        print("filtering with country")
        filtered_data = filtered_data[filtered_data['Country Code'] == int(country)]
    # Calculate start and end indices
    start = (page_number - 1) * per_page
    end = start + per_page
    
    # Fetch the required slice of data
    restaurants_slice = filtered_data.iloc[start:end]
    restaurants_list = restaurants_slice.to_dict(orient='records')
    
    # Create response
    response = {
        'page': page_number,
        'per_page': per_page,
        'total': len(filtered_data),
        'restaurants': restaurants_list
    }
    
    return jsonify(response)

@cross_origin()
@app.route('/api/filter', methods=['GET'])
def get_cuisine():
     
    # Extract unique cuisines
    unique_cuisines = zomato_data['Cuisines'].str.split(', ').explode().str.strip().unique()
    unique_cuisines = list(unique_cuisines)  # Convert to list for JSON serialization
    country_code_file_path = 'archive/Country-code.xlsx'
    country_code_data = pd.read_excel(country_code_file_path)
    country_codes = [
            {"id": str(row['Country Code']), "name": row['Country']}
            for index, row in country_code_data.iterrows()
            ]

    filtered_data = zomato_data
    result = filtered_data.to_dict(orient='records')
    response_data = {
        "cuisines": unique_cuisines,
        "country_codes": country_codes
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
