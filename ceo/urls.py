from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ceo/graph/', views.graph, name='graph'),
    path('ceo/sendAPI/<name>/', views.clothList, name='clothList'),
]
