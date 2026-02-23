from django.urls import path
from apps.post import views as user_views


urlpatterns = [
    # 对外开放的接口
    path('post', user_views.get_post_list, name = 'get_post_list'),
    path('post/<int:post_id>', user_views.get_post_by_id, name = 'get_post_by_id'),
    path('post/add/', user_views.add_post, name = 'add_post'),

    # 帖子搜索的接口
    path('post_by_params', user_views.get_posts_by_params, name = 'get_posts_by_params'),

    # 用户反馈邮件发送接口
    path('send-proposal/', user_views.send_proposal_email, name='send-proposal-email'),

    # 对管理员开发的接口
    path('manage/post', user_views.manage_get_post_list, name = 'manage_get_post_list'), # GET: 管理员获取帖子列表
    path('manage/post/<int:post_id>', user_views.manage_post, name = 'manage_post'), # GET: 管理员获取帖子内容 POST: 管理员更新帖子内容 DELETE: 管理员删除帖子
    path('manage/post/status', user_views.manage_post_status, name = 'manage_post_status'), # POST: 管理员更新帖子 is_public 状态
]
