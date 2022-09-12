from django.contrib import admin
from .models import Flight, Result

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'take_off_place', 'take_off_date')
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'place', 'pigeon')

admin.site.register(Flight, FlightAdmin)
admin.site.register(Result, ResultAdmin)
