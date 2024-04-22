from rest_framework import serializers
from .models import FoodSummary
from account.serializers import*

class SummarySerializer(serializers.Serializer):
    user = UserSerializer
    class Meta:
        model = FoodSummary
        fields = '__all__'