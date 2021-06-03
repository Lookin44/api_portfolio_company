from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=50)


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=50)
    code = serializers.CharField(required=True)
