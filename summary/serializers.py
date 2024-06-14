from rest_framework import serializers
from food.models import Food
from account.serializers import*
from rest_framework import serializers
from food.models import Food, ConsumedFood

class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ['energy','fat','saturated_fat']


class ConsumedFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = ConsumedFood
        fields = ['id', 'user', 'food', 'date_eating']


