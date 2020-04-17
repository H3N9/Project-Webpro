from django.urls import path, include
from . import views

urlpatterns = [
    path('cloth/stock/', views.stock, name='stock'),
    path('cloth/stock/add/', views.addStock, name='addStock'),
    path('cloth/color/', views.color, name='color'),
    path('cloth/type/', views.cloth, name='cloth'),
    path('cloth/type/add/', views.clothAdd, name='clothAdd'),
    path('cloth/type/edit/<int:cid>/', views.clothEdit, name='clothEdit'),
    path('cloth/color/edit/<int:cid>/', views.colorEdit, name='colorEdit'),
    path('cloth/color/add/', views.colorAdd, name='colorAdd'),
    path('cloth/stock/edit/<int:sid>/', views.stockEdit, name='stockEdit'),
]
