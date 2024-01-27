from django.shortcuts import render

# Create your views here.
import json
import logging

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from django.http import JsonResponse

from mailinglist.services import SubscriptionService
from mailinglist.models import MailingList

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger('django')

@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def subscribe_user(request):
    """
    Subscribe a user to a mailing list.

    Example:
    POST http://127.0.0.1:8000/api/subscribe
    Body: {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "mailing_list_slug": "example-slug"
    }
    """
    if request.method == 'POST':
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        mailing_list_slug = request.data.get("mailing_list_slug")
        print(email, first_name, last_name)

        try:
            service = SubscriptionService()
            mailing_list = MailingList.objects.get(slug=mailing_list_slug)
            user = service.create_user(email=email, first_name=first_name, last_name=last_name)
            service.subscribe(user=user, mailing_list=mailing_list)

            # 记录成功的订阅
            logger.info(f"User {email} subscribed to {mailing_list_slug}")

            return Response({"code": 0, "message": "Subscribed successfully, Please check your email"})
        except Exception as e:
            # 记录异常
            logger.error(f"Subscription failed: {str(e)}")
            return JsonResponse({"code": 1, "message": "Subscription failed"})

    else:
        return JsonResponse({"code": 1, "message": "Invalid request method."})
