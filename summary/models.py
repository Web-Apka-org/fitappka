from django.db import models
from django.conf import settings

from food.models import*

class FoodSummary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    consumed_food = models.ForeignKey(
        ConsumedFood,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    microelements = models.ForeignKey(
        Microelements,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    macroelements = models.ForeignKey(
        Macroelements,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    vitamins = models.ForeignKey(
        Vitamins,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

