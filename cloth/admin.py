from django.contrib import admin

# Register your models here.
from .models import Cloth_in_stock, Cloth_type, Color

# Register your models here.
admin.site.register(Cloth_in_stock)

admin.site.register(Cloth_type)

admin.site.register(Color)