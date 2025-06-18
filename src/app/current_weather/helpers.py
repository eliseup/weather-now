"""
Helpers for the current_weather app.
"""
import uuid

from typing import Tuple

from django.core.cache import cache

from services.openweather import DirectGeocodingClient, GeocodingDictType, CurrentWeatherClient
from current_weather.models import WeatherQuery


def gen_weather_query_query_id() -> str:
    """Generates a unique query ID to be used in WeatherQuery.query_id."""
    return uuid.uuid4().hex


def build_weather_cache_key(key_name: str) -> str:
    return f'WQ:{key_name.strip().lower().replace(" ", "_")}'


def get_cached_weather(city_name: str) -> WeatherQuery | None:
    cache_key = build_weather_cache_key(city_name)

    return cache.get(cache_key)


def create_and_cache_weather(city_name: str, weather_data: dict) -> WeatherQuery:
    """Creates and caches a WeatherQuery."""
    cache_key = build_weather_cache_key(city_name)

    weather = WeatherQuery.objects.create(
        query_id=gen_weather_query_query_id(), city_name=city_name, data=weather_data, status='done'
    )

    cache.set(cache_key, weather, timeout=600)

    return weather


def cache_weather(weather_query: WeatherQuery):
    """Caches the given WeatherQuery only."""
    cache_key = build_weather_cache_key(weather_query.city_name)
    cache.set(cache_key, weather_query, timeout=600)


def request_city_current_weather(city_name: str) -> dict | None:
    """Request OpenWeather API and retrieve the current weather data."""
    city_name = city_name.strip().lower()
    success, geocoding_data = request_city_geocoding(city_name)

    if geocoding_data:
        current_weather_client = CurrentWeatherClient()

        response = current_weather_client.make_request(
            method='GET',
            params=dict(lat=geocoding_data['lat'], lon=geocoding_data['lon']),
        )

        if response.status_code == 200:
            return response.json()

    return None


def request_city_geocoding(city_name: str) -> Tuple[bool, GeocodingDictType]:
    """Request OpenWeather API for city geocoding data."""
    rtn = dict(lat=None, lon=None)

    geocoding_client = DirectGeocodingClient()

    response = geocoding_client.make_request(
        method='GET',
        params=dict(q=city_name),
    )

    if response.status_code == 200:
        data = response.json()

        if len(data):
            data = data[0]
            rtn['lat'] = data.get('lat')
            rtn['lon'] = data.get('lon')

            return True, rtn

    return False, rtn


def get_city_current_weather(city_name: str) -> WeatherQuery | None:
    """
    First, check if the city weather data is in the cache. If not, request OpenWeather API,
    retrieve the current weather data, store it in the cache, and return it.
    """
    cached_weather = get_cached_weather(city_name)

    if cached_weather:
        return cached_weather

    city_weather_data = request_city_current_weather(city_name)

    if city_weather_data:
        return create_and_cache_weather(city_name, weather_data=city_weather_data)

    return None
