from rest_framework import mixins
from rest_framework.response import Response


class CreateModelMixinEmptyResponse(mixins.CreateModelMixin):
    '''
    Custom mixin for creating new model object which return empty response.
    '''

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)
