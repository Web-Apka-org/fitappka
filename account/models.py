from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _


class User(AbstractUser):
    first_name = None
    last_name = None

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_(
            'Required. Letters, digits and @/./+/-/_ only. '
            '(max 30 characters)'
        ),
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
