from rest_framework import mixins
from rest_framework import generics

from .models import ConsumedFood
from .serializers import ConsumedFoodSerializer


class ConsumedFoodView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    queryset = ConsumedFood.objects.all()
    serializer_class = ConsumedFoodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
