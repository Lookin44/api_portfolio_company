from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import CompanyViewSet, CompanyNewsViewSet, FollowViewSet

router_v1 = DefaultRouter()

router_v1.register('company', CompanyViewSet)
router_v1.register(r'company/(?P<company_id>[^/.]+)/companynews',
                   CompanyNewsViewSet)
router_v1.register('follow', FollowViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
