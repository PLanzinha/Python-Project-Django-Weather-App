import requests
from django.shortcuts import render

key = "API_KEY.txt"

try:
    with open(key, "r") as API_KEY_FILE:
        api_key = API_KEY_FILE.read().strip()
except FileNotFoundError:
    raise ValueError("API_KEY file not found!")


def index(request):
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

    if request.method == "POST":
        selected_city = request.POST['selected_city']
        compared_city = request.POST.get('compared_city', None)

        if not selected_city:
            return render(request, "weather_app/index.html", {"error_message": "Please enter a city name!"})

        selected_city_weather = get_weather_forecasts(selected_city, api_key, current_weather_url)

        if compared_city:
            compared_city_weather = get_weather_forecasts(compared_city, api_key, current_weather_url)
        else:
            compared_city_weather = None

        context = {
            "selected_city_weather": selected_city_weather,
            "compared_city_weather": compared_city_weather,
        }

        return render(request, "app/index.html", context)
    else:
        return render(request, "app/index.html")


def get_weather_forecasts(city, key, current_weather_url):
    try:
        current_weather_response = requests.get(current_weather_url.format(city, key))

        if current_weather_response.status_code == 200:
            current_data = current_weather_response.json()

            weather_data = {
                "city": city,
                "temp": round(current_data['main']['temp']),
                "description": current_data['weather'][0]['description'],
                "icon_url": f"https://openweathermap.org/img/wn/{current_data['weather'][0]['icon']}.png"
            }

            return weather_data
        else:
            return "Responses are empty!"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
