from django.urls import path,include
from authapp import views

urlpatterns = [
    path('',include('djoser.urls')),
    path('',include('djoser.urls.authtoken')),
    path('restricted/',views.restricted),
]