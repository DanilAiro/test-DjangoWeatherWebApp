from django.shortcuts import render
import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry


def get_weather_description(weather_code: int) -> str:
    if weather_code in [0]:
        return 'Чистое небо'
    elif weather_code in [1, 2, 3]:
        return 'Преимущественно ясно, переменная облачность, пасмурно'
    elif weather_code in [45, 48]:
        return 'Туман и оседающий изморозь'
    elif weather_code in [51, 53, 55]:
        return 'Морось: слабая, умеренная и интенсивная'
    elif weather_code in [56, 57]:
        return 'Замерзающая морось: слабая и плотная интенсивность'
    elif weather_code in [61, 63, 65]:
        return 'Дождь: слабый, умеренный и сильный'
    elif weather_code in [66, 67]:
        return 'Замерзающий дождь: слабой и сильной интенсивности'
    elif weather_code in [71, 73, 75]:
        return 'Снегопад: слабый, умеренный и сильный'
    elif weather_code in [77]:
        return 'Снежные зерна'
    elif weather_code in [80, 81, 82]:
        return 'Ливневые дожди: слабые, умеренные и сильные'
    elif weather_code in [85, 86]:
        return 'Снежные ливни слабые и сильные'
    elif weather_code in [95]:
        return 'Гроза: слабая или умеренная'
    elif weather_code in [96, 99]:
        return 'Гроза с небольшим и сильным градом'

    return 'Недостаточно данных'


def index(request):
    text = ''

    if request.method == 'POST':
        text = request.POST.get('txt', None)

    if text != '':
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        url1 = f"https://geocoding-api.open-meteo.com/v1/search"
        params_city = {
            "name": text,
            "count": 1,
            "language": "ru",
            "format": "json",
        }
        resp = requests.get(url1, params_city)

        if len(resp.json()) > 1:
            geo_json = resp.json()["results"][0]

            url2 = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": geo_json["latitude"],
                "longitude": geo_json["longitude"],
                "forecast_days": 1,
                "current": "temperature_2m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min",
            }
            responses = openmeteo.weather_api(url2, params=params)

            response = responses[0]
            response_current_t = response.Current().Variables(0).Value()
            weather_code = response.Current().Variables(1).Value()
            current_weather = get_weather_description(weather_code)
            max_t = response.Daily().Variables(0).ValuesAsNumpy()[0]
            min_t = response.Daily().Variables(1).ValuesAsNumpy()[0]

            return render(request, 'main/index.html', {
                'city': f'{geo_json["name"]}, {geo_json["country"]}',
                'current_t': round(response_current_t),
                'max_today': round(max_t),
                'min_today': round(min_t),
                'description': current_weather,
            })

    return render(request, 'main/index.html')
