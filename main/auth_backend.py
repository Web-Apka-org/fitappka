from account.models import User
from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):
    def authenticate(self,
                     request,
                     username,
                     email,
                     password,
                     admin=False,
                     **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        if not admin and user.email != email:
            return None

        return user
