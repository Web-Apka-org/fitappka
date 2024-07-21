from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from .models import UserRating


# def is_recipie_rated(recipie_id):
#     if UserRating.objects.filter(recipie=recipie_id):
#         raise ValidationError('User already rated this Recipie.')

def rating_validator(value):
    rates = ['1', '2', '3', '4', '5', '6']

    for rate in rates:
        if rate == value:
            return

    raise ValidationError('Wrong rating value, only from 1 to 6.')


rating_validators = [
    MaxLengthValidator(1, 'Only one character allowed.'),
    rating_validator
]
