from datetime import datetime

from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ConsumedFood
from .serializers import ConsumedFoodSerializer

from extra import Token
from extra.permissions import JWTPermission
from extra.utils import getDatetime
from extra.exceptions import WrongTokenError, WrongDateFormatError


class ConsumedFoodView(mixins.CreateModelMixin, APIView):
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
                return Response(
                    {
                        'Error': 'Date \'from\' is later than date \'to\'.'
                    },
                    status=403
                )

            token = request.META['HTTP_TOKEN']
            user = Token.get_user(token)
        except (
            WrongTokenError,
            WrongDateFormatError
        ) as ex:
            return Response({
                'Error': str(ex),
                status=403
            })
        else:
            data = ConsumedFood.objects.filter(
                user_id=user.id,
                date_eating__range=(date_from, date_to)
            )

            context = ConsumedFoodSerializer(data, many=True)
            return Response(context.data)

    def post(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_TOKEN']
            Token.get_user(token)
        except (
            WrongTokenError
        ) as ex:
            return Response(
                {
                    'Error': str(ex)
                },
                status=403
            )

        if len(request.POST['date_eating']) != 16:
            return Response(
                {
                    'Error': 'Incorrect date format. (accepted: %Y-%m-%d,%H:%M)'
                },
                status=403
            )

        return self.create(request, *args, **kwargs)

    # only for testing
    def put(self, request, *args, **kwargs):
        token = request.META['HTTP_TOKEN']
        user = Token.get_user(token)
        data = ConsumedFoodSerializer(
            ConsumedFood.objects.filter(user_id=user.id),
            many=True
        )
        return Response(data.data)
