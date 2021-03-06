from django.urls import path
from . import views

urlpatterns = [
    path('employee/', views.showEmployee, name='showEmployee'),
    path('employee/add/', views.addEmployee, name='addEmployee'),
    path('employee/detail/<int:eid>/', views.detail, name='detail'),
    path('employee/delete/<int:eid>/', views.deleteEmployee, name='deleteEmployee'),
    path('employee/add/time/<int:eid>/', views.addTime, name='addTime'),
    path('employee/paid_salary/<int:eid>/', views.paidSalary, name='paidSalary'),
    path('account/', views.account, name='account'),
    path('account/expense/', views.expense, name='expense'),
    path('account/revenue/', views.revenue, name='revenue'),
    path('customer/', views.customer, name='customer'),
    path('customer/add/', views.addCustomer, name='addCustomer'),
    path('customer/edit/<int:cid>/', views.editCustomer, name='editCustomer'),
    path('employee/edit/<int:eid>/', views.editEmployee, name='editEmployee'),
    path('account/revenue/detail/<int:aid>/', views.revenueDetail, name='revenueDetail'),
    path('account/expense/detail/<int:aid>/', views.expenseDetail, name='expenseDetail'),
    path('account/revenue/cloth/<int:cid>/', views.getCloth, name='getCloth'),
]
