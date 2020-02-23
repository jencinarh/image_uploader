from django.db import models


class Gender(models.TextChoices):
    MALE = 'm', 'Male'
    FEMALE = 'f', 'Female'
