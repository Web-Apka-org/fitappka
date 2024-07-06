from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''
    def create(self, validated_data):
        user = User(
            id = validated_data['id']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    '''
    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=30)
    email = serializers.EmailField()
    password1 = serializers.CharField(min_length=8)
