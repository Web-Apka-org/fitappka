from django.conf import settings
from django.db import models


kwargs = {'max_digits': 6, 'decimal_places': 2}

class Food(models.Model):
    name = models.CharField(max_length=80)
    energy = models.IntegerField()
    fat = models.DecimalField(**kwargs)
    saturated_fat = models.DecimalField(**kwargs)
    carbo = models.DecimalField(**kwargs)
    sugar = models.DecimalField(**kwargs)
    salt = models.DecimalField(**kwargs)
    protein = models.DecimalField(**kwargs)
    fibre = models.DecimalField(**kwargs)
    alcohol = models.DecimalField(**kwargs)


class ConsumedFood(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    date_eating = models.DateTimeField()


class Microelements(models.Model):
    food = models.OneToOneField(
        Food,
        on_delete=models.CASCADE
    )

    fluorite = models.DecimalField(**kwargs)
    iodine = models.DecimalField(**kwargs)
    chromium = models.DecimalField(**kwargs)
    copper = models.DecimalField(**kwargs)
    zink = models.DecimalField(**kwargs)
    iron = models.DecimalField(**kwargs)


class Macroelements(models.Model):
    food = models.OneToOneField(
        Food,
        on_delete=models.CASCADE
    )

    calcium = models.DecimalField(**kwargs)
    phosphor = models.DecimalField(**kwargs)
    magnesium = models.DecimalField(**kwargs)
    potassium = models.DecimalField(**kwargs)


class Vitamins(models.Model):
    food = models.OneToOneField(
        Food,
        on_delete=models.CASCADE
    )

    a = models.DecimalField(**kwargs)
    c = models.DecimalField(**kwargs)
    d = models.DecimalField(**kwargs)
    e = models.DecimalField(**kwargs)
    k = models.DecimalField(**kwargs)
    b1 = models.DecimalField(**kwargs)
    b2 = models.DecimalField(**kwargs)
    b3 = models.DecimalField(**kwargs)
    b5 = models.DecimalField(**kwargs)
    b6 = models.DecimalField(**kwargs)
    b7 = models.DecimalField(**kwargs)
    b9 = models.DecimalField(**kwargs)
    b12 = models.DecimalField(**kwargs)
