from django.db import models
from django.utils import timezone
from uuid6 import uuid7


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=20)
    gender_probability = models.FloatField()
    sample_size = models.IntegerField()
    age = models.IntegerField()
    age_group = models.CharField(max_length=20)
    country_id = models.CharField(max_length=3)
    country_probability = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name