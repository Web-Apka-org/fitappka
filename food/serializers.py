from rest_framework import serializers
from .models import ConsumedFood


class ConsumedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumedFood
        fields = ['user', 'food', 'date_eating']
