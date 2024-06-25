from rest_framework import serializers
from .models import  User


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
