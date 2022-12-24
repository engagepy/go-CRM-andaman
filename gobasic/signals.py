from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from .models import Trip



# @receiver(pre_save, sender=Trip)
# def trip_final_cal(sender, instance, update_fields='activity_cost', **kwargs):
#     total = 0
#     activity_selected = instance.activities.all()
#     for i in activity_selected:
#         print('via pre_save '+ str(i.net_cost))
#         total += i.net_cost
#     print(total)
#     instance.activity_cost=total

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