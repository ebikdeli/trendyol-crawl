from django.contrib import admin
from .models import Category, Brand, Product


admin.site.register([Category, Brand, Product])
