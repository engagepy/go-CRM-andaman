from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from .models import Trip

@receiver(post_save, sender=Trip)
def trip_final_cal(sender, instance, **kwargs):
    total = 0
    activity_selected = instance.activities.all()
    for i in activity_selected:
        print('via post_save '+ str(i.net_cost))
        total += i.net_cost
    print(total)
    Trip.activity_cost = total
    return Trip.activity_cost

# @receiver(m2m_changed, sender=Trip)
# def trip_final_cal(sender, instance, **kwargs):
#     total = 0
#     activity_selected = sender.activity.all()
#     for i in activity_selected:
#         print('via m2m ' + str(i))
#         total += i.net_cost
#     print(total)
#     Trip.activity_cost = total
#     return Trip.activity_cost