from django.urls import path

from current_weather.views import WeatherQueryRetrieveView, WeatherQueryHistoryListView, \
    WeatherQueryScheduleView, WeatherQueryScheduleRetrieveView


urlpatterns = [
    path('weather', WeatherQueryRetrieveView.as_view(), name='weather-query'),
    path('weather/schedule', WeatherQueryScheduleView.as_view(), name='weather-schedule'),
    path('weather/history', WeatherQueryHistoryListView.as_view(), name='weather-history'),
    path(
        'weather/result/<str:query_id>',
        WeatherQueryScheduleRetrieveView.as_view(),
        name='weather-result'
    ),
]
