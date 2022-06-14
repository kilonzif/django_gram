from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

from . import views



urlpatterns = [
    path('', views.home),
    path('add_post/',views.add_post,name='add_post'),
    
    path('view_post/<int:post_id>/', views.view_post, name='view_post'),
    
    path('add_post_comment/<int:post_id>',views.add_post_comment,name='add_post_comment'),
    path('like_post/<int:post_id>',views.like_post,name='like_post'),
    
    path('register/',views.register),
    path('login/',views.signin),
    path('signout/',views.signout),
    
    path('profile/',views.profile),
    
    path('user_profile/<int:id>', views.user_profile, name="user_profile")
    
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
