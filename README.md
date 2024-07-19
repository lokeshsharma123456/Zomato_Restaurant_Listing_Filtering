# Zomato Restaurant API

This project provides a Flask-based API for accessing and filtering Zomato restaurant data.

## Installation and Setup

1. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
2. **Run the web service:**

   ```bash
   python webServices.py
   ```

The server will be created at `127.0.0.1:5000`.

## API Endpoints

- `/api/restaurants/{idNumber}`: Get restaurant details by ID.
- `/api/restaurants?page_number={numb}&per_page={23}`: Get restaurants with pagination.

http://localhost:5000//api/restaurant/6317637

http://localhost:5000//api/restaurants

npm start

npm run
