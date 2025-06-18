import requests

from typing import TypedDict, Union
from dataclasses import dataclass, field

from django.conf import settings

from utils.mixins import StringEnumMixin


GeocodingDictType = TypedDict(
    'GeocodingDictType', {'lat': Union[float, None], 'lon': Union[float, None]}
)


@dataclass
class OpenWeatherAPITypes(StringEnumMixin):
    CURRENT_WEATHER: str = 'CURRENT_WEATHER'
    GEOCODING: str = 'GEOCODING'


@dataclass
class OpenWeatherClient:
    """A client to be used when requesting OpenWeather APIs."""
    api_type: OpenWeatherAPITypes
    api_key: str = field(default=settings.OPENWEATHER_API_KEY)
    base_url: str = field(init=False, default='https://api.openweathermap.org')
    api_url: str = field(init=False)

    def __post_init__(self):
        self._set_api_url()

    def _set_api_url(self):
        if self.api_type.value == OpenWeatherAPITypes.CURRENT_WEATHER.value:
            self.api_url = f'{self.base_url}/data/2.5'

        elif self.api_type.value == OpenWeatherAPITypes.GEOCODING.value:
            self.api_url = f'{self.base_url}/geo/1.0'

    def _build_url(self, path: str) -> str:
        return f'{self.api_url}{path}'

    def make_request(
            self,
            *,
            method: str,
            path: str,
            params: dict = None,
            payload: dict = None,
            headers: dict = None,
    ) -> requests.Response | None:
        url = self._build_url(path)
        params['appid'] = self.api_key

        try:
            return requests.request(
                method=method,
                url=url,
                headers=headers,
                json=payload,
                params=params
            )

        except requests.exceptions.RequestException as e:
            # Todo - Improve
            print('Error......', str(e))

        return None


@dataclass
class CurrentWeatherClient(OpenWeatherClient):
    def __init__(self):
        super().__init__(api_type=OpenWeatherAPITypes.CURRENT_WEATHER)

    def _set_api_url(self):
        super()._set_api_url()
        self.api_url = f'{self.api_url}/weather'

    def make_request(
            self,
            method: str,
            path: str = '',
            params: dict = None,
            payload: dict = None,
            headers: dict = None,
    ) -> requests.Response | None:
        return super().make_request(
            method=method,
            path=path,
            params=params,
            payload=payload,
            headers=headers
        )


@dataclass
class DirectGeocodingClient(OpenWeatherClient):
    def __init__(self):
        super().__init__(api_type=OpenWeatherAPITypes.GEOCODING)

    def _set_api_url(self):
        super()._set_api_url()
        self.api_url = f'{self.api_url}/direct'

    def make_request(
            self,
            method: str,
            path: str = '',
            params: dict = None,
            payload: dict = None,
            headers: dict = None,
    ) -> requests.Response | None:
        return super().make_request(
            method=method,
            path=path,
            params=params,
            payload=payload,
            headers=headers,
        )
