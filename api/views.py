from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Company, CompanyNews, Follow
from .serializers import (CompanySerializer,
                          CompanyNewsSerializer,
                          FollowSerializer)
from .permissions import IsAuthorOrReadOnlyPermission


class GetPostMethods(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    pass


class CompanyViewSet(viewsets.ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CompanyNewsViewSet(viewsets.ModelViewSet):

    queryset = CompanyNews.objects.all()
    serializer_class = CompanyNewsSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnlyPermission]

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs.get('company_id'))
        return company.news

    def perform_create(self, serializer):
        company = get_object_or_404(Company, pk=self.kwargs.get('company_id'))
        if company.author == self.request.user:
            serializer.save(author=self.request.user, company_id=company.id)


class FollowViewSet(GetPostMethods):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)
