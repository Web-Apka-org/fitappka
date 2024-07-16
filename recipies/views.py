from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
# from rest_framework import mixins

from extra.permissions import JWTPermission
from extra.views import CreateModelMixinEmptyResponse

from .serializers import RecipieSerializer


class RecipiesView(CreateModelMixinEmptyResponse, GenericAPIView):
    permission_classes = [JWTPermission]
    serializer_class = RecipieSerializer

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
