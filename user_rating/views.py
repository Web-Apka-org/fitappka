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

    def get(self, request, *args, **kwargs):
        token = request.META['HTTP_TOKEN']

        try:
            user = Token.get_user(token)
        except WrongTokenError as ex:
            return ErrorResponse(ex)
        else:
            user_rating = UserRating.objects.filter(user=user)
            serializer = UserRatingSerializer(data=user_rating, many=True)
            serializer.is_valid(raise_exception=False)

            return Response(serializer.data, status=200)

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

            UserRating.objects.update_or_create(
                user=user,
                recipie=data.recipie,
                defaults=data
            )

            return Response(status=201)

    def delete(self, request, *args, **kwargs):
        if 'id' not in request.GET:
            return ErrorResponse('No ID of User Rating passed.')

        try:
            user_rating = UserRating.objects.get(pk=request.GET['id'])
            user_rating.delete()
            return Response(status=204)
        except UserRating.DoesNotExist:
            return ErrorResponse('User Rating of this ID does not exists.')
        except ValueError as ex:
            return ErrorResponse(ex)
