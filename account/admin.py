from django.contrib import admin

# Register your models here.
from .models import Employee, Working_time, Expense, Paid_salary, Revenue, Sell_list, Engaging, Engage_list, Selling, Customer

# Register your models here.
admin.site.register(Employee)

admin.site.register(Working_time)

admin.site.register(Expense)

admin.site.register(Paid_salary)

admin.site.register(Revenue)

admin.site.register(Sell_list)

admin.site.register(Engaging)

admin.site.register(Engage_list)

admin.site.register(Selling)

admin.site.register(Customer)