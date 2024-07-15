import re

from django.core.exceptions import ValidationError
from django.core.validators import  MaxLengthValidator, \
                            MinLengthValidator, EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import User


def is_username_reserved(username: str):
    if User.objects.filter(username=username):
        raise ValidationError('This username is used by someone.')


username_validators = [
    MinLengthValidator(4, 'Too short username (min 4).'),
    MaxLengthValidator(30, 'Too long username (max 30).'),
    UnicodeUsernameValidator,
    is_username_reserved
]


def is_email_reserved(email: str):
    if User.objects.filter(email=email):
        raise ValidationError('This email is used by someone.')


email_validators = [
    EmailValidator,
    is_email_reserved
]

# Password validator regex function
# check if is required characters:
# - digit
# - uppercase letter
# - character oder than alphanumeric
def password_regex_validator(password: str):
    regex = [
        re.compile(r'[a-z]'),
        re.compile(r'[A-Z]'),
        re.compile(r'[0-9]'),
        re.compile(r'\W')
    ]

    for r in regex:
        if not r.findall(password):
            raise ValidationError(
                'Invalid password. Must have digit, uppercase letter '
                'and special character.')


password_validators = [
    MinLengthValidator(8, 'Too short password (min 8).'),
    MaxLengthValidator(150, 'Too long password (max 150).'),
    password_regex_validator
]
