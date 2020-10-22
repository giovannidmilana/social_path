"""Defines url patterns for users."""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

from django.contrib import admin 
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *

from django.conf.urls import url



app_name = 'users'
urlpatterns = [
    # Login page
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    path('search/', SearchResultsView.as_view(), name='search_results'),
    #path('', views.disp_post, name='disp_post'),
    #
    path('disp_post/', views.disp_post, name='disp_post'),
    #path('<int:post_id>/', views.disp_post, name='disp_post'),
    path('create_profile/', views.create_profile, name='create_profile'),
    #path('login/', views.login, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Logout page
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Registration page.
    #path('profiles_tm/<int:user_id>/', views.messaging, name='messaging'),
    #path('profiles_tm/<slug:user_id>/', views.messaging, name='messaging'),
    #path('messaging/', views.messaging, name='messaging'),   
    path('messaging/<int:user_id>/', views.messaging, name='messaging'),
    path('register/', views.register, name='register'),
    #path('image_upload/', profile_photo_view, name ='image_upload'), 
    path('profile/', profile_edit_view, name='profile_edit_view'),
    #
    path('profiles_tm/', views.profiles_tm, name ='profiles_tm'),
    path('user_post/', user_post, name='user_post'),
    path('profile_edit/', profile_edit_view, name='profile_edit_view'),
    path('profile_photo_edit/', edit_profile_photo, name='edit_profile_photo'),
      
      
    path('<int:user_id><int:chat_id>/', views.send_message, name='send_message'),
    path('messages/', views.messages, name='messages'),
    #path('search/', SearchResultsView.as_view(), name='search_results'),
    #path('search/', views.search, name='search'), 
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    #path('disp_post/<int:post_id>/', views.post, name='post'),
    #path('disp_post/', views.user_post, name='user_post'),
    #path('disp_post/<int:post_id>/', views.user_post, name='user_post'),
    #path('disp_post/<int:post_id>/', views.new_comment, name='new_comment'),
    path('<int:post_id>/', views.delete_post, name='delete_post'),
    path('new_comment/<int:post_id>/', views.new_comment, name='new_comment'),
    #path('new_comment/<int:post_id>/', views.post, name='post'),
    path('profile_user/', views.profile_user, name='profile_user'), 
    path('profiles_tm/<int:user_id>/', views.profile_user, name='profile_user'),
    path('index/<int:user_id>/', views.profile_user, name='profile_user'), 
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
