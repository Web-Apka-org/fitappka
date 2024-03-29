from django.conf import settings
from django.db import models

from food.models import Food


class Recipie(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    food = models.OneToOneField(
        Food,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
