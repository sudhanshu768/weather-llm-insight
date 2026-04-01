import requests
from datetime import datetime, timedelta
from app.config import WEATHER_API_KEY

BASE_URL = "https://api.weatherapi.com/v1"


def get_current_weather(city):
    url = f"{BASE_URL}/current.json"
    params = {"key": WEATHER_API_KEY, "q": city}

    res = requests.get(url, params=params).json()

    # 🔍 DEBUG
    print("\n[DEBUG] Current Weather API Response:")
    print(res)

    # Handle error
    if "error" in res:
        print("[ERROR] Current Weather:", res["error"]["message"])
        return None

    return {
        "temp": res["current"]["temp_c"],
        "precip": res["current"]["precip_mm"],
        "condition": res["current"]["condition"]["text"]
    }


def get_historical_weather(city, date):
    url = f"{BASE_URL}/history.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "dt": date.strftime("%Y-%m-%d")
    }

    print("\n[DEBUG] Fetching historical date:", date.strftime("%Y-%m-%d"))

    res = requests.get(url, params=params).json()

    # 🔥 MAIN DEBUG LINE (THIS IS WHAT YOU ASKED)
    print("\n[DEBUG] Historical API RESPONSE:")
    print(res)

    # Handle API error
    if "error" in res:
        print("[ERROR] Historical Weather:", res["error"]["message"])
        return None

    if "forecast" not in res:
        print("[ERROR] No forecast data found")
        return None

    day_data = res["forecast"]["forecastday"][0]["day"]

    return {
        "temp": day_data["avgtemp_c"],
        "precip": day_data["totalprecip_mm"],
        "condition": day_data["condition"]["text"]
    }


def get_weather_data(city, compare_type=None, custom_date=None):
    current_data = get_current_weather(city)

    if current_data is None:
        return {
            "city": city,
            "current_temp": None,
            "current_precip": None,
            "current_condition": None,
            "past_temp": None,
            "past_precip": None,
            "past_condition": None,
            "temp_diff": None,
            "error": "Failed to fetch current weather"
        }

    past_data = None

    # Custom date (highest priority)
    if custom_date:
        past_data = get_historical_weather(city, custom_date)

    elif compare_type == "yesterday":
        past_data = get_historical_weather(city, datetime.now() - timedelta(days=1))

    elif compare_type == "last_month":
        past_data = get_historical_weather(city, datetime.now() - timedelta(days=30))

    elif compare_type == "last_year":
        past_data = get_historical_weather(city, datetime.now() - timedelta(days=365))

    # If historical failed
    if (compare_type or custom_date) and past_data is None:
        return {
            "city": city,
            "current_temp": current_data["temp"],
            "current_precip": current_data["precip"],
            "current_condition": current_data["condition"],
            "past_temp": None,
            "past_precip": None,
            "past_condition": None,
            "temp_diff": None,
            "error": "Historical data not available (free API limit: ~7 days)"
        }

    return {
        "city": city,

        # current
        "current_temp": current_data["temp"],
        "current_precip": current_data["precip"],
        "current_condition": current_data["condition"],

        # past
        "past_temp": past_data["temp"] if past_data else None,
        "past_precip": past_data["precip"] if past_data else None,
        "past_condition": past_data["condition"] if past_data else None,

        # diff
        "temp_diff": (
            round(current_data["temp"] - past_data["temp"], 2)
            if past_data else None
        )
    }