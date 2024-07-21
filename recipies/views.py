from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from django.db.utils import IntegrityError

from extra import Token
from extra.utils import ErrorResponse
from extra.permissions import JWTPermission
from extra.exceptions import UserDoesNotExist, WrongTokenError

from food.models import Food

from .serializers import RecipieSerializer, RecipieModifySerializer
from .models import Recipie


class Recipies(APIView):
    permission_classes = [JWTPermission]

    def get(self, request, *args, **kwargs):
        context = RecipieSerializer(data=Recipie.objects.all(), many=True)
        context.is_valid(raise_exception=False)
        return Response(context.data)

    def post(self, request, *args, **kwargs):
        serializer = RecipieModifySerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        token = request.META['HTTP_TOKEN']

        try:
            user = Token.get_user(token)
            food = Food.objects.get(pk=request.POST['food'])

            data = serializer.data
            data.update({
                'user': user,
                'food': food
            })

            Recipie.objects.create(**data)
        except (
            UserDoesNotExist,
            WrongTokenError,
            ValueError
        ) as ex:
            return ErrorResponse(ex)
        except IntegrityError:
            return ErrorResponse('Recipie for this food exists.')
        except Food.DoesNotExist:
            return ErrorResponse('Food of this ID does not exists.')

        return Response(status=201)


class RecipiesUpdate(APIView):
    permission_classes = [JWTPermission]

    def post(self, request, *args, **kwargs):
        serializer = RecipieModifySerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        token = request.META['HTTP_TOKEN']

        try:
            user = Token.get_user(token)
            food = Food.objects.get(pk=request.POST['food'])

            data = serializer.data
            data.update({
                'user': user,
                'food': food
            })

            Recipie.objects.update(**data)
        except (
            UserDoesNotExist,
            WrongTokenError,
            ValueError
        ) as ex:
            return ErrorResponse(ex)
        except Food.DoesNotExist:
            return ErrorResponse('Food of this ID does not exists.')

        return Response(status=200)
