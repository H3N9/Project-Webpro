from django.contrib import admin

# Register your models here.
from .models import Employee, Working_time

# Register your models here.
admin.site.register(Employee)

admin.site.register(Working_time)