from django.db import models

from common.models import TimestampedAbstractModel


class WeatherQuery(TimestampedAbstractModel):
    query_id = models.CharField(max_length=255, unique=True)
    city_name = models.CharField(max_length=45)
    data = models.JSONField(null=True, blank=True)

    # Using CharField instead of a separate model for simplicity.
    status = models.CharField(max_length=20, default='pending')  # pending, done, failed

    class Meta:
        ordering = ['-created_at']
