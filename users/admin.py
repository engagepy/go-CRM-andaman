from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from gobasic.models import Customer, Hotel, Activity,Transfer, Trip, Locations
# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile' 
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'user_type']
    list_filter = ('is_staff', 'is_active', 'user_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_type', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active', 'user_type')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    
admin.site.register(User, CustomUserAdmin)

intern, created = Group.objects.get_or_create(name='Intern')
employee, created = Group.objects.get_or_create(name='Employee')
owner, created = Group.objects.get_or_create(name='Owner')

content_type_customer = ContentType.objects.get_for_model(Customer)
content_type_trip = ContentType.objects.get_for_model(Trip)
content_type_activity = ContentType.objects.get_for_model(Activity)
content_type_hotel = ContentType.objects.get_for_model(Hotel)
content_type_locations = ContentType.objects.get_for_model(Locations)
content_type_transfer = ContentType.objects.get_for_model(Transfer)

# Permissions for Customer
view_customer, created = Permission.objects.get_or_create(codename='view_customer', name='Can view customer', content_type=content_type_customer)
add_customer, created = Permission.objects.get_or_create(codename='add_customer', name='Can add customer', content_type=content_type_customer)
change_customer, created = Permission.objects.get_or_create(codename='change_customer', name='Can change customer', content_type=content_type_customer)
delete_customer, created = Permission.objects.get_or_create(codename='delete_customer', name='Can delete customer', content_type=content_type_customer)

# Permissions for Trip
view_trip, created = Permission.objects.get_or_create(codename='view_trip', name='Can view trip', content_type=content_type_trip)
add_trip, created = Permission.objects.get_or_create(codename='add_trip', name='Can add trip', content_type=content_type_trip)
change_trip, created = Permission.objects.get_or_create(codename='change_trip', name='Can change trip', content_type=content_type_trip)
delete_trip, created = Permission.objects.get_or_create(codename='delete_trip', name='Can delete trip', content_type=content_type_trip)

# Permissions for Activity
view_activity, created = Permission.objects.get_or_create(codename='view_activity', name='Can view activity', content_type=content_type_activity)
add_activity, created = Permission.objects.get_or_create(codename='add_activity', name='Can add activity', content_type=content_type_activity)
change_activity, created = Permission.objects.get_or_create(codename='change_activity', name='Can change activity', content_type=content_type_activity)
delete_activity, created = Permission.objects.get_or_create(codename='delete_activity', name='Can delete activity', content_type=content_type_activity)

# Permissions for Hotel
view_hotel, created = Permission.objects.get_or_create(codename='view_hotel', name='Can view hotel', content_type=content_type_hotel)
add_hotel, created = Permission.objects.get_or_create(codename='add_hotel', name='Can add hotel', content_type=content_type_hotel)
change_hotel, created = Permission.objects.get_or_create(codename='change_hotel', name='Can change hotel', content_type=content_type_hotel)
delete_hotel, created = Permission.objects.get_or_create(codename='delete_hotel', name='Can delete hotel', content_type=content_type_hotel)

# Permissions for Locations
view_locations, created = Permission.objects.get_or_create(codename='view_locations', name='Can view locations', content_type=content_type_locations)
add_locations, created = Permission.objects.get_or_create(codename='add_locations', name='Can add locations', content_type=content_type_locations)
change_locations, created = Permission.objects.get_or_create(codename='change_locations', name='Can change locations', content_type=content_type_locations)
delete_locations, created = Permission.objects.get_or_create(codename='delete_locations', name='Can delete locations', content_type=content_type_locations)

# Permissions for Transfer
view_transfer, created = Permission.objects.get_or_create(codename='view_transfer', name='Can view transfer', content_type=content_type_transfer)
add_transfer, created = Permission.objects.get_or_create(codename='add_transfer', name='Can add transfer', content_type=content_type_transfer)
change_transfer, created = Permission.objects.get_or_create(codename='change_transfer', name='Can change transfer', content_type=content_type_transfer)
delete_transfer, created = Permission.objects.get_or_create(codename='delete_transfer', name='Can delete transfer', content_type=content_type_transfer)

# Assigning permissions to groups
intern.permissions.add(view_customer, view_trip, view_activity, view_hotel, view_locations, view_transfer)
employee.permissions.add(view_customer, view_trip, view_activity, view_hotel, view_locations, view_transfer, add_customer, add_trip, add_activity, add_hotel, add_locations, add_transfer, change_customer, change_trip, change_activity, change_hotel, change_locations, change_transfer, delete_customer, delete_trip, delete_activity, delete_hotel, delete_locations, delete_transfer)
owner.permissions.add(view_customer, view_trip, view_activity, view_hotel, view_locations, view_transfer, add_customer, add_trip, add_activity, add_hotel, add_locations, add_transfer, change_customer, change_trip, change_activity, change_hotel, change_locations, change_transfer, delete_customer, delete_trip, delete_activity, delete_hotel, delete_locations, delete_transfer)

