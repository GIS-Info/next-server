from django.urls import path
from apps.post import views


urlpatterns = [
    path('schools', views.get_school_list, name = 'get_school_list'),
]
