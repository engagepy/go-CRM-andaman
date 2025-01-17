from .models import Hotel, Activity, Customer, Trip , Locations, Transfer
from django import forms

class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['timestamp','slug']

class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['balance_due', 'end_date','trip_completed', 'margin', 'timestamp','slug']

class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['timestamp','slug']


class TransferCreateForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = '__all__'
        exclude = ['slug']

class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = '__all__'
        exclude = ['timestamp','slug']

class TripCreateForm(forms.ModelForm):

    class Meta():
        model = Trip

        fields = '__all__'
        exclude = [
            'balance_due', 'tax', 'profit', 'end_date',
            'trip_completed', 'duration', 'hotel_cost', 
            'transfer_cost' , 'timestamp', 'activity_cost', 
            'total_trip_cost','slug'
            ]      

