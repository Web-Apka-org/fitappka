from datetime import datetime

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import ConsumedFood, Food
from .serializers import ConsumedFoodSerializer

from extra import Token
from extra.permissions import JWTPermission
from extra.utils import getDatetime, ErrorResponse
from extra.exceptions import WrongTokenError, WrongDateFormatError


class ConsumedFoodView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericAPIView):
    permission_classes = [JWTPermission]
    serializer_class = ConsumedFoodSerializer

    def get(self, request, *args, **kwargs):
        '''
        Return list consumed food from specify date.

        If only 'from' parameter passed then in date range 'from' to today.
        If only 'to' parameter passed then only from date in 'to'.
        If two paramters passed then in date range 'from' 'to'.
        If no GET parameters are passed then return list consumed food only
        from today (server date!).

        It's recommended to always pass date in 'to' because date from
        server might be not the same as on client !

        Date format: '%Y-%m-%d'
        '''
        date_from = datetime.now().replace(hour=0, minute=0, second=0)
        date_to = datetime.now().replace(hour=23, minute=59, second=59)

        try:
            if 'from' in request.GET:
                date_from = getDatetime(request.GET['from'])

            if 'to' in request.GET:
                date_to = getDatetime(request.GET['to']) \
                            .replace(hour=23, minute=59, second=59)
                if 'from' not in request.GET:
                    date_from = getDatetime(request.GET['to'])

            if date_from > date_to:
                return ErrorResponse('Date \'from\' is later than date \'to\'.')

            token = request.META['HTTP_TOKEN']
            user = Token.get_user(token)
        except (
            WrongTokenError,
            WrongDateFormatError
        ) as ex:
            return ErrorResponse(ex)
        else:
            data = ConsumedFood.objects.filter(
                user_id=user.id,
                date_eating__range=(date_from, date_to)
            )

            context = ConsumedFoodSerializer(data, many=True)
            return Response(context.data)

    def post(self, request, *args, **kwargs):
        '''
        Create or update record in ConsumedFood table.
        Accepted date format: %Y-%m-%d,%H:%M

        For update you should post 'id' parameter.
        '''
        if not request.POST.keys() >= {'food_id', 'date_eating'}:
            return ErrorResponse('Missing food_id or date_eating in form.')

        date_eating = request.POST['date_eating']
        if len(request.POST['date_eating']) != 16:
            return ErrorResponse(
                'Incorrect date format. (accepted: %Y-%m-%d,%H:%M)'
            )

        token = request.META['HTTP_TOKEN']
        food = Food.objects.get(pk=request.POST['food_id'])

        try:
            user = Token.get_user(token)
        except WrongTokenError as ex:
            return ErrorResponse(ex)
        else:
            if 'id' in request.POST:
                id = request.POST['id']
                try:
                    consumed_food = ConsumedFood.objects.filter(
                        pk=id
                    )
                except ConsumedFood.DoesNotExist:
                    return ErrorResponse(
                        'Failed to update ConsumedFood, wrong ID.'
                    )
                else:
                    consumed_food.update(
                        id=id,
                        user=user,
                        food=food,
                        date_eating=date_eating
                    )
            else:
                ConsumedFood.objects.create(
                    user=user,
                    food=food,
                    date_eating=date_eating
                )

        return Response(status=201)

    def delete(self, request, *args, **kwargs):
        '''
        Delete record from ConsumedFood table.
        Record are deleted by passed 'id'.
        '''
        if 'id' not in request.GET:
            return ErrorResponse('No ID of Consumed Food passed.')

        token = request.META['HTTP_TOKEN']

        try:
            user = Token.get_user(token)
        except WrongTokenError as ex:
            return ErrorResponse(ex)
        else:
            self.queryset = ConsumedFood.objects.filter(
                user=user,
                pk=request.GET['id']
            )

            if self.queryset is None:
                return ErrorResponse('No record with this ID.')

            return self.destroy(request, *args, **kwargs)

    # only for testing
    # return all records in ConsumedFood table
    def put(self, request, *args, **kwargs):
        token = request.META['HTTP_TOKEN']
        user = Token.get_user(token)
        data = ConsumedFoodSerializer(
            ConsumedFood.objects.filter(user_id=user.id),
            many=True
        )
        return Response(data.data)
