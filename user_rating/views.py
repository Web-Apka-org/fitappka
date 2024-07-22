from rest_framework.response import Response
from rest_framework.views import APIView

from extra import Token
from extra.permissions import JWTPermission
from extra.exceptions import WrongTokenError, UserDoesNotExist
from extra.utils import ErrorResponse

from .serializers import UserRatingSerializer
from .models import UserRating


class UserRatingView(APIView):
    permission_classes = [JWTPermission]

    def post(self, request, *args, **kwargs):
        serializer = UserRatingSerializer(data=request.POST)
        serializer.is_valid(raise_exceptions=True)
        token = request.META['HTTP_TOKEN']

        try:
            user = Token.get_user(token)
        except (
            WrongTokenError,
            UserDoesNotExist
        ) as ex:
            return ErrorResponse(ex)
        else:
            data = serializer.data
            data.update({'user': user})

            UserRating.objects.update_or_create(user=user, defaults=data)

            return Response(status=201)
