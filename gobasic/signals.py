from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from .models import Trip
import datetime



@receiver(pre_save, sender=Trip)
def trip_final_cal(sender, instance, *args, **kwargs):

    instance.hotel_cost = 0
    instance.transfer_cost = 0
    if not instance.hotel_pb:
        instance.pb_rooms = 0
        instance.pb_nights = 0
    if not instance.hotel_hv:
        instance.hv_rooms = 0
        instance.hv_nights = 0
    if not instance.hotel_nl:
        instance.nl_rooms = 0
        instance.nl_nights = 0

    if instance.transfers == 'PB-HV-PB-ALL':
        instance.transfer_cost += (10500 * instance.customer.pax)
    elif instance.transfers == 'PB-HV-NL-PB-ALL':
        instance.transfer_cost += (15000 * instance.customer.pax)
    elif instance.transfers == 'PB-HV-PB-PnD':
        instance.transfer_cost += (8000 * instance.customer.pax)
    elif instance.transfers == 'PB-HV-NL-PB-PnD':
        instance.transfer_cost += (12500 * instance.customer.pax)
    elif instance.transfers == 'PB-HV-Ferry':
        instance.transfer_cost += (3500 * instance.customer.pax)
    elif instance.transfers == 'PB-HV-NL-Ferry':
        instance.transfer_cost += (5000 * instance.customer.pax)

    instance.duration = instance.pb_nights + instance.hv_nights + instance.nl_nights
    instance.end_date = instance.start_date + datetime.timedelta(days=instance.duration)
    if instance.hv_nights and instance.pb_nights and instance.nl_nights > 0:
        instance.hotel_cost += instance.hv_nights * (instance.hotel_hv.net_cp * instance.hv_rooms)
        instance.hotel_cost += instance.pb_nights * (instance.hotel_pb.net_cp * instance.pb_rooms)
        instance.hotel_cost += instance.nl_nights * (instance.hotel_nl.net_cp * instance.nl_rooms) 
    elif instance.hv_nights and instance.pb_nights > 0:
        instance.hotel_cost += instance.hv_nights * (instance.hotel_hv.net_cp * instance.hv_rooms) 
        instance.hotel_cost += instance.pb_nights * (instance.hotel_pb.net_cp * instance.pb_rooms)
    elif instance.nl_nights and instance.pb_nights > 0:
        instance.hotel_cost += instance.nl_nights * (instance.hotel_nl.net_cp * instance.nl_rooms) 
        instance.hotel_cost += instance.pb_nights * (instance.hotel_pb.net_cp * instance.pb_rooms)
    elif instance.nl_nights > 0:
        instance.hotel_cost += instance.nl_nights * (instance.hotel_nl.net_cp * instance.nl_rooms) 
    elif instance.pb_nights > 0:
        instance.hotel_cost += instance.pb_nights * (instance.hotel_pb.net_cp * instance.pb_rooms)
    elif instance.hv_nights >0:
        instance.hotel_cost += instance.hv_nights * (instance.hotel_hv.net_cp * instance.hv_rooms) 
    instance.total_trip_cost = instance.activity_cost + instance.hotel_cost + instance.transfer_cost 

@receiver(m2m_changed, sender=Trip.activities.through)
def activity_final_cal(sender, instance, action,model,pk_set, *args, **kwargs):
    total = 0
    activity_selected = instance.activities.all()
    for i in activity_selected:
        print('via m2m ' + str(i))
        total += i.net_cost
    print(total)
    instance.activity_cost = total
    instance.save()