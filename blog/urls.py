from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('login/', views.user_login, name='user_login'),
    path('auth/', views.register, name='register'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('logout/', views.logout_view, name='logout_view'),
    path('logout/', include('django.contrib.auth.urls')), # copy worked, but redirect in web-interface
    # url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
]
