from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import send_mail
from django.conf import settings
from threading import Thread
import datetime

'''
Send mail function is defined below to assist with outgoing email communication. 
'''

# def send(email):
#     #Calculating Time, and limiting decimals
#     x = datetime.datetime.now()
#     s = x.strftime('%Y-%m-%d %H:%M:%S.%f')
#     s = s[:-7]
#     y = f'Your trip interest has been registed at {s} ? You can reply to this email, while our team is preparing your itinerary options, thanks.'
#     #using the send_mail import below
#     send_mail(
#         subject='GoAndamans - Best Andaman Experiences',
#         message=y,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email]
#         )
#     pass
# Base User Models Here.

class User(AbstractUser):
    is_owner = models.BooleanField(verbose_name='Is Owner ?', default=False)
    is_manager = models.BooleanField(verbose_name='Is Manager ?', default=False)
    is_employee = models.BooleanField(verbose_name='Is Employee ?', default=False)
    is_intern = models.BooleanField(verbose_name='Is Intern ?', default=False)
    is_customer = models.BooleanField(verbose_name='Is Customer ?', default=False)


#Base Data Models Here.
class Locations(models.Model):

    location = models.CharField(max_length=30, unique=True, primary_key=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    

    def __repr__(self):
        return f"{self.location}"

    def __str__(self):
        return f"{self.location}"

    def get_absolute_url(self):
        return reverse("location-list")
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.location)
        return super().save(*args, **kwargs)

class Hotel(models.Model):

    '''
    This class aims to accumulate all required hotel/resort room data, meals plans and other stay related add-ons. This includes
    net rates and exclusive feature that must be gaurded, and integration fields.
    '''

    ratings = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
] 

    room_categories = [
    ('Budget', 'Budget'),
    ('Premium', 'Premium'),
    ('Deluxe', 'Deluxe'),
    ('Luxury', 'Luxury'),
    ('Ultra Luxury', 'Ultra Luxury'),
] 

    hotel_name = models.CharField(max_length=25)
    slug = models.SlugField(null=True, blank=True, unique=True)
    customer_rating = models.CharField(max_length=1, choices = ratings, default='1' )
    room_name = models.CharField(max_length=15)
    room_categories = models.CharField(max_length=12, choices=room_categories, default='1')
    location = models.ForeignKey(Locations, on_delete=models.PROTECT)
    net_cp = models.PositiveIntegerField(validators=[MaxValueValidator(1000000),  MinValueValidator(1)], verbose_name ='CP', default=0, help_text = 'Per Day for 2pax')
    net_map = models.PositiveIntegerField(validators=[MaxValueValidator(1000000),  MinValueValidator(1)], verbose_name ='MAP', default=0, help_text = 'Per Day for 2pax')
    net_cp_kid = models.PositiveIntegerField(validators=[MaxValueValidator(1000000),  MinValueValidator(1)], verbose_name ='CP Kid', default=0, help_text = 'Per Day for 1pax')
    net_map_kid = models.PositiveIntegerField(validators=[MaxValueValidator(1000000),  MinValueValidator(1)],verbose_name ='MAP Kid', default=0, help_text = 'Per Day for 1pax')
    entry_last_updated = models.DateTimeField(auto_now=True, editable=False)
    entry_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['customer_rating']
    
    def __repr__(self):
        return f"Hotel {self.hotel}, Location {self.location}, Room {self.room_categories} - {self.room.name}"
    
    def __str__(self):
        return f"{self.hotel_name} - {self.location} - {self.room_categories} - {self.room_name}"

    def get_absolute_url(self):
        return reverse('hotels-list')
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.hotel_name)
        return super().save(*args, **kwargs)    

