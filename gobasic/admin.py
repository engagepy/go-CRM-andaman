from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Customer, Hotel, Activity,Transfer, Trip, Locations


admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Hotel)
admin.site.register(Locations)
admin.site.register(Transfer)

