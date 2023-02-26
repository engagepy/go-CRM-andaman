from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, Hotel, Activity, Trip, User, Locations, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Hotel)
admin.site.register(Locations)