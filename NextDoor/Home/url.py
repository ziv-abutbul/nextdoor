from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('home/map', views.map, name='map'),
    path('search/', views.search, name="search"),
    path('AbutUs/', views.AbutUs, name="AbutUs"),
]
