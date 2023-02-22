#django imports
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
#import from within the app
from .forms import CustomerCreateForm, TripCreateForm, HotelCreateForm,  ActivityCreateForm, LocationCreateForm, TransferCreateForm
from .models import  Trip, Customer, Hotel, Activity, Locations, Transfer
from django.contrib.auth.models import User, Group
#imported for send mail
from django.core.mail import send_mail
from django.conf import settings
from threading import Thread
import datetime

# def send(email, username):
#     #Calculating Time, and limiting decimals
#     x = datetime.datetime.now()
#     s = x.strftime('%Y-%m-%d %H:%M:%S.%f')
#     s = s[:-7]
#     y = f'{username} just logged in at {s} ? If not, please report the incident, thanks.'
#     #using the send_mail import below
#     send_mail(
#         subject='GoAndamans - Login Update',
#         message=y,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email]
#         )
#     pass

# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "oops")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #threaded function for async email sending
            email= user.email
            #Thread(target=send, args=(email, username)).start()
            return redirect('index')
        else:
            messages.error(request, 'Some detail is incorrect, retry!')

    loginPage_data = {'page':page}
    return render(request, 'gobasic/login.html', loginPage_data)  
    

def logoutUser(request):
    logout(request)
    return redirect('login')


class IndexView(LoginRequiredMixin, TemplateView):
    # permission_denied_message = 'Access Denied'
    login_url = 'login/'
    redirect_field_name = 'index'
    template_name = "gobasic/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra QuerySets here
        #context['book_list'] = Book.objects.all()
        context['name'] = "Go CRM"
        
        return context


# Customer Views Below

class CustomerCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_customer'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'gobasic/create_form.html'


class CustomerEdit(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_customer'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'gobasic/create_form.html'


class CustomerDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'gobasic.delete_customer'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    template_name = 'gobasic/customer_delete.html'
    success_url = reverse_lazy("index")


class CustomerList(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_customer'
    login_url = '/login/'
    redirect_field_name = 'index'
    login_required = True
    model = Customer
    template_name = 'gobasic/customer_list.html'
    paginate_by = 10 


# Transfer Views Here : 

class TransferCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_transfer'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Transfer
    form_class = TransferCreateForm
    template_name = 'gobasic/create_form.html'


class TransferList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_transfer'
    login_url = '/login/'
    redirect_field_name = 'index'
    login_required = True
    model = Transfer
    template_name = 'gobasic/transfer_list.html'
    paginate_by = 10 


class TransferEdit(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_transfer'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Transfer
    form_class = TransferCreateForm
    template_name = 'gobasic/create_form.html'


# Trip Views Here

class TripCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_trip'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    form_class = TripCreateForm
    template_name = 'gobasic/create_form.html'


class TripEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_trip'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    form_class = TripCreateForm
    template_name = 'gobasic/create_form.html'


class TripDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'gobasic.delete_trip'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    template_name = 'gobasic/trip_delete.html'
    success_url = reverse_lazy("index")


class TripLists(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_trip'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    template_name = 'gobasic/trip_list.html'
    paginate_by = 10 


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra QuerySets here
        context['total_trips'] = Trip.objects.all().count()
        #activity = Trip.objects.order_by('activity')
        return context    


# Hotel Views Below    

class HotelCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_hotel'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'gobasic/create_form.html'


class HotelEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_hotel'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'gobasic/create_form.html'


class HotelDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'gobasic.delete_hotel'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    template_name = 'gobasic/hotel_delete.html'
    success_url = reverse_lazy("index")


class HotelList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_hotel'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    template_name = 'gobasic/hotel_list_pb.html'
    paginate_by = 10 


# Locations Views Here
class LocationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_location'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Locations
    form_class = LocationCreateForm
    template_name = 'gobasic/create_form.html'


class LocationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_location'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Locations
    template_name = 'gobasic/location_list.html'
    paginate_by = 10 


class LocationEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_location'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Locations
    form_class = LocationCreateForm
    template_name = 'gobasic/create_form.html'


# Activity Views Below  

class ActivityCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_activity'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    form_class = ActivityCreateForm
    template_name = 'gobasic/create_form.html'


class ActivityEdit(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_activity'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    form_class = ActivityCreateForm
    template_name = 'gobasic/activity_create_form.html'


class ActivityDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'gobasic.delete_activity'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    template_name = 'gobasic/activity_delete.html'
    success_url = reverse_lazy("index")


class ActivityList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_activity'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    template_name = 'wheelio/activity_list.html'
    paginate_by = 10 
