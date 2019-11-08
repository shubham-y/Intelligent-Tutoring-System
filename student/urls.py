from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('test/<int:ana_id>/<int:que_id>', views.test,name="test"),
    path('start_test/', views.start_test,name="start_test"),
    path('analyse/<int:sub_id>', views.analyse,name="analyse"),
]