'''
This document contains signal functions, attached via 
@decorator. 
'''
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from .models import Trip, Customer
import datetime

'''
Trip.Model 'pre-save' call --> def 'trip_final_cal'
Objective: Aims to perform all neccessary logic to arrive at the
travel product total. 
'''

@receiver(pre_save, sender=Trip)
def trip_final_cal(sender, instance, *args, **kwargs):
    '''
    if statements below, represent error checking of incomplete hotel data.
    Example if hotel is selected, nights are not. Or nights and rooms are but,
    hotel is not selected. Such input if calculated would lead to incorrect
    product cost. This part is critical, important to note when refining. 
    '''

    instance.hotel_cost = 0
    instance.transfer_cost = 0
    
    if not instance.hotel_pb or instance.pb_rooms == 0 or instance.pb_nights == 0:
        instance.pb_rooms = 0
        instance.pb_nights = 0
        instance.hotel_pb = None
    if not instance.hotel_hv or instance.hv_rooms == 0 or instance.hv_nights == 0:
        instance.hv_rooms = 0
        instance.hv_nights = 0
        instance.hotel_hv = None
    if not instance.hotel_nl or instance.nl_rooms == 0 or instance.nl_nights == 0:
        instance.nl_rooms = 0
        instance.nl_nights = 0
        instance.hotel_nl = None


    '''
    if and elif statements below represent transfer selection and appropriate
    integer assignment. Hard codes product values are a strict No. To be 
    improved shortly.
    '''
    if instance.transfers != None:
        instance.transfer_cost = instance.transfers.net_cost
        instance.duration = instance.pb_nights + instance.hv_nights + instance.nl_nights
        instance.end_date = instance.start_date + datetime.timedelta(days=instance.duration)
    else:
        instance.duration = instance.pb_nights + instance.hv_nights + instance.nl_nights
        instance.end_date = instance.start_date + datetime.timedelta(days=instance.duration)
        
    '''
    Checks & Logic for "hotel room * nights = hotel_cost". 
    Ensure no null/zero value gets processed.
    CP, MAP, AP meal plan business logic.
    '''

    if instance.hv_nights > 0 and instance.hv_rooms > 0:
        if instance.plan_hv == 'net_cp':
            instance.hotel_cost += instance.hv_nights * (instance.hotel_hv.net_cp * instance.hv_rooms) + instance.hv_add_on
        elif instance.plan_hv == 'net_map':
            instance.hotel_cost += instance.hv_nights * (instance.hotel_hv.net_map * instance.hv_rooms) + instance.hv_add_on
    if instance.pb_nights > 0 and instance.pb_rooms > 0:
        if instance.plan_pb == 'net_cp':
            instance.hotel_cost += instance.pb_nights * (instance.hotel_pb.net_cp * instance.pb_rooms) + instance.pb_add_on
        elif instance.plan_pb == 'net_map':
            instance.hotel_cost += instance.pb_nights * (instance.hotel_pb.net_map * instance.pb_rooms) + instance.pb_add_on
    if instance.nl_nights > 0 and instance.nl_rooms > 0:
        if instance.plan_nl == 'net_cp':
            instance.hotel_cost += instance.nl_nights * (instance.hotel_nl.net_cp * instance.nl_rooms) + instance.nl_add_on 
        elif instance.plan_nl == 'net_map':
            instance.hotel_cost += instance.nl_nights * (instance.hotel_nl.net_map * instance.nl_rooms) + instance.nl_add_on 

    instance.total_trip_cost = instance.activity_cost + instance.hotel_cost + instance.transfer_cost
    instance.profit = instance.total_trip_cost * float(instance.profit_percentage / 100)
    instance.tax = (instance.profit * 1.18) - instance.profit
    instance.total_trip_cost += instance.profit + instance.tax

'''
Trip.Model 'm2m_changed' call --> def 'activity_final_cal'
Objective: Aims to perform all neccessary logic to arrive at the
activity total, which is a 'm2m' field in Trip.Model. 
'''

@receiver(m2m_changed, sender=Trip.activities.through)
def activity_final_cal(sender, instance, action,model,pk_set, *args, **kwargs):
    total = 0
    activity_selected = instance.activities.all()
    for i in activity_selected:
        print('m2m Update Occurred: ' + str(i))

# Activity_cost is a product of net_cost * customer.pax, at times maybe invalid on all pax
        total += i.net_cost * instance.customer.pax
    print(f"Activity Total Updated: {total}")
    instance.activity_cost = total
    instance.save()

# write a receiver for customer.pax changes, recalculates trip.activity_cost

@receiver(post_save, sender=Customer)
def customer_pax_update(sender, instance, *args, **kwargs):
    print('Customer pax updated')
    trip = Trip.objects.filter(customer=instance)
    for i in trip:
        i.activity_cost = 0
        i.save()
        activity_selected = i.activities.all()
        for j in activity_selected:
            i.activity_cost += j.net_cost * instance.pax
        i.save()


        



#If Customer.pax changes during or post trip creation. Auto-recalculate trip.activity_cost 