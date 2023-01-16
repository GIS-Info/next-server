from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from knox.auth import TokenAuthentication
from .serializer import UserListSerializer
from ...models import UserInfo


class UserListPagination(PageNumberPagination):
    page_size_query_param = "pageSize"  # 每页最多数据条数
    page_query_param = "pageIndex"  # 第几页


# FIXME: 请求URL在末尾缺少"/"的情况下会自动添加"/"并重定向，在使用DELETE方法请求时，如果缺少"/"会添加"/"并默认重定向为GET
class UserListView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'username'
    pagination_class = UserListPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserInfo.objects.all().order_by('id')
