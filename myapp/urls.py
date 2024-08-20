from django.urls import path
from . import views  # 뷰를 가져옵니다
from .views import video_list


urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지
    path('community/', views.community, name='community'),  # 커뮤니티 페이지
    path('videos/', views.video_list, name='videos'),  # 비디오 페이지
    path('community/', views.community, name='community'),
    path('community/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('community/post/new/', views.post_create, name='post_create'),
    path('community/post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('community/post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('community/post/<int:pk>/like/', views.post_like, name='post_like'),
    path('community/post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('videos/', views.video_list, name='videos'),
    path('search/', views.search_results, name='search_results'),
    path('fighter/<int:fighter_id>/', views.fighter_detail, name='fighter_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('videos/', video_list, name='video_list'),
    path('upcoming/', views.upcoming_events, name='upcoming_events'),
    path('vote/<int:match_id>/', views.vote_match, name='vote_match'),
]
