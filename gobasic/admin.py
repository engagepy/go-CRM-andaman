from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from django.shortcuts import get_object_or_404
from .models import Customer, Hotel, Activity,Transfer, Trip, Locations

# # Connecting one-to-one relationship of User model to Profile model -> for Admin Panel display
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'profile'

# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline, )

# Important Step is to unregister User model from Admin Panel

# admin.site.unregister(User)

# Register your models as usual here.

# admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Hotel)
admin.site.register(Locations)
admin.site.register(Transfer)

