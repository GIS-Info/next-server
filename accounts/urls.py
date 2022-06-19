from .views import RegisterAPI, LoginAPI
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/manage/register/', RegisterAPI.as_view(), name='register'),
    path('api/manage/login/', LoginAPI.as_view(), name='login'),
    path('api/manage/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/manage/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]