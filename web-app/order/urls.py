from django.urls import path
from django.shortcuts import render
from . import views
import comments.views

urlpatterns =[
   # path('homepage/',views.homepage,name = 'homepage'),
    path('',views.checkorder,name = 'checkOrder'),
    path('<int:id>/makereview',comments.views.makereview, name = "makereview" ),
    path('<int:id>/readreview/',comments.views.readreview, name = 'readreview')
]