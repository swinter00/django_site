from django.urls import path, reverse_lazy
from . import views

app_name='jamup'
urlpatterns = [
    path('', views.PostListView.as_view()),
    path('jamup', views.PostListView.as_view(), name='all'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create',
        views.PostCreateView.as_view(success_url=reverse_lazy('jamup:all')), name='post_create'),
    path('post/<int:pk>/update',
        views.PostUpdateView.as_view(success_url=reverse_lazy('jamup:all')), name='post_update'),
    path('post/<int:pk>/delete',
        views.PostDeleteView.as_view(success_url=reverse_lazy('jamup:all')), name='post_delete'),
    path('post/<int:pk>/reply',
        views.ReplyCreateView.as_view(), name='post_reply_create'),
    path('reply/<int:pk>/delete',
        views.ReplyDeleteView.as_view(success_url=reverse_lazy('jamup:all')), name='post_reply_delete'),
    path('jamup/profiles', views.ProfileListView.as_view(), name='all_profiles'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/create',
        views.ProfileCreateView.as_view(success_url=reverse_lazy('jamup:all_profiles')), name='profile_create'),
    path('profile/<int:pk>/update',
        views.ProfileUpdateView.as_view(success_url=reverse_lazy('jamup:all_profiles')), name='profile_update'),
    path('profile/<int:pk>/delete',
        views.ProfileDeleteView.as_view(success_url=reverse_lazy('jamup:all')), name='profile_delete'),
    path('profile_picture/<int:pk>', views.stream_file, name='profile_picture'),
    path('jamup/messages', views.MessageListView.as_view(), name='my_messages'),
    path('message/create',
        views.MessageCreateView.as_view(success_url=reverse_lazy('jamup:my_messages')), name='message_create'),
    path('message/<int:pk>/delete',
        views.MessageDeleteView.as_view(success_url=reverse_lazy('jamup:my_messages')), name='message_delete'),
]