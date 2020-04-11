from django.urls import path, include
from . import views

urlpatterns = [
    path('cloth/stock/', views.stock, name='stock'),
    path('cloth/type/add/', views.addStock, name='addStock'),
    path('cloth/color/', views.color, name='color'),
    path('cloth/type/', views.cloth, name='cloth'),
]
