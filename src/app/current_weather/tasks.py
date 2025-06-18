from celery import shared_task

from current_weather.helpers import request_city_current_weather, cache_weather
from current_weather.models import WeatherQuery


@shared_task
def task_process_scheduled_query(query_id: str):
    """
    Request OpenWeather API, retrieve the current weather data, and store it in the cache.
    """
    weather_query = WeatherQuery.objects.get(query_id=query_id)

    weather_data = request_city_current_weather(weather_query.city_name)

    if weather_data:
        weather_query.status = 'done'
        weather_query.data = weather_data
        weather_query.save()

        cache_weather(weather_query=weather_query)
