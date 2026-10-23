from django.contrib import admin
from django.urls import path
from blog.views import *

app_name="blog"

urlpatterns=[
    path('',blog_home,name="home"),
    path('single/<int:pk>/',blog_single,name="single"),
   
]