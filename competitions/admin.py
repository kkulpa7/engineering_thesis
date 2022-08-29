from django.contrib import admin
from .models import Competition, Category, Results

# Register your models here.
admin.site.register(Competition)
admin.site.register(Category)
admin.site.register(Results)
