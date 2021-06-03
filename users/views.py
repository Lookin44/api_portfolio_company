from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import AdminPermission
from .serializers import (ConfirmationCodeSerializer, UsernameSerializer,
                          UserSerializer)
from users.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation_code(request):
    serializer = UsernameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data['username']
    check_user = User.objects.filter(username=username).exists()
    if not check_user:
        user = User.objects.create(username=username)
        code = default_token_generator.make_token(user)
        return Response(
            {'message': f'Ваш код подтверждения: {code}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Такой пользователь уже существует'},
        status=status.HTTP_403_FORBIDDEN
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data['username']
    code = serializer.data['code']
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, code):
        return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(user)
    return Response({'token': f'{token}'}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
