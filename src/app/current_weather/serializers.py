from rest_framework import serializers

from current_weather.models import WeatherQuery


class WeatherQuerySerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()

    def get_city_name(self, obj):
        return obj.city_name.title()

    class Meta:
        model = WeatherQuery
        fields = ['created_at', 'updated_at', 'city_name', 'status', 'query_id', 'data']
        read_only_fields = fields
