from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, confirmation_code, get_token

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')


registration = [
    path('create_user/', confirmation_code),
    path('get_token/', get_token),
]
urlpatterns = [
    path('v1/auth/', include(registration)),
    path('v1/', include(router_v1.urls)),
]
