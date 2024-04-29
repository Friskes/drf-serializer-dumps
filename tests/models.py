from django.contrib.postgres.fields import ArrayField
from django.db import models


class Person(models.Model):  # noqa: DJ008
    name = models.CharField(max_length=256)
    phones = ArrayField(models.CharField(max_length=256))
