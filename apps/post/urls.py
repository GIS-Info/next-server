from django.urls import path
from apps.post import views as user_views
from . import views


urlpatterns = [
    # 对外开放的接口
    path('post', user_views.get_post_list, name = 'get_post_list'),
    path('post/<int:post_id>', user_views.get_post_by_id, name = 'get_post_by_id'),
    path('post/add/', user_views.add_post, name = 'add_post'),

    # 使用university的接口
    path('post/universities/', views.get_universities, name='get_universities'),
    path('post/cities/', views.get_cities, name='get_cities'),
    path('post/countries/', views.get_countries, name='get_countries'),

    # 这里querystring接口没有尾部url原因是改为了post请求以解决中文url乱码问题
    path('post_querystring', user_views.get_posts_by_querystring, name = 'get_posts_by_querystring'),
    path('post_closedate/', user_views.get_posts_by_enddate, name = 'get_posts_by_enddate'),

    # 对管理员开发的接口
    path('manage/post', user_views.manage_get_post_list, name = 'manage_get_post_list'), # GET: 管理员获取帖子列表
    path('manage/post/<int:post_id>', user_views.manage_post, name = 'manage_post'), # GET: 管理员获取帖子内容 POST: 管理员更新帖子内容 DELETE: 管理员删除帖子
    path('manage/post/status', user_views.manage_post_status, name = 'manage_post_status'), # POST: 管理员更新帖子 is_public 状态

    # 暂不使用的接口
    path('post_jobtitle/', user_views.get_posts_by_jobtitle, name = 'get_posts_by_jobtitle'),
    path('post_major/', user_views.get_posts_by_major, name = 'get_posts_by_major'),
    path('manage/delete/<int:post_id>', user_views.delete_post, name = 'delete_post'),

]
