from django.urls import path
from apps.subscriptions import views


urlpatterns = [
    path('subscribe', views.subscribe_user, name = 'subscribe_user'),
    path('subscribe/<str:token>/confirm', views.confirm_subscription, name='subscribe_confirm'),
]
