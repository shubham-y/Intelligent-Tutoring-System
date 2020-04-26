from django.contrib import admin
from django.urls import path
from expert import views

urlpatterns = [
    path('', views.login,name="login"),
    path('dashboard/', views.home1,name="home1"),
    path('add_user/', views.add_user,name="add_user"),
    path('add_subject/', views.add_subject,name="add_subject"),
    path('add_topic/', views.add_topic,name="add_topic"),
    path('add_questions/', views.add_questions,name="add_questions"),
]