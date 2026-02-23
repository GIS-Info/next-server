import json
import logging

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger('django')

# from django.core import serializers
# from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
# from django.http import HttpResponse
from django.http import JsonResponse
# from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .models import GISource
from .serializer import GISourceSerializer
#使用Q对象来组合多个查询条件
from django.db.models import Q

# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_posts_by_params(request):
    """
    Get posts based on various parameters. 统一搜索接口,优化用户体验.

    Examples:
    - http://127.0.0.1:8000/api/postList?queryString=example&pageSize=10&pageIndex=1
    - http://127.0.0.1:8000/api/postList?label=GIS&pageSize=10&pageIndex=1
    - http://127.0.0.1:8000/api/postList?year=2022&month=5&pageSize=10&pageIndex=1
    - http://127.0.0.1:8000/api/postList?pageSize=10&pageIndex=1&is_public=1&is_deleted=0
    """
    if request.method == 'POST':
        # 构造params用于筛选
        params = {
            'is_public': 1,
            'is_deleted': 0,
        }
        print(request)
        queryString = request.data.get('queryString', '')
        label = request.data.get('label', '')
        year = request.data.get('year', '')
        month = request.data.get('month', '')
        pageSize = request.data.get('pageSize', 7)
        pageIndex = request.data.get('pageIndex', 1)
        
        if queryString:
            params.update({
                'query_condition': (
                    Q(title_cn__icontains=queryString) |
                    Q(title_en__icontains=queryString) |
                    Q(description__icontains=queryString)
                )
            })

        if label:
            params.update({f'label_{label.lower()}': 1})

        if year and month:
            params.update({
                'date__year': year,
                'date__month': month,
            })

        query_condition = params.pop('query_condition', Q())  # 获取并移除 query_condition
        records = GISource.objects.filter(query_condition, **params).order_by('-event_id')

        paginator = Paginator(records, pageSize)
        page_content = paginator.page(pageIndex)
        count = paginator.count
        serializer = GISourceSerializer(page_content, many=True)
        
        return Response({"code": 0, "data": serializer.data, "count": count})
    else:
        return JsonResponse({"code": 1, "msg": "Invalid request method."})

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_post_list(request):
    """
        Get all the posts with given settings
        e.g.
        http://127.0.0.1:8000/api/post?pageSize=2&pageIndex=1
        http://127.0.0.1:8000/api/post?pageSize=2&pageIndex=1&job_title=phd&country=100

    """
    if request.method == "GET":
        params = {
            'is_public': 1,
            'is_deleted': 0,
        }
        pageSize = 10
        pageIndex = 1

        for key in request.GET:
            if key == 'pageSize':
                pageSize = request.GET[key]
            elif key == 'pageIndex':
                pageIndex = request.GET[key]
            else:
                params[key] = request.GET[key]
        if params:
            record = GISource.objects.filter(**params).order_by('-event_id')
        else:
            record = GISource.objects.all().order_by('-event_id')

        paginator = Paginator(record, pageSize)
        page_content = paginator.page(pageIndex)
        # 条数，用于前端显示页码
        count = paginator.count
        serializer = GISourceSerializer(page_content, many=True)
        # print(serializer.data)
        return Response({"code": 0, "data": serializer.data, "count": count})
    else:
        return JsonResponse({"code": 1, "msg": "wrong request method"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def manage_get_post_list(request):
    if request.method == "GET":
        params = {
            'is_deleted': 0,
        }
        pageSize = 10
        pageIndex = 1

        for key in request.GET:
            if key == 'pageSize':
                pageSize = request.GET[key]
            elif key == 'pageIndex':
                pageIndex = request.GET[key]
            else:
                params[key] = request.GET[key]
        if params:
            record = GISource.objects.filter(**params).order_by('-event_id')
        else:
            record = GISource.objects.all().order_by('-event_id')

        paginator = Paginator(record, pageSize)
        page_content = paginator.page(pageIndex)
        # 条数，用于前端显示页码
        count = paginator.count
        serializer = GISourceSerializer(page_content, many=True)
        return Response({"code": 0, "data": serializer.data, "count": count})
    else:
        return JsonResponse({"code": 1, "msg": "wrong request method"})


# GET: 管理员获取帖子内容
# POST: 管理员更新帖子内容 
# DELETE: 管理员删除帖子
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def manage_post(request, post_id):
    try:
        record = GISource.objects.get(event_id=post_id)
    except:
        return JsonResponse({"code": 5, "msg": "no such post"})
    if request.method == 'GET':
        serializer = GISourceSerializer(record)
        return Response(serializer.data)
    elif request.method == 'POST':
        body = json.loads(request.body)
        record_serializer = GISourceSerializer(record, data=body)
        if record_serializer.is_valid():
            record_serializer.save()
            return JsonResponse({"code": 0, "msg": "success"})
        logger.error(record_serializer.errors)
        return JsonResponse({"code": 500, "msg": 'record_serializer not pass'})
    elif request.method == 'DELETE':
        record.is_deleted = 1
        record.save()
        return JsonResponse({"code": 0, "msg": "success"})
    else:
        return JsonResponse({"code": 1, "msg": "wrong request method"})


# POST: 管理员改变帖子开放状态，即 is_public 字段值
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def manage_post_status(request):
    body = json.loads(request.body)
    event_id = body['event_id']
    record = GISource.objects.get(event_id=event_id)
    record.is_public = body['is_public']
    record.save()
    return JsonResponse({"code": 0, "msg": "success"})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_post_by_id(request, post_id):
    """Read: Get a post with given event_id

    e.g. http://127.0.0.1:8000/api/post/2

    """
    if request.method == 'GET':
        if post_id:
            record = GISource.objects.filter(event_id=post_id)
            serializer = GISourceSerializer(record, many=True)
            if serializer.data[0]['is_public'] == 0:
                return JsonResponse({"code": 3, "msg": "post is not public"})
            elif serializer.data[0]['is_deleted'] == 1:
                return JsonResponse({"code": 4, "msg": "post is deleted"})
            else:
                return Response(serializer.data)
        else:
            return JsonResponse({"code": 2, "msg": "wrong post id"})


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def add_post(request):
    """Create: Add new post
    api/post/add
    e.g.
    http://127.0.0.1:8000/api/post/add
    Request body:
    jobTitle: Test job title
    country: 1001
    """
    if request.method == "POST":
        body = json.loads(request.body)
        key_flag = bool(body["title_cn"]) | bool(body["title_en"])
        if key_flag:
            university_cn = body['university_cn']
            university_en = body['university_en']
            country_cn = body['country_cn']
            country_en = body['country_en']
            job_cn = body['job_cn']
            job_en = body['job_en']
            description = body['description']
            title_cn = body['title_cn']
            title_en = body['title_en']
            label_physical_geo = body['label_physical_geo']
            label_human_geo = body['label_human_geo']
            label_urban = body['label_urban']
            label_gis = body['label_gis']
            label_rs = body['label_rs']
            label_gnss = body['label_gnss']
            date = body['date']
            is_public = body['is_public']
            is_deleted = body['is_deleted']

            # Insert the new post
            # added_post = GISource(job_title = job_title, country = country)
            GISource.objects.create(university_cn=university_cn, university_en=university_en, country_cn=country_cn,
                                    country_en=country_en, job_cn=job_cn, job_en=job_en, description=description,
                                    title_cn=title_cn, title_en=title_en, label_physical_geo=label_physical_geo,
                                    label_human_geo=label_human_geo, label_urban=label_urban, label_gis=label_gis,
                                    label_rs=label_rs, label_gnss=label_gnss, date=date, is_public=is_public, is_deleted=is_deleted)
            return JsonResponse({"status": "200", "msg": "public post successfully!"})
        else:
            return JsonResponse({"status": "400", "msg": "Please check the params"})
    else:
        return JsonResponse({"status": "400", "msg": "Please check the params"})

from django.core.mail import EmailMessage
from django.conf import settings
@api_view(['POST'])
@permission_classes((AllowAny,))

def send_proposal_email(request):
    try:
        # 1. 获取文字字段
        category = request.data.get('category')
        content = request.data.get('content')
        user_email = request.data.get('email')  # 对应你在前端新增的 email 字段
        
        # 2. 获取上传的文件对象 (这里的 'file' 必须和前端 formData 的 key 一致)
        uploaded_file = request.FILES.get('file')

        if not category or not content:
            return Response({'status': 'error', 'message': 'Category and content are required'}, status=400)

        category_map = {
            'school': '学校更新',
            'professor': '教授信息更新',
            'recruitment': '招生信息更新',
            'competition': '论文竞赛/会议信息'
        }
        category_text = category_map.get(category, category)

        # 3. 准备邮件元数据
        subject = f'新的用户反馈 - {category_text}'
        body = f"收到新的用户反馈\n\n类别: {category_text}\n\n内容:\n{content}\n\n用户邮箱: {user_email}\n\n---\n系统自动发送"

        # 4. 创建 EmailMessage 实例
        # 注意：这里参数名是 to，接收的是列表
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['gisphere@outlook.com'],
        )

        # 5. 关键步骤：如果用户上传了文件，将其挂载为附件
        if uploaded_file:
            # attach 接收三个参数: 文件名, 文件二进制内容, MIME类型
            email.attach(
                uploaded_file.name, 
                uploaded_file.read(), 
                uploaded_file.content_type
            )

        # 6. 发送邮件
        email.send(fail_silently=False)

        return Response({
            'status': 'success',
            'message': '您的反馈已成功发送'
        })

    except Exception as e:
        # logger 这里需要确保你在文件开头已经定义过了
        logger.error(f'Error sending proposal email: {str(e)}')
        return Response({
            'status': 'error',
            'message': f'发送失败: {str(e)}'
        }, status=500)
