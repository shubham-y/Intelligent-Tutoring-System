from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name="login"),
    path('login_action/', views.login_action,name="login_action"),
    path('register/', views.register,name="register"),
    path('register_action/', views.register_action,name="register_action"),
    path('logout/', views.logout,name="logout"),
    path('home',views.home,name="home"),
    path('test/<int:ana_id>/<int:que_id>', views.test,name="test"),
    path('start_test/', views.start_test,name="start_test"),
    path('analyse/<int:sub_id>', views.analyse,name="analyse"),
    path('ajax/load_action/', views.ajax_load_action, name='ajax_load_action'),
    path('start_test2/', views.start_test2,name="start_test2"),
    path('test2/<int:sub_id>/<int:top_id>', views.test2,name="test2"),
    path('forum/', views.forum,name="forum"),
    path('forum_add/', views.forum_add,name="forum_add"),
    path('forum_topic/', views.forum_topic,name="forum_topic"),
]