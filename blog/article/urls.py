from django.contrib import admin
from django.urls import path
from . import views

app_name = "article"

urlpatterns=[
    path('dashbord',views.dashbord,name='dashbord'),
    path('addarticle',views.addarticle,name='addarticle'),
    path('article/<int:id>', views.detail , name='detail'),
    path('update/<int:id>', views.updateArticle , name='updateArticle'),
    path('delete/<int:id>', views.deleteArticle , name='deleteArticle'),
    path('', views.articles , name='articles'),

]

