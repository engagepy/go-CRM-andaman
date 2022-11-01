from django.contrib import admin
from .models import Customer, Hotel, Activity, Trip

# Register your models here.

admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Hotel)
