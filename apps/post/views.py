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

from .models import GISource, NewUniversity,Cities,Countries
from .serializer import UniversitySerializer, GISourceSerializer,CitySerializer
from .serializer import UniCitySerializer,CountrySerializer
from django.db import connection


# Create your views here.
@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_posts_by_jobtitle(request):
    """
    Get all the posts with selected job title

    e.g.
     http://127.0.0.1:8000/api/post_jobtitle?jobTitle=phd
    """
    if request.method == "GET":
        if len(request.GET['jobTitle']):
            jobTitle = request.GET['jobTitle']
            pageSize = 10
            pageIndex = 1

            if 'pageSize' in request.GET:
                pageSize = request.GET['pageSize']
            if 'pageIndex' in request.GET:
                pageIndex = request.GET['pageIndex']

            record = GISource.objects.filter(
                job_title=jobTitle
            )
            paginator = Paginator(record, pageSize)
            page_content = paginator.page(pageIndex)
            serializer = GISourceSerializer(page_content, many=True)
            print(serializer.data)

            return Response(serializer.data)
        else:
            return JsonResponse({"status": "1", "msg": "Please check the params"})
    else:
        return JsonResponse({"status": "0", "msg": "Please check the request method"})


# change get request to post
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_posts_by_querystring(request):
    """
        Get all the posts with selected country or university

        e.g.
        Query by country:
        http://127.0.0.1:8000/api/post_querystring

        Query by university:
        http://127.0.0.1:8000/api/post_querystring

        """
    if request.method == "POST":
        queryString = request.data.get('queryString', '')
        pageSize = request.data.get('pageSize', 10)
        pageIndex = request.data.get('pageIndex', 1)

        record = GISource.objects.filter(
            title_cn__icontains=queryString,
            is_public=1,
            is_deleted=0
        ).union(GISource.objects.filter(
            title_cn__icontains=queryString,
            is_public=1,
            is_deleted=0
        )).order_by('-date')
        paginator = Paginator(record, pageSize)
        page_content = paginator.page(pageIndex)
        count = paginator.count
        serializer = GISourceSerializer(page_content, many=True)

        return Response({"code": 0, "data": serializer.data, "count": count})
    else:
        return JsonResponse({"status": "0", "msg": "Please check the request method"})

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_posts_by_major(request):
    """
            Get all the posts by major

            e.g.
            http://127.0.0.1:8000/api/post_major?label=GIS

            """
    if request.method == "GET":
        if len(request.GET['label']):
            major = request.GET['label']
            pageSize = 10
            pageIndex = 1

            if 'pageSize' in request.GET:
                pageSize = request.GET['pageSize']
            if 'pageIndex' in request.GET:
                pageIndex = request.GET['pageIndex']

            record = GISource.objects.filter(
                label__contains=major
            )
            paginator = Paginator(record, pageSize)
            page_content = paginator.page(pageIndex)
            serializer = GISourceSerializer(page_content, many=True)
            print(serializer.data)

            return Response(serializer.data)
        else:
            return JsonResponse({"status": "1", "msg": "Please check the params"})
    else:
        return JsonResponse({"status": "0", "msg": "Please check the request method"})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_posts_by_enddate(request):
    """
    Get post by closed date
    e.g.
    http://127.0.0.1:8000/api/post_closedate?year=2022&month=5
    """
    if request.method == "GET":
        if len(request.GET['year']):
            if len(request.GET['month']):
                year = request.GET['year']
                month = request.GET['month']  # should be 01, 02, ...10, 11, 12
                print(year)
                print(month)
                # year_month = year + "-" + month

                pageSize = 10
                pageIndex = 1

                if 'pageSize' in request.GET:
                    pageSize = request.GET['pageSize']
                if 'pageIndex' in request.GET:
                    pageIndex = request.GET['pageIndex']

                record = GISource.objects.filter(
                    # close_date__year = year,
                    # close_date__month = month
                    date__year=year,
                    date__month=month,
                    is_public=1,
                    is_deleted=0
                ).order_by('-date')
                paginator = Paginator(record, pageSize)
                page_content = paginator.page(pageIndex)
                count = paginator.count
                serializer = GISourceSerializer(page_content, many=True)

                return Response({"code": 0, "data": serializer.data, "count": count})
        else:
            return JsonResponse({"code": 1, "msg": "wrong request method"})


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
        logger.error('1')
        if record_serializer.is_valid():
            logger.error('2')
            record_serializer.save()
            logger.error('3')
            return JsonResponse({"code": 0, "msg": "success"})
        logger.error('4')
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


