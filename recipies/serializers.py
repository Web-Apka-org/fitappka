from rest_framework import serializers

from .models import Recipie


class RecipieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipie
        fields = '__all__'