class Activity(models.Model):

    '''
    This class aims to accumulate all activity data that can be 
    offered as add-on during trip creation. 
    Adventure sport specific validation, form and communication must follow. 
    '''

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
    slug = models.SlugField(null=True, blank=True, unique=True)
    acitivity_duration = models.CharField(max_length=2, choices = acitivity_duration )
    activity_location = models.ForeignKey(Locations, on_delete=models.PROTECT)
    description = models.CharField(max_length=250)
    net_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(1)], default=0)
    activity_status = models.BooleanField(default=False)
    entry_last_updated = models.DateTimeField(auto_now=True, editable=False)
    entry_created = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        ordering = ['activity_title']
    
    def __repr__(self):
        return f"{self.activity_title} - {self.activity_location} - {self.net_cost}"
        
    def __str__(self):
        return f"{self.activity_title}, {self.activity_location}, {self.acitivity_duration}, {self.net_cost}"

    def get_absolute_url(self):
        return reverse('activitys-list')

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.activity_title)
        return super().save(*args, **kwargs) 


# Transfers model is here

class Transfer(models.Model):

    '''
    This class aims to accumulate all transfer data that can be 
    offered as add-on during trip creation. Cabs, Ferry, All Inclusive or Ala Carte.
    '''


    transfer_title = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.CharField(max_length=250)
    net_cost = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(1)], default=0)
    entry_last_updated = models.DateTimeField(auto_now=True, editable=False)
    entry_created = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        ordering = ['transfer_title']
    
    def __repr__(self):
        return f"{self.transfer_title} - {self.net_cost}"
        
    def __str__(self):
        return f"{self.transfer_title}, {self.net_cost}"

    def get_absolute_url(self):
        return reverse('transfer-list')

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.transfer_title)
        return super().save(*args, **kwargs) 


# Customer Model Here

class Customer(models.Model):
    '''
    This class aims to accumulate all required data for a customer. 
    This includes personal information that must be gaurded, 
    and integration fields.
    '''
    
    source_choices = [
    ('whatsapp', 'WhatsApp'),
    ('email', 'Email'),
    ('phone', 'Phone'),
    ('founder', 'Founder'),
    ('social', 'Social Media'),
    ('web', 'Website'),
    ('other', 'Other'),
] 
    
    name = models.CharField(max_length = 30)
    slug = models.SlugField(null=True, blank=True, unique=True)
    mobile = models.CharField(max_length=12, unique=True, help_text= '<em>10 digits</em>')
    email = models.EmailField(blank=True, unique=True)
    pax = models.PositiveSmallIntegerField(default=1)
    source = models.CharField(max_length=10, choices=source_choices)
    entry_last_updated = models.DateTimeField(auto_now=True, editable=False)
    entry_created = models.DateTimeField(auto_now_add=True, editable=False)    

    def save(self, *args, **kwargs):
        email= self.email
        #Thread(target=send, args=(email)).start()     
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        ordering = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} - {self.pax}"

    def get_absolute_url(self):
        return reverse('customer-list')
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs) 
# Trip Model Here

class Trip(models.Model):
    '''
    -->  will host all fields required to book the final travel product 
    --> constitutes sub products and services 
    --> data will facilitate itinerary generation, cost calculation and 
    communication functions.
    '''

    transfer_choices = [
    ('PB-HV-PB-ALL', 'PB-HV AI'),
    ('PB-HV-NL-PB-ALL', 'PB-HV-NL AI'),
    ('PB-HV-PB-PnD', 'PB-HV P-n-D'),
    ('PB-HV-NL-PB-PnD', 'PB-HV-NL P-n-D'),
    ('PB-HV-Ferry', 'Ferry-Only-PB-HV'),
    ('PB-HV-NL-Ferry', 'Ferry-Only-PB-HV-NL'),
]

    lead_status = [
    ('Enquiry', 'Enquiry'),
    ('Proposal', 'Proposal'),
    ('Confirmed', 'Confirmed'),
    ('Passed', 'Passed'),
    ('VIP', 'VIP'),
    ('Defense', 'Defense'),
    ('F-n-F', 'F-n-F'),
]

    meal_plan = [
    ('net_cp', 'Breakfast'),
    ('net_map', 'Breakfast + 1 Meal'),
    # ('net_cp_kid', 'Child Breakfast'),
    # ('net_map_kid', 'Child Breakfast + 1 Meal'),
]

    customer = models.ForeignKey(Customer, null=True, on_delete=models.PROTECT)
    slug = models.SlugField(null=True, blank=True, unique=True)
    lead = models.CharField(max_length=11, choices=lead_status, blank=True, null=True)
    start_date = models.DateTimeField(default= timezone.now, help_text='yyyy-mm-dd,hh--mm')
    end_date = models.DateTimeField(default = timezone.now)

    #destination 1 hotels related fields below
    hotel_pb = models.ForeignKey(Hotel, verbose_name='Hotel Port Blair', related_name='pb_hotel_set', limit_choices_to={'location': 'Port Blair'}, on_delete=models.PROTECT, blank=True, null=True)
    plan_pb = models.CharField(max_length=11, verbose_name='Meal Plan', default='CP', choices=meal_plan)
    pb_rooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(30), MinValueValidator(0)],default=0, verbose_name='Port Blair Rooms', help_text='Number of Rooms')
    pb_nights = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)],default=0, verbose_name='Port Blair Nights', help_text='Port Blair Nights')
    pb_add_on = models.PositiveBigIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)],default=0, verbose_name='Port Blair Add-On', help_text='Port Blair Hotel Add On')

    #destination 2 hotel related fields below
    hotel_hv = models.ForeignKey(Hotel, verbose_name='Hotel Havelock', related_name='hv_hotel_set',limit_choices_to={'location': 'Havelock Island'},  on_delete=models.PROTECT, blank=True, null=True)
    plan_hv = models.CharField(max_length=11, verbose_name='Meal Plan', default='CP', choices=meal_plan)
    hv_rooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(30), MinValueValidator(0)],default=0, verbose_name='Havelock Rooms', help_text='Number of Rooms')
    hv_nights = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)],default=0, verbose_name='Havelock Nights')
    hv_add_on = models.PositiveBigIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)],default=0, verbose_name='Havelock Hotel Add-On', help_text='Havelock Hotel Add On')

    #destination 3 hotel related fields below
    hotel_nl = models.ForeignKey(Hotel, verbose_name='Hotel Neil', related_name='nl_hotel_set',limit_choices_to={'location': 'Neil Island'},  on_delete=models.PROTECT, blank=True, null=True)
    plan_nl = models.CharField(max_length=11, verbose_name='Meal Plan', default='CP', choices=meal_plan)
    nl_rooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(30), MinValueValidator(0)],default=0, verbose_name='Neil Rooms', help_text='Number of Rooms')
    nl_nights = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)],default=0, verbose_name='Neil Nights')
    nl_add_on = models.PositiveBigIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)],default=0, verbose_name='Neil Hotel Add-On', help_text='Neil Hotel Add On')

    #duration and add-ons below
    duration = models.PositiveSmallIntegerField(verbose_name='Trip Nights', blank=True)
    trip_completed = models.BooleanField(default=False)
    activities = models.ManyToManyField(Activity, related_name="activities", blank=True, help_text='select multiple, note locations')
    transfers = models.ForeignKey(Transfer, blank=True, null=True, on_delete=models.PROTECT)

    #fiscal fields below
    transfer_cost = models.PositiveIntegerField(default=0, blank = True, null=False)
    hotel_cost = models.PositiveIntegerField(default=0, null=False)
    advance_paid = models.PositiveIntegerField(default=0)
    activity_cost = models.PositiveIntegerField(default =0)
    total_trip_cost = models.PositiveIntegerField(default=0)
    profit = models.PositiveBigIntegerField(default=0)
    tax = models.PositiveBigIntegerField(default=0)

    booked = models.BooleanField(default=False)

    entry_last_updated = models.DateTimeField(auto_now=True, editable=False)
    entry_created = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        ordering = []

    def __repr__(self):
        return f'{self.customer.name} for {self.duration} day/s'

    def __str__(self):
        return f"{self.customer.name} - {self.duration} - {self.start_date} - {self.end_date}"

    def get_absolute_url(self):
        return reverse('trip-lists')

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.customer.name)
        return super().save(*args, **kwargs) 
