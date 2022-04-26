from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import GISource
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import GISourceSerializer

# Create your views here.
@api_view(['GET'])
def get_post_list(request):
    """
        Get all the posts with given settings
    """
    # return HttpResponse("hello world this is the test")
    if request.method == "GET":
        # req = json.loads(request.body)
        # key_flag = len(request.GET['pageSize']) & len(request.GET['pageIndex']) & len(request.GET['job']) \
        #            & len(request.GET['country']) & len(request.GET['term']) & len(request.GET['tag']) \
        #            & len(request.GET['endMonth']) & len(request.GET['queryString'])
        # key_flag = request.GET['eventID']
        # print("key_flag: ")
        # record = GISource.objects.filter(event_id=key_flag)
        # serializer = GISourceSerializer(record, many=True)
        # print(serializer.data)
        # return JsonResponse({"code": key_flag})
        key_flag = len(request.GET['pageSize']) & len(request.GET['pageIndex']) & len(request.GET['job']) \
                   & len(request.GET['country']) & len(request.GET['term']) & len(request.GET['tag']) \
                   & len(request.GET['queryString'])
        #
        if key_flag:
            pageSize = request.GET['pageSize'] # 有package
            pageIndex = request.GET['pageIndex']
            job = request.GET['job']
            country = request.GET['country']
            term = request.GET['term']
            tag = request.GET['tag']
            endMonth = request.GET['endMonth'] # 最后被创建的时间
            queryString = request.GET['queryString']

            # 处理时间的格式, python Date 对象

            return JsonResponse({"pageSize": pageSize, "pageIndex": pageIndex, "job": job, "endMonth": endMonth,
                                 "country": country, "term": term, "tag": tag,
                                 "queryString": queryString})


            # Get dataset
            # record = GISource.objects.filter(event_id=event_id)
            # serializer = GISourceSerializer(record, many=True)
            # return Response(serializer.data)

@api_view(['GET'])
def get_post_by_id(request, post_id):
    """Read: Get a post with given event_id"""
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

# @api_view(['POST'])
def update_post(request, post_id):
    """Update: update the post content OR delete the post
    api/manage/post/<post_id>
    """

    # Django 基于不同的请求用不同的函数
    if request.method == "POST":
        if post_id:
            post = GISource.objects.get(event_id=post_id)

        key_flag = len(request.GET["job"]) | len(request.GET['country']) | len(request.GET['term']) \
                    | len(request.GET['tag'])
        try:
            if key_flag & post:
                job = request.GET['job']
                country = request.GET['country']
                term = request.GET['term']
                tag = request.GET['tag']
                # endMonth = request.GET['endMonth']
                # queryString = request.GET['queryString']

                if job:
                    post.job = job
                if country:
                    post.country = country
                if term:
                    post.term = term
                if tag:
                    post.tag = tag
                post.save()
                return JsonResponse({"status": "200", "msg": "Update the post successfully!"})
        except:
            return JsonResponse({"status": "300", "msg": "Post is not existed, fail to update.."})

    """Delete: delete the post"""
    if request.method == "DELETE":
        try:
            post = GISource.objects.get(event_id=post_id)
            post.delete()
            return JsonResponse({"status": "200", "msg": "Delete the post successfully!"})
        except:
            return JsonResponse({"status": "300", "msg": "Post doesnot exist, fail to delete"})

@api_view(['POST'])
def add_post(request):
    """Create: Add new post
    api/manage/post
    """
    if request.method == "POST":
        key_flag = len(request.GET["job"]) | len(request.GET['country']) | len(request.GET['term']) \
                   | len(request.GET['tag'])

        if key_flag:
            job = request.GET['job']
            country = request.GET['country']
            term = request.GET['term']
            tag = request.GET['tag']

            # Insert the new post
            added_post = GISource(job = job, country = country, term = term, tag = tag)
            added_post.save()
            return JsonResponse({"status": "200", "msg": "public post successfully!"})
    else:
        return JsonResponse({"status": "400", "msg": "Please check the params"})





