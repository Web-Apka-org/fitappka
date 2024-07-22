from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator


def rating_validator(value):
    rates = ['1', '2', '3', '4', '5', '6']

    for rate in rates:
        if value == rate:
            return

    raise ValidationError('Wrong rating value, only from 1 to 6.')


rating_validators = [
    MaxLengthValidator(1, 'Only one character allowed.'),
    rating_validator
]
