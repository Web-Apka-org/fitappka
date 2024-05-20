import logging
from datetime import datetime

from django.http import JsonResponse
from rest_framework import mixins, generics, status

from .models import ConsumedFood, Food
from .serializers import ConsumedFoodSerializer
from .utils import getDatetime


class ConsumedFoodView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    serializer_class = ConsumedFoodSerializer

    def get_queryset(self):
        '''
            Return list consumed food from specify date.

            If only 'from' parameter passed then in date range 'from' to today.
            If only 'to' parameter passed then only from date in 'to'.
            If two paramters passed then in date range 'from' 'to'.
            If no GET parameters are passed then return list consumed food only
            from today (server date!). 

            It's recommended to always pass date in 'to' because date from
            server might be not the same as on client !
        '''
        date_from = datetime.now().replace(hour=0, minute=0, second=0)
        date_to = datetime.now().replace(hour=23, minute=59, second=59)

        if 'from' in self.request.GET:
            date_from = getDatetime(self.request.GET['from'])
                    
        if 'to' in self.request.GET:
            date_to = getDatetime(self.request.GET['to']) \
                            .replace(hour=23, minute=59, second=0)

            if not 'from' in self.request.GET:
                date_from = getDatetime(self.request.GET['to'][:10])

        return ConsumedFood.objects. \
                filter(date_eating__range=(date_from, date_to))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        date_eating = datetime.strptime(request.POST['date_eating'],
                                        '%Y-%m-%d,%H:%M')

        return self.create(request, *args, **kwargs)
