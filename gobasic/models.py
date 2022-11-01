from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator

# Base Models Here.

class Hotel(models.Model):
    ratings = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
] 

    hotel_location = [
    ('Pb', 'Port Blair'),
    ('Hv', 'Havelock'),
    ('Nl', 'Neil'),
] 
    hotel_name = models.CharField(max_length=25, unique=True)
    customer_rating = models.CharField(max_length=1, choices = ratings )
    room_category = models.CharField(max_length=15)
    location = models.CharField(max_length=2, choices=hotel_location)
    ep_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 2pax')
    cp_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 2pax')
    map_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 2pax')
    ap_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 2pax')
    ep_child = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 1pax')
    cp_child = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 1pax')
    map_child = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 1pax')
    ap_child = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0, help_text = 'Per Day for 1pax')

    entry_last_updated = models.DateTimeField(auto_now=True, editable = False)
    entry_created = models.DateTimeField(auto_now_add=True, editable = False)

    class Meta:
        ordering = ['customer_rating']
    
    def __repr__(self):
        return f"Hotel {self.hotel}, Location {self.location}, Rating {self.customer_rating}, Room {self.room_category}"
    
    def __str__(self):
        return f"{self.hotel_name} - {self.location} - {self.room_category} - {self.customer_rating}"

    def get_absolute_url(self):
        return reverse('hotel-list')
        #, kwargs={'pk' : self.pk})

class Activity(models.Model):
    activity_location = [
    ('Pb', 'Port Blair'),
    ('Hv', 'Havelock'),
    ('Nl', 'Neil'),
] 

    acitivity_duration = [
    ('1H', '1 hour'),
    ('2H', '2 hour'),
    ('3H', '3 hour'),
    ('1D', '1 Day'),
    ('2D', '2 Day'),
    ('4D', '4 Day'),
    ('6D', '6 Day'),
] 
    activity_title = models.CharField(max_length=20, unique=True)
    acitivity_duration = models.CharField(max_length=2, choices = acitivity_duration )
    activity_location = models.CharField(max_length=2, choices = activity_location, default="Pb")
    description = models.CharField(max_length=250)
    mrp_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0)
    net_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0)
    margin = models.PositiveIntegerField(default = 0)
    entry_last_updated = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True)
    activity_status = models.BooleanField(default=False)

    
    class Meta:
        ordering = ['margin']
    
    def __repr__(self):
        return f"Activity {self.activity_title}, Location {self.activity_location}, Duration {self.acitivity_duration}, Cost {self.mrp_cost}"
    
    def __str__(self):
        return f"{self.activity_title} - {self.activity_location} - {self.mrp_cost}"

    def get_absolute_url(self):
        return reverse('activity-list')
        #, kwargs={'pk' : self.pk})
    
    def save(self, *args, **kwargs):
        self.margin = self.mrp_cost - self.net_cost
        super(Activity, self).save(*args, **kwargs)



# Customer Model Here

class Customer(models.Model):
    
    source_choices = [
    ('whatsapp', 'WhatsApp'),
    ('email', 'Email'),
    ('phone', 'Phone'),
    ('founder', 'Founder'),
    ('socialm', 'Social Media'),
    ('web', 'Website'),
    ('other', 'Other'),
] 
    #Create function to auto list next 10 years into choice tuples

    name = models.CharField(max_length = 30)
    mobile = models.CharField(max_length=12, unique=True, help_text= '<em>10 digits</em>')
    email = models.EmailField(blank=True, unique=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=10, choices=source_choices)
    entry_last_updated = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True, editable = False)

    class Meta:
        ordering = ['entry_created']

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} - {self.mobile}"

    def get_absolute_url(self):
        return reverse('customer-list')

# Trip Model Here

class Trip(models.Model):
    hotel_pb = models.ForeignKey(Hotel, related_name='pb_hotel_set', on_delete=models.PROTECT, blank=True, null=True)
    hotel_hv = models.ForeignKey(Hotel, related_name='hv_hotel_set', on_delete=models.PROTECT, blank=True, null=True)
    hotel_nl = models.ForeignKey(Hotel, related_name='nl_hotel_set', on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default= timezone.now, help_text='yyyy-mm-dd,hh--mm')
    duration = models.PositiveSmallIntegerField(verbose_name='Trip Nights', default=0)
    end_date = models.DateTimeField(default = timezone.now)
    acitivity_pb = models.ForeignKey(Activity, related_name='pb_activity_set', on_delete=models.PROTECT, blank=True, null=True)
    acitivity_hv = models.ForeignKey(Activity, related_name='hv_activity_set', on_delete=models.PROTECT, blank=True, null=True)
    acitivity_nl = models.ForeignKey(Activity, related_name='nl_activity_set', on_delete=models.PROTECT, blank=True, null=True)
    total_cost = models.PositiveIntegerField(default=0)
    advance_paid = models.PositiveIntegerField(default=0)
    balance_due = models.PositiveIntegerField(default =0)
    trip_completed = models.BooleanField(default=False)
    entry_last_updated = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __repr__(self):
        return f'{self.customer.name} for {self.duration} day/s'

    def __str__(self):
        return f"{self.hotel_pb.hotel_name} - {self.hotel_hv.hotel_name} - {self.hotel_nl.hotel_name} - {self.customer.name} - {self.resort} - {self.room_no}"

    def save(self, *args, **kwargs):
        self.end_date += datetime.timedelta(days=self.duration)
        self.balance_due = self.total_cost - self.advance_paid

        #Not Working - Needs to be updated on rental, and re-updated on rental termination
        super(Trip, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('trip-list')

