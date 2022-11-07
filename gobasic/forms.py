from .models import Hotel, Activity, Customer, Trip 
from django import forms
from django.forms import modelformset_factory

class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['balance_due', 'end_date','trip_completed', 'margin']

class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        exclude = ['balance_due', 'end_date','trip_completed', 'duration', 'hotel_cost', 'transfer_cost' , 'activity_cost', 'total_trip_cost']      

