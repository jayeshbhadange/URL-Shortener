# URL Shortener with AI-Driven Click Prediction

This project is a URL shortening service built using Python and Flask. It integrates an AI-driven click prediction model to optimize link performance and enhance user experience by generating short URLs with the highest predicted click-through rates.

## Features

- Shorten long URLs to a more manageable length.
- Track the number of clicks on each shortened URL.
- Use a machine learning model to predict and optimize the click likelihood of generated short URLs.
  

## Shorten a URL:
- Run the application: __flask run__
- Open your web browser and go to http://127.0.0.1:5000/.
- Enter the long URL you want to shorten and submit.
- The service will generate an optimized short URL.
- Use the generated short URL to redirect to the original link.
- Click counts will be stored in the database.
