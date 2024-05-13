from datetime import datetime

from rest_framework import mixins
from rest_framework import generics

from .models import ConsumedFood
from .serializers import ConsumedFoodSerializer


class ConsumedFoodView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    serializer_class = ConsumedFoodSerializer

    def get_queryset(self):
        date_from = datetime.now().replace(hour=0, minute=0)
        date_to = datetime.now().replace(hour=23, minute=59)

        if 'from' in self.request.GET:
            date_from = datetime.strptime(self.request.GET['from'], '%Y-%m-%d')
        if 'to' in self.request.GET:
            date_to = datetime.strptime(self.request.GET['to'], '%Y-%m-%d') \
                              .replace(hour=23, minute=59)

            if not 'from' in self.request.GET:
                date_from = datetime. \
                        strptime(self.request.GET['to'], '%Y-%m-%d')

        return ConsumedFood.objects. \
                filter(date_eating__range=(date_from, date_to))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
