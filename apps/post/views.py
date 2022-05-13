from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import GISource
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import EmptyPage, Paginator

from .serializer import GISourceSerializer

# Create your views here.
@api_view(['GET'])
def get_post_list(request):
    """
        Get all the posts with given settings
        e.g.
        http://127.0.0.1:8000/api/post?pageSize=2&pageIndex=3&jobTitle=postdoc&country=100&label=GIS&queryString=geography
    """
    if request.method == "GET":

        key_flag = len(request.GET['pageSize']) & len(request.GET['pageIndex']) & len(request.GET['jobTitle']) \
                   & len(request.GET['country']) & len(request.GET['label']) & len(request.GET['queryString'])
        #
        if key_flag:
            pageSize = request.GET['pageSize'] # 有package
            pageIndex = request.GET['pageIndex']
            jobTitle = request.GET['jobTitle'] #job title char
            country = request.GET['country'] #country_id
            # closeDate = request.GET['closeDate'] # 最后被创建的时间
            label = request.GET['label']
            queryString = request.GET['queryString']

            # 处理时间的格式, python Date 对象 --> 这部分是测试

            # Get dataset --> 如果确定好获取的参数，就可以用这一部分，将filter中的参数替换成上面的, 需要检查下下面的类型是否对应, 需要进一步测试
            record = GISource.objects.filter(
                country = country
            )
            paginator = Paginator(record, pageSize)
            page_content = paginator.page(pageIndex)
            serializer = GISourceSerializer(page_content, many=True)
            print(serializer.data)
            # return JsonResponse({"pageSize": pageSize, "pageIndex": pageIndex,
            #                      "job": jobTitle, "country": country,
            #                      "label": label, "queryString": queryString
            #                      })
            return Response(serializer.data)

@api_view(['GET'])
def get_post_by_id(request, post_id):
    """Read: Get a post with given event_id

    e.g. http://127.0.0.1:8000/api/post/2

    """
    if request.method == 'GET':
        # key_flag = len(request.GET['eventID'])
        # if key_flag:
        #     record = GISource.objects.filter(event_id=post_id)
        #     serializer = GISourceSerializer(record, many=True)
        if post_id:
            record = GISource.objects.filter(event_id=post_id)
            serializer = GISourceSerializer(record, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"code": 0, "msg": "wrong post id"})

@api_view(['POST'])
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
def add_post(request):
    """Create: Add new post
    api/manage/post
    e.g.
    http://127.0.0.1:8000/api/manage/add/post
    Request body:
    jobTitle: Test job title
    country: 1001
    """
    if request.method == "POST":
        key_flag = len(request.POST["jobTitle"]) | len(request.POST['country'])

        if key_flag:
            job_title = request.POST['jobTitle']
            country = request.POST['country']

            # Insert the new post
            # added_post = GISource(job_title = job_title, country = country)
            GISource.objects.create(job_title=job_title, country = country)
            return JsonResponse({"status": "200", "msg": "public post successfully!"})
    else:
        return JsonResponse({"status": "400", "msg": "Please check the params"})





