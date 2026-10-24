from django.urls import path
from . import views

app_name="blog"

urlpatterns=[
    path('', views.blog_home,name="home"),
    path('single/<int:pk>/',views.blog_single,name="single"),
   
]