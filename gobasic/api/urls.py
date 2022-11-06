from django.urls import path, include
from rest_framework import routers
from .views import  GroupViewSet, UserViewSet, TripViewSet, HotelViewSet, ActivityViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'trips', TripViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'activitys', ActivityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]