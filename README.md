# <b>FastAPI + SQLAlchemy 2.0 + MySQL + OpenWeatherMap API</b>

A demonstration of Python REST API backend app that can interact with [OpenWeatherMap API](https://openweathermap.org/api).

The backend app is built with [FastAPI](https://fastapi.tiangolo.com/) framework.

MySQL Database is used to store user and weather preference data.

[PyOWM](https://github.com/csparpa/pyowm) library is used to call the OpenWeatherMAP API.

SQL Database connection is handled by [SQLAlchemy](https://www.sqlalchemy.org/) 2.0.x library.

## <b> Getting Started </b>

### Requirements

* Python v3.10.x or newer.
* MySQL database v8.0 or newer with an empty database/schema prepared.
* OpenWeaterMap API Key that you can get by creating an account in [OpenWeatherMap](https://openweathermap.org/) website.

### How to install the app

* Initialize and activate virtual environment inside the project folder:
    ```bash
    $ python3 -m venv venv
    $ . venv/bin/activate
    ```
* Install the required libraries:

    ```bash
    $ pip3 install -r requirements.txt
    ```

* In `.env` file, set the `DB_URL` environment variable to your database url and set the `OWM_API_KEY` environment variable to your OpenWeatherMap API key.

### How to run the app

* Activate the virtual environment if you haven't already:
    ```bash
    $ . venv/bin/activate
    ```

* Run the server:
    ```bash
    $ uvicorn main:app --reload
    ```
    The server will run at http://localhost:8000

    The swagger API docs can be accessed at http://localhost:8000/docs

    The tables in database will be created automatically if they don't exist yet when the server starts or restarts.

## API Endpoints Information

1. `POST /users` (Create a new user endpoint)
   * Create a new user.
   * Accept `email`, `password`, `confirm_password`, and `user_name` values.

2. `GET /users/:user_id` (Get a user by id endpoint)
   * Find user by id and return its detail and preference data.

3. `PUT /users/:user_id/preference` (Update user preference endpoint)
   * Update user preference related to best day recommendation from 5-day weather forecast.
   * Accepted values (all fields are optional/nullable):
     * `location`: User location (e.g. "Berlin,DE")
     * `temp_min`: Min accepted temperature (e.g. 300.5)
     * `temp_max`: Max accepted temperature (e.g. 310)
     * `max_cloudiness`: Max accepted cloudiness (e.g. 99)
     * `max_wind_speed`: Max accepted wind speed (e.g. 8)
     * `max_rain_volume`: Max accepted rain volume (e.g. 1.5)
     * `max_snow_volume`: Max accepted snow volume (e.g. 2)

4. `GET /users/:user_id/weather` (Get user's current weather data endpoint)
   * Return user's current weather data from OpenWeatherMap.

5. `GET /users/:user_id/forecast-best-day` (Find the recommended best day from 5-day weather forecast endpoint)
   * Find and return the recommended best day from OpenWeatherMap's 5-day weather forecast for a user.
   * User's `location` in preference must be set for this endpoint to work.
   * If no best day can be found, 404 (not found) error response will be returned.

The API endpoint's request parameter and response body details can be seen in the swagger API docs (http://localhost:8000/docs)
