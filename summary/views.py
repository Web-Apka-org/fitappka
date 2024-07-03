import logging

from decimal import Decimal
import calendar
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from food.models import ConsumedFood

from extra import Token
from extra.utils import getDatetime
from extra.permissions import JWTPermission
from extra.exceptions import WrongDateFormatError, WrongTokenError


class SummaryView(APIView):
    permission_classes = [JWTPermission]

    def get(self, request, *args, **kwargs):
        '''
        Return summared nutritions consumed by user.

        If only 'from' parameter passed then in date range 'from' to today.
        If only 'to' parameter passed then only from date in 'to'.
        If two paramters passed then in date range 'from' 'to'.
        If no GET parameters are passed then return summared nutritions only
        from this month (server date!).

        It's recommended to always pass date in 'to' because date from
        server might be not the same as on client !

        Date format: '%Y-%m-%d' and '%Y-%m'

        If is used shorted date format then in 'from' is first day and in 'to'
        is last day of month.
        '''
        token = request.META['HTTP_TOKEN']
        formats = ['%Y-%m-%d', '%Y-%m']
        now = datetime.now()
        last_months_day = calendar.monthrange(now.year, now.month)[1]
        date_from = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        date_to = datetime.now().replace(
            day=last_months_day,
            hour=23,
            minute=59,
            second=59
        )

        from_str: str = None
        to_str: str = None
        if 'from' in request.GET:
            from_str = request.GET['from']

        if 'to' in request.GET:
            to_str = request.GET['to']

        try:
            if from_str:
                date_from = getDatetime(from_str, formats)

            if to_str:
                date_to = getDatetime(to_str, formats) \
                            .replace(hour=23, minute=59, second=59)

                # check if its format '%Y-%m'
                if len(to_str) == 7:
                    last_months_day = calendar.monthrange(
                        date_to.year,
                        date_to.month
                    )[1]

                    date_to = date_to.replace(day=last_months_day)

                if not from_str:
                    date_from = getDatetime(to_str, formats)
            
            if date_from > date_to:
                return Response(
                    {
                        'Error': 'Date \'from\' is later than date \'to\'.'
                    },
                    status=403
                )

            header = Token.decode_header(token)
        except (
            WrongDateFormatError,
            WrongTokenError
        ) as ex:
            return Response(
                {
                    'Error': str(ex),
                },
                status=403
            )
        else:
            consumed_foods = ConsumedFood.objects.filter(
                date_eating__range=(date_from, date_to),
                user_id=header['user_id']
            )

            summary = {
                'Energy': int(),
                'Fat': Decimal(),
                'Saturated Fat': Decimal(),
                'Carbo': Decimal(),
                'Sugar': Decimal(),
                'Salt': Decimal(),
                'Protein': Decimal(),
                'Fibre': Decimal(),
                'Alcohol': Decimal()
            }

            for consumed in consumed_foods:
                summary['Energy'] += consumed.food.energy
                summary['Fat'] += consumed.food.fat
                summary['Saturated Fat'] += consumed.food.saturated_fat
                summary['Carbo'] += consumed.food.carbo
                summary['Sugar'] += consumed.food.sugar
                summary['Salt'] += consumed.food.salt
                summary['Protein'] += consumed.food.protein
                summary['Fibre'] += consumed.food.fibre
                summary['Alcohol'] += consumed.food.alcohol

            return Response(summary)
