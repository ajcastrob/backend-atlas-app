from django.db import models
from apps.base.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100)
    region = models.CharField(max_length=50, blank=True)
    iso_code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.name} - {self.capital}"
