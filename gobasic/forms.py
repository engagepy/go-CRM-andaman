from .models import Hotel, Activity, Customer, Trip , Locations
from django import forms
from django.forms import modelformset_factory

class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['timestamp']

class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['balance_due', 'end_date','trip_completed', 'margin', 'timestamp']

class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['timestamp']

class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = '__all__'
        exclude = ['timestamp']

class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        exclude = ['balance_due', 'end_date','trip_completed', 'duration', 'hotel_cost', 'transfer_cost' , 'timestamp', 'activity_cost', 'total_trip_cost']      

