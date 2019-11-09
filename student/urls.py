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
]