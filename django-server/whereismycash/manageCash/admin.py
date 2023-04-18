from django.contrib import admin
from .models import User, Category, Payment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Payment)