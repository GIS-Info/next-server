from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializer import UserListSerializer
from ...viewsets import ModelViewSetWithCustomResponse


class UserListView(ModelViewSetWithCustomResponse):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

