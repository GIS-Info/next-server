import json
import logging

from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import GISource
from .serializer import GISourceSerializer

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_posts_by_params(request):
    params = {
        'is_public': 1,
        'is_deleted': 0,
    }
    query_string = request.data.get('queryString', '')
    label = request.data.get('label', '')
    year = request.data.get('year', '')
    month = request.data.get('month', '')
    page_size = request.data.get('pageSize', 7)
    page_index = request.data.get('pageIndex', 1)

    if query_string:
        params['query_condition'] = (
            Q(title_cn__icontains=query_string)
            | Q(title_en__icontains=query_string)
            | Q(description__icontains=query_string)
        )

    if label:
        params[f'label_{label.lower()}'] = 1

    if year and month:
        params['date__year'] = year
        params['date__month'] = month

    query_condition = params.pop('query_condition', Q())
    records = GISource.objects.filter(query_condition, **params).order_by('-event_id')

    paginator = Paginator(records, page_size)
    page_content = paginator.page(page_index)
    serializer = GISourceSerializer(page_content, many=True)
    return Response({'code': 0, 'data': serializer.data, 'count': paginator.count})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_post_list(request):
    params = {
        'is_public': 1,
        'is_deleted': 0,
    }
    page_size = 10
    page_index = 1

    for key in request.GET:
        if key == 'pageSize':
            page_size = request.GET[key]
        elif key == 'pageIndex':
            page_index = request.GET[key]
        else:
            params[key] = request.GET[key]

    records = GISource.objects.filter(**params).order_by('-event_id')
    paginator = Paginator(records, page_size)
    page_content = paginator.page(page_index)
    serializer = GISourceSerializer(page_content, many=True)
    return Response({'code': 0, 'data': serializer.data, 'count': paginator.count})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def manage_get_post_list(request):
    params = {
        'is_deleted': 0,
    }
    page_size = 10
    page_index = 1

    for key in request.GET:
        if key == 'pageSize':
            page_size = request.GET[key]
        elif key == 'pageIndex':
            page_index = request.GET[key]
        else:
            params[key] = request.GET[key]

    records = GISource.objects.filter(**params).order_by('-event_id')
    paginator = Paginator(records, page_size)
    page_content = paginator.page(page_index)
    serializer = GISourceSerializer(page_content, many=True)
    return Response({'code': 0, 'data': serializer.data, 'count': paginator.count})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def manage_post(request, post_id):
    try:
        record = GISource.objects.get(event_id=post_id)
    except GISource.DoesNotExist:
        return JsonResponse({'code': 5, 'msg': 'no such post'})

    if request.method == 'GET':
        serializer = GISourceSerializer(record)
        return Response(serializer.data)

    if request.method == 'POST':
        body = json.loads(request.body)
        record_serializer = GISourceSerializer(record, data=body)
        if record_serializer.is_valid():
            record_serializer.save()
            return JsonResponse({'code': 0, 'msg': 'success'})
        logger.error(record_serializer.errors)
        return JsonResponse({'code': 500, 'msg': 'record_serializer not pass'})

    record.is_deleted = 1
    record.save()
    return JsonResponse({'code': 0, 'msg': 'success'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def manage_post_status(request):
    body = json.loads(request.body)
    record = GISource.objects.get(event_id=body['event_id'])
    record.is_public = body['is_public']
    record.save()
    return JsonResponse({'code': 0, 'msg': 'success'})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_post_by_id(request, post_id):
    if not post_id:
        return JsonResponse({'code': 2, 'msg': 'wrong post id'})

    records = GISource.objects.filter(event_id=post_id)
    if not records.exists():
        return JsonResponse({'code': 5, 'msg': 'no such post'})

    serializer = GISourceSerializer(records, many=True)
    if serializer.data[0]['is_public'] == 0:
        return JsonResponse({'code': 3, 'msg': 'post is not public'})
    if serializer.data[0]['is_deleted'] == 1:
        return JsonResponse({'code': 4, 'msg': 'post is deleted'})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def add_post(request):
    body = json.loads(request.body)
    key_flag = bool(body['title_cn']) | bool(body['title_en'])
    if not key_flag:
        return JsonResponse({'status': '400', 'msg': 'Please check the params'})

    GISource.objects.create(
        university_cn=body['university_cn'],
        university_en=body['university_en'],
        country_cn=body['country_cn'],
        country_en=body['country_en'],
        job_cn=body['job_cn'],
        job_en=body['job_en'],
        description=body['description'],
        title_cn=body['title_cn'],
        title_en=body['title_en'],
        label_physical_geo=body['label_physical_geo'],
        label_human_geo=body['label_human_geo'],
        label_urban=body['label_urban'],
        label_gis=body['label_gis'],
        label_rs=body['label_rs'],
        label_gnss=body['label_gnss'],
        date=body['date'],
        is_public=body['is_public'],
        is_deleted=body['is_deleted'],
    )
    return JsonResponse({'status': '200', 'msg': 'public post successfully!'})


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def send_proposal_email(request):
    try:
        category = request.data.get('category')
        content = request.data.get('content')
        user_email = request.data.get('email')
        uploaded_file = request.FILES.get('file')

        if not category or not content:
            return Response({'status': 'error', 'message': 'Category and content are required'}, status=400)

        category_map = {
            'school': '学校更新',
            'professor': '教授信息更新',
            'recruitment': '招生信息更新',
            'competition': '论文竞赛/会议信息',
        }
        category_text = category_map.get(category, category)

        subject = f'新的用户反馈 - {category_text}'
        body = f"收到新的用户反馈\n\n类别: {category_text}\n\n内容:\n{content}\n\n用户邮箱: {user_email}\n\n---\n系统自动发送"

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['gisphere@outlook.com'],
        )

        if uploaded_file:
            email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

        email.send(fail_silently=False)
        return Response({'status': 'success', 'message': '您的反馈已成功发送'})

    except Exception as exc:
        logger.error(f'Error sending proposal email: {str(exc)}')
        return Response({'status': 'error', 'message': f'发送失败: {str(exc)}'}, status=500)
