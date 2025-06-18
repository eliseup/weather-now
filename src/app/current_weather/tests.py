from django.urls import reverse
from django.test import SimpleTestCase

from rest_framework.test import APITestCase

from current_weather.models import WeatherQuery
from current_weather.helpers import build_weather_cache_key, gen_weather_query_query_id


class CurrentWeatherTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cities = ['Paris', 'Contagem', 'Belo Horizonte']

        for city in cities:
            WeatherQuery.objects.create(
                query_id=gen_weather_query_query_id(),
                city_name=city.strip().lower(),
                data={},
                status='done'
            )


class CurrentWeatherViewTests(CurrentWeatherTestCase):
    def test_retrieve_city_weather(self):
        response = self.client.get(reverse('weather-query', query={'city': 'London'}))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertIsNotNone(response.json())

    def test_list_history_weather(self):
        response = self.client.get(reverse('weather-history'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertGreaterEqual(len(response.json()), 2)


class CurrentWeatherHelpersTests(SimpleTestCase):
    def test_weather_cache_key_name(self):
        self.assertEqual(build_weather_cache_key('London'), 'WQ:london')
        self.assertEqual(build_weather_cache_key('Belo Horizonte'), 'WQ:belo_horizonte')
        self.assertEqual(build_weather_cache_key('  New yorK '), 'WQ:new_york')
