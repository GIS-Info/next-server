from django.urls import path

from apps.post import views as user_views

urlpatterns = [
    path('post', user_views.get_post_list, name = 'get_post_list'),
    path('post/<int:post_id>', user_views.get_post_by_id, name = 'get_post_by_id'),
    path('post/add/', user_views.add_post, name = 'add_post'),
    #以下接口目前暂不使用
    path('manage/post/<int:post_id>', user_views.update_post, name = 'update_post'),
    path('manage/delete/<int:post_id>', user_views.delete_post, name = 'delete_post'),

    path('post_jobtitle/', user_views.get_posts_by_jobtitle, name = 'get_posts_by_jobtitle'),
    path('post_querystring/', user_views.get_posts_by_querystring, name = 'get_posts_by_querystring'),
    path('post_major/', user_views.get_posts_by_major, name = 'get_posts_by_major'),
    path('post_closedate/', user_views.get_posts_by_enddate, name = 'get_posts_by_enddate')
]