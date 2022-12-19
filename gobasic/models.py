from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import send_mail
from django.conf import settings
import asyncio
from threading import Thread
import datetime

# Send mail function is defined below to assist with outgoing email communication. t
def send(email):
    #Calculating Time, and limiting decimals
    x = datetime.datetime.now()
    s = x.strftime('%Y-%m-%d %H:%M:%S.%f')
    s = s[:-3]
    y = f'Your trip interest has been registed at {s} ? Please respond to this email, or give us sometime. Our team will connect with you shortly, thanks.'
    #using the send_mail import below
    send_mail(
        subject='GoAndamans - Best Andaman Experiences',
        message=y,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
        )

# Base Models Here.

class Hotel(models.Model):

    '''
    This class aims to accumulate all required hotel/resort room data, meals plans and other stay related add-ons. This includes
    net rates and exclusive features that must be gaurded, and integration fields.
    '''

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
    customer_rating = models.CharField(max_length=1, choices = ratings, default='1' )
    room_category = models.CharField(max_length=15)
    location = models.CharField(max_length=2, choices=hotel_location , default='Pb')
    net_cp = models.PositiveIntegerField(validators=[MaxValueValidator(100000),  MinValueValidator(0)], verbose_name ='CP', default=0, help_text = 'Per Day for 2pax')
    net_map = models.PositiveIntegerField(validators=[MaxValueValidator(100000),  MinValueValidator(0)], verbose_name ='MAP', default=0, help_text = 'Per Day for 2pax')

    net_cp_kid = models.PositiveIntegerField(validators=[MaxValueValidator(100000),  MinValueValidator(0)], verbose_name ='CP Kid', default=0, help_text = 'Per Day for 1pax')
    net_map_kid = models.PositiveIntegerField(validators=[MaxValueValidator(100000),  MinValueValidator(0)],verbose_name ='MAP Kid', default=0, help_text = 'Per Day for 1pax')
   
    entry_last_updated = models.DateTimeField(auto_now=True, editable = False)
    entry_created = models.DateTimeField(auto_now_add=True, editable = False)

    class Meta:
        ordering = ['customer_rating']
    
    def __repr__(self):
        return f"Hotel {self.hotel}, Location {self.location}, Room {self.room_category}"
    
    def __str__(self):
        return f"{self.hotel_name} - {self.location} - {self.room_category}"

    def get_absolute_url(self):
        return reverse('hotels-list')

class Activity(models.Model):

    '''
    This class aims to accumulate all activity data that can be offered as add-on during trip creation. Adventure sport specific validation, form and communication must follow. 
    '''

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
    net_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)], default=0)
    entry_last_updated = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True)
    activity_status = models.BooleanField(default=False)
    class Meta:
        ordering = ['activity_title']
    
    def __repr__(self):
        return f"{self.activity_title} - {self.activity_location} - {self.net_cost}"
        
    def __str__(self):
        return f"Activity {self.activity_title}, Location {self.activity_location}, Duration {self.acitivity_duration}, Cost {self.net_cost}"

    def get_absolute_url(self):
        return reverse('activitys-list')
        #, kwargs={'pk' : self.pk})



# Customer Model Here

class Customer(models.Model):
    '''
    This class aims to accumulate all required data for a customer. This includes
    personal information that must be gaurded, and integration fields.
    '''
    
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
    pax = models.PositiveSmallIntegerField(default=1)
    source = models.CharField(max_length=10, choices=source_choices)
    entry_last_updated = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True, editable = False)
    def save(self, *args, **kwargs):
        email= self.email
        Thread(target=send, args=(email,)).start()      
        
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-entry_created']

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} - {self.pax}"

    def get_absolute_url(self):
        return reverse('customer-list')

# Trip Model Here

