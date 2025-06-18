import uuid

from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import ValidationError, NotFound

from current_weather.helpers import get_city_current_weather
from current_weather.tasks import task_process_scheduled_query
from current_weather.models import WeatherQuery
from current_weather.serializers import WeatherQuerySerializer


class WeatherQueryRetrieveMixin:
    """Mixin to validate and extract the 'city' query parameter from the request."""
    def validates_city(self, query_params: dict) -> str:
        city = query_params.get('city')

        if not city:
            raise ValidationError({'city': 'Query parameter is required.'})

        return city


class WeatherQueryRetrieveView(generics.RetrieveAPIView, WeatherQueryRetrieveMixin):
    """
    Retrieve current weather data for a given city.

    This view checks the cache for recent queries.
    If no recent data is found, it fetches fresh weather data from the OpenWeather API,
    stores it, and returns the result.
    """
    serializer_class = WeatherQuerySerializer
    throttle_classes = [AnonRateThrottle]

    def get_object(self):
        city = self.validates_city(self.request.query_params)

        city_current_weather = get_city_current_weather(city)

        if city_current_weather:
            return city_current_weather

        raise NotFound({'city': city})


class WeatherQueryScheduleView(generics.RetrieveAPIView, WeatherQueryRetrieveMixin):
    """
    Schedule a weather data query for a given city.

    This view enqueues an asynchronous task to fetch weather data using Celery.
    It returns a WeatherQuery with a query ID that can be used to retrieve the result later.
    """
    serializer_class = WeatherQuerySerializer
    throttle_classes = [AnonRateThrottle]

    def get_object(self):
        city = self.validates_city(self.request.query_params)

        weather_query = WeatherQuery.objects.create(
            city_name=city,
            query_id=uuid.uuid4().hex,
            status='pending',
        )

        task_process_scheduled_query.delay(weather_query.query_id)

        return weather_query


class WeatherQueryScheduleRetrieveView(generics.RetrieveAPIView):
    """
    Retrieve the result of a previously scheduled weather data query.

    This view returns the weather data associated with the given query ID,
    once the asynchronous task has completed.
    """
    serializer_class = WeatherQuerySerializer
    throttle_classes = [AnonRateThrottle]
    lookup_field = 'query_id'
    queryset = WeatherQuery.objects.all()


class WeatherQueryHistoryListView(generics.ListAPIView):
    """
    List the most recent weather queries.

    This view returns the last 10 weather data queries made by the system,
    ordered by the most recent first.
    """
    queryset = WeatherQuery.objects.order_by('-created_at')[:10]
    serializer_class = WeatherQuerySerializer
    throttle_classes = [AnonRateThrottle]
