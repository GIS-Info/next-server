from django.contrib.auth.models import User
from .serializer import UserListSerializer
from ...viewsets import ModelViewSetWithCustomResponse
from app.response import SuccessResponse


class UserListView(ModelViewSetWithCustomResponse):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'username'
