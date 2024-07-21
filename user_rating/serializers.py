from rest_framework import serializers

from .validators import rating_validators


class UserRatingSerializer(serializers.Serializer):
    recipie = serializers.IntegerField()
    rating = serializers.CharField(validators=rating_validators)
