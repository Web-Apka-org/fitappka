from django.conf import settings
from django.db import models

from recipies.models import Recipie


class UserRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    recipe = models.OneToOneField(
        Recipie,
        on_delete=models.CASCADE
    )

    rating = models.CharField(max_length=1)