class Trip(models.Model):
    '''
    This class aims to perform all functions and calculations required to book a customer. This includes
    itinerary generation, cost calculation and communication functions. 
    '''

    transfer_choices = [
    ('PB-HV-PB', 'Havelock Round Trip'),
    ('PB-HV-NL-PB', 'Havelock-Neil Round Trip'),

]

    lead_status = [
    ('Enquiry', 'Enquiry'),
    ('Proposal', 'Proposal'),
    ('Confirmed', 'Confirmed'),

]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    lead = models.CharField(max_length=11, choices=lead_status, blank=True, null=True)
    start_date = models.DateTimeField(default= timezone.now, help_text='yyyy-mm-dd,hh--mm')
    end_date = models.DateTimeField(default = timezone.now)

    #destination 1 hotels related fields below
    hotel_pb = models.ForeignKey(Hotel, verbose_name='Hotel PB', related_name='pb_hotel_set', limit_choices_to={'location': 'Pb'}, on_delete=models.PROTECT, blank=True, null=True)
    pb_rooms = models.PositiveSmallIntegerField(default=0, verbose_name='PB Rooms', help_text='Number of Rooms')
    pb_nights = models.PositiveSmallIntegerField(default=0, verbose_name='PB Nights', help_text='include return nights')

    #destination 2 hotel related fields below
    hotel_hv = models.ForeignKey(Hotel, verbose_name='Hotel HV', related_name='hv_hotel_set', limit_choices_to={'location': 'Hv'}, on_delete=models.PROTECT, blank=True, null=True)
    hv_rooms = models.PositiveSmallIntegerField(default=0, verbose_name='HV Rooms', help_text='Number of Rooms')
    hv_nights = models.PositiveSmallIntegerField(default=0, verbose_name='HV Nights')

    #destination 3 hotel related fields below
    hotel_nl = models.ForeignKey(Hotel, verbose_name='Hotel NL', related_name='nl_hotel_set', limit_choices_to={'location': 'Nl'}, on_delete=models.PROTECT, blank=True, null=True)
    nl_rooms = models.PositiveSmallIntegerField(default=0, verbose_name='NL Rooms', help_text='Number of Rooms')
    nl_nights = models.PositiveSmallIntegerField(default=0, verbose_name='NL Nights')

    #duration and add-ons below
    duration = models.PositiveSmallIntegerField(verbose_name='Trip Nights', blank=True)
    trip_completed = models.BooleanField(default=False)
    activity = models.ManyToManyField(Activity, related_name="activities", blank=True, verbose_name='Activities', help_text='select multiple, note location tags')
    transfers = models.CharField(max_length=11, choices=transfer_choices, blank=True, null=True)

    #fiscal fields below
    transfer_cost = models.PositiveIntegerField(default=0, blank = True, null=False)
    hotel_cost = models.PositiveIntegerField(default=0, null=False)
    advance_paid = models.PositiveIntegerField(default=0)
    activity_cost = models.PositiveIntegerField(default =0)
    total_trip_cost = models.PositiveIntegerField(default=0)
    
    #admin fields below
    entry_last_updated = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_created']

    def __repr__(self):
        return f'{self.customer.name} for {self.duration} day/s'

    def __str__(self):
        return f"{self.customer.name} - {self.duration} - {self.start_date} - {self.end_date}"

    def save(self, *args, **kwargs):

        self.hotel_cost = 0
        self.transfer_cost = 0

        if self.transfers == 'PB-HV-PB':
            self.transfer_cost += (7500 * self.customer.pax)
        elif self.transfers == 'PB-HV-NL-PB':
            self.transfer_cost += (12500 * self.customer.pax)

        self.duration = self.pb_nights + self.hv_nights + self.nl_nights
        self.end_date = self.start_date + datetime.timedelta(days=self.duration)
        if self.hv_nights and self.pb_nights and self.nl_nights > 0:
            self.hotel_cost += self.hv_nights * (self.hotel_hv.net_cp * self.hv_rooms)
            self.hotel_cost += self.pb_nights * (self.hotel_pb.net_cp * self.pb_rooms)
            self.hotel_cost += self.nl_nights * (self.hotel_nl.net_cp * self.nl_rooms) 
        elif self.hv_nights and self.pb_nights > 0:
            self.hotel_cost += self.hv_nights * (self.hotel_hv.net_cp * self.hv_rooms) 
            self.hotel_cost += self.pb_nights * (self.hotel_pb.net_cp * self.pb_rooms)
        elif self.nl_nights and self.pb_nights > 0:
            self.hotel_cost += self.nl_nights * (self.hotel_nl.net_cp * self.nl_rooms) 
            self.hotel_cost += self.pb_nights * (self.hotel_pb.net_cp * self.pb_rooms)
        elif self.nl_nights > 0:
            self.hotel_cost += self.nl_nights * (self.hotel_nl.net_cp * self.nl_rooms) 
        elif self.pb_nights > 0:
            self.hotel_cost += self.pb_nights * (self.hotel_pb.net_cp * self.pb_rooms)
        elif self.hv_nights >0:
            self.hotel_cost += self.hv_nights * (self.hotel_hv.net_cp * self.hv_rooms)
        super(Trip, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('trip-lists')

