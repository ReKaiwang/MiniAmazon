from django.urls import path
from django.shortcuts import render
from . import views
from django.views.generic.base import TemplateView

urlpatterns =[
   # path('homepage/',views.homepage,name = 'homepage'),
    path('',views.browsePro,name = 'browsePro'),
    path('success/', views.resultsView, name='addcartsuccess'),
    path('productlist/',views.showProList, name = 'productlist')
]