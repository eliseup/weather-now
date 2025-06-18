"""
Abstract Django models and base classes shared across apps.
"""
from django.db import models


class TimestampedAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
