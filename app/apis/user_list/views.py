from django.contrib.auth.models import User
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .serializer import UserListSerializer
from ...renders import APIRenderer


class UserListPagination(PageNumberPagination):
    page_size_query_param = "pageSize"  # 每页最多数据条数
    page_query_param = "pageIndex"  # 第几页


class UserListView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'username'
    renderer_classes = [APIRenderer, BrowsableAPIRenderer]
    pagination_class = UserListPagination
    def get_queryset(self):
        return User.objects.all().order_by('id')