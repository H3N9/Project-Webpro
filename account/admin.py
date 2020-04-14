from django.contrib import admin

# Register your models here.
from .models import Employee, Working_time, Expense, Paid_salary

# Register your models here.
admin.site.register(Employee)

admin.site.register(Working_time)

admin.site.register(Expense)

admin.site.register(Paid_salary)