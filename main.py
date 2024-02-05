from datetime import datetime
import os
import requests

# Define constants
OWM_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/"
SHEETY_ENDPOINT = "https://api.sheety.co/"
PIXELA_USERNAME = "rahulp"
PIXELA_GRAPH_ID = "graph001"
SHEETY_SHEET_NAME = "workouts"
SHEETY_PROJECT_NAME = "workoutTracking"
GENDER = "male"
AGE = 4
MY_LAT = 51.78
MY_LONG = -1.53
MY_PHONE = "+44"

# Define environment constants
OWM_API_KEY = os.environ["OWM_API_KEY"]
PIXELA_TOKEN = os.environ["PIXELA_TOKEN"]
APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
GSHEET_URI = os.environ["GSHEET_URI"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]

# Use OWM API to get local weather data
owm_parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": OWM_API_KEY,
}

response = requests.get(url=OWM_ENDPOINT, params=owm_parameters)
response.raise_for_status()
data = response.json()

# Print results
print(response)
print(type(data))
print(data)

# Use Pixela API to post an update to a Pixela graph
headers = {
    "X-USER-TOKEN": PIXELA_TOKEN
}
p_body = {
    "date": "20230719",
    "quantity": "39",
}

response = requests.post(url=f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{PIXELA_GRAPH_ID}", headers=headers, json=p_body)
response.raise_for_status()

# Print results
print(response.text)

# Use Nutrition IX API to post exercises and return exercises data
exercise_text = input("Tell me which exercises you did: ")

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}
nutritionix_params = {
    "query": exercise_text,
    "gender": GENDER,
    "age": AGE,
}

response = requests.post(
    url=f"{NUTRITIONIX_ENDPOINT}v2/natural/exercise",
    headers=nutritionix_headers,
    json=nutritionix_params
)
response.raise_for_status()
exercises_list = response.json()["exercises"]

# Use Sheety API to post exercises data to Google sheet
sheety_headers = {
    "Authorization": SHEETY_TOKEN,
}

today = datetime.today()
for activity in exercises_list:
    sheety_params = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": activity["name"].title(),
            "duration": activity["duration_min"],
            "calories": activity["nf_calories"],
        }
    }
    response = requests.post(
        url=f"{SHEETY_ENDPOINT}{GSHEET_URI}/{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}",
        headers=sheety_headers,
        json=sheety_params
    )
    response.raise_for_status()
