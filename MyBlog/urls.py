"""
URL configuration for MyBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views as blog_views
from django.conf.urls import handler404

handler404 = 'blog.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 用户认证相关URL - 确保完全一致
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # 密码重置URL - 特别检查这些
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset.html',
             email_template_name='blog/password_reset_email.html',  # 邮件模板
             subject_template_name='blog/password_reset_subject.txt'  # 邮件主题模板
         ),
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # 自定义用户认证视图
    path('register/', blog_views.register, name='register'),
    path('profile/', blog_views.profile, name='profile'),
    
    # 博客页面
    path('', include('blog.urls')),
]