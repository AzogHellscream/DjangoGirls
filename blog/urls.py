from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('login/', views.user_login, name='user_login'),
    path('auth/', views.register, name='register'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('top10/', views.top_ten_tags, name='top_ten_tags'),
    path('api/v1/postlist/', views.PostAPIView.as_view(), name='PostAPIView'),
]
