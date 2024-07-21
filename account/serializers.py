from rest_framework import serializers

from .models import User
from .validators import email_validators, username_validators, \
                        password_validators


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
        fields = ['id', 'username', 'email']
        # extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(validators=username_validators)
    email = serializers.EmailField(validators=email_validators)
    password = serializers.CharField(validators=password_validators)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
