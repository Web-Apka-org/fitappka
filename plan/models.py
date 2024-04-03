from django.conf import settings
from django.db import models

from food.models import Food


class PlannedMeal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()
