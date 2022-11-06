from rest_framework import viewsets
from rest_framework import permissions
from gobasic.serializers import UserSerializer, GroupSerializer, TripSerializer
from django.contrib.auth.models import User, Group
from gobasic.models import  Trip, Customer, Hotel, Activity


###API VIEWS




class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Trip.objects.all().order_by('end_date')
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
   