# this is deprecated
@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_post_list_deprecated(request):
    """
        Get all the posts with given settings
        e.g.
        http://127.0.0.1:8000/api/post?pageSize=2&pageIndex=1&jobTitle=postdoc&country=100&label=GIS&queryString=geography
        http://127.0.0.1:8000/api/post?pageSize=2&pageIndex=1&jobTitle=phd&country=100&label=GIS&queryString=geography

    """
    if request.method == "GET":
        key_flag = len(request.GET['pageSize']) & len(request.GET['pageIndex']) & len(request.GET['jobTitle']) \
                   & len(request.GET['country']) & len(request.GET['label']) & len(request.GET['queryString'])

        if key_flag:
            pageSize = request.GET['pageSize']  # 有package
            pageIndex = request.GET['pageIndex']
            jobTitle = request.GET['jobTitle']  # job title char
            country = request.GET['country']  # country_id
            # closeDate = request.GET['closeDate'] # 最后被创建的时间
            label = request.GET['label']
            queryString = request.GET['queryString']

            # 处理时间的格式, python Date 对象 --> 这部分是测试

            # Get dataset --> 如果确定好获取的参数，就可以用这一部分，将filter中的参数替换成上面的, 需要检查下下面的类型是否对应, 需要进一步测试
            record = GISource.objects.filter(
                country=country,
                job_title=jobTitle
            )
            paginator = Paginator(record, pageSize)
            page_content = paginator.page(pageIndex)
            serializer = GISourceSerializer(page_content, many=True)
            print(serializer.data)
            return Response(serializer.data)


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
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def update_post(request, post_id):
    """Update: update the post content
    api/manage/post/<post_id>

    e.g. http://127.0.0.1:8000/api/manage/post/2
    Request body:
        jobTitle = postdoc
        country = 100
    """

    # Django 基于不同的请求用不同的函数
    if request.method == "POST":
        print("yes the request method is post")
        if post_id:
            post = GISource.objects.get(event_id=post_id)
            print(post.job_title)

        if post:
            key_flag = len(request.POST["jobTitle"]) | len(request.POST['country'])
            if key_flag:
                job_title = request.POST['jobTitle']
                country = request.POST['country']
                if job_title:
                    post.job_title = job_title
                if country:
                    post.country = country
                post.save()
                print(post.job_title, post.country)
                return JsonResponse({"status": "200", "msg": "Update the post successfully!"})
            else:
                return JsonResponse({"status": "300", "msg": "Did not pass the parameters..."})
        else:
            return JsonResponse({"status": "300", "msg": "Post is not existed, fail to update.."})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def delete_post(request, post_id):
    """
    e.g. http://127.0.0.1:8000/api/manage/delete/44
    """
    if request.method == "DELETE":
        print("post id is ", post_id)
        post = GISource.objects.get(event_id=post_id)
        print(post.job_title)
        if post:
            post.delete()
            return JsonResponse({"status": "200", "msg": "Delete the post successfully!"})
        else:
            return JsonResponse({"status": "300", "msg": "Post doesnot exist, fail to delete"})


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

@api_view(['GET'])
def get_universities(request):
    universities = NewUniversity.objects.all()
    serializer = UniversitySerializer(universities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_cities(request):
    cities = Cities.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_countries(request):
    countries = Countries.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_continent_data(request, continent):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM new_Universities u 
            JOIN new_city c ON u.City = c.City_Name_EN
            JOIN new_country co ON c.Country = co.Country_Name_CN
            WHERE co.Continent = %s
        """, [continent])
        rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            'University_Name_CN': row[0],
            'University_Name_EN': row[1],
            'University_Name_Local': row[2],
            'City': row[3],
            'URL': row[4],
            'University_Abbr': row[5],
            'University_Other_Name': row[6],
            'Description_CN': row[7],
            'Description_EN': row[8],
            'Unit_CN': row[9],
            'Unit_EN': row[10],
            'id': row[13],
            'Country': row[16],
        })

    return Response(data)

@api_view(['GET'])
def get_country_data(request, country):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM new_Universities u 
            JOIN new_city c ON u.City = c.City_Name_EN
            JOIN new_country co ON c.Country = co.Country_Name_CN
            WHERE co.Country_Name_CN = %s
        """, [country])
        rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            'University_Name_CN': row[0],
            'University_Name_EN': row[1],
            'University_Name_Local': row[2],
            'City': row[3],
            'URL': row[4],
            'University_Abbr': row[5],
            'University_Other_Name': row[6],
            'Description_CN': row[7],
            'Description_EN': row[8],
            'Unit_CN': row[9],
            'Unit_EN': row[10],
            'id': row[13],
            'Country': row[16],
        })

    return Response(data)