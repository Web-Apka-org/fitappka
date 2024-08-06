from rest_framework import serializers

from .models import Recipie


class RecipieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipie
        fields = '__all__'


class RecipieModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipie
        fields = ['food_id', 'title', 'content']

    # def create(self, validated_data):
    #     pass
