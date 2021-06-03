from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Company, CompanyNews, Follow
from users.models import User


class CompanySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        fields = '__all__'
        model = Company


class CompanyNewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = CompanyNews


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError('Вы не можете сами'
                                              ' на себя подписываться!')
        return value

    class Meta:
        fields = '__all__'
        model = Follow
        read_only_fields = ['user', 'following']
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
            )
        ]
