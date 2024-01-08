"""nextServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

Router system: url --- view
"""
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from app.views import UserListView
from django.conf import settings

from . import views

router = DefaultRouter()
router.register('api/manage/user', UserListView)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.hello),
    path('hello/', views.hello_world),
    path('', include(router.urls)),
    path('api/', include("apps.post.urls")),
    path('api/', include("apps.school.urls")),
    path('', include('accounts.urls')),
    path("mailinglist/", include("mailinglist.urls", namespace="mailinglist")),
]
if settings.DEBUG:
    urlpatterns += [path('', include('app.apis.swagger.urls')),
                    ]