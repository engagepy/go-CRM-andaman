from django.shortcuts import render

# Create your views here.
from re import A
from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import CustomerCreateForm, TripCreateForm,HotelCreateForm,  ActivityCreateForm
from .models import  Trip, Customer, Hotel, Activity

# Create your views here, leave global variables below.

class IndexView(TemplateView):
    template_name = "gobasic/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra QuerySets here
        #context['book_list'] = Book.objects.all()
        context['name'] = "Go CRM"
        return context

# Customer Views Below
class CustomerCreate(CreateView):
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'gobasic/customer_create_form.html'

class CustomerEdit(UpdateView):
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'gobasic/customer_create_form.html'

class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'gobasic/customer_delete.html'
    success_url = reverse_lazy("index")

class CustomerList(ListView):
    model = Customer
    template_name = 'gobasic/customer_list.html'
    paginate_by = 10 

class CustomerDetail(DetailView):
    model = Customer
    template_name = 'gobasic/customer_detail.html'

# Trip Views Below
class TripCreate(CreateView):
    model = Trip
    form_class = TripCreateForm
    template_name = 'gobasic/trip_create_form.html'

class TripEdit(UpdateView):
    model = Trip
    form_class = TripCreateForm
    template_name = 'gobasic/trip_create_form.html'

class TripDelete(DeleteView):
    model = Trip
    template_name = 'gobasic/trip_delete.html'
    success_url = reverse_lazy("index")

class TripList(ListView):
    model = Trip
    template_name = 'gobasic/trip_list.html'
    paginate_by = 10 

class TripDetail(DetailView):
    model = Trip
    template_name = 'gobasic/trip_detail.html'   

# Hotel PB Views Below    
class HotelCreate(CreateView):
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'gobasic/hotel_create_form.html'
  
class HotelEdit(UpdateView):
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'gobasic/hotel_create_form.html'

class HotelDelete(DeleteView):
    model = Hotel
    template_name = 'gobasic/hotel_delete.html'
    success_url = reverse_lazy("index")
 
class HotelList(ListView):
    model = Hotel
    template_name = 'gobasic/hotel_list_pb.html'
    paginate_by = 10 

class HotelDetail(DetailView):
    model = Hotel
    template_name = 'gobasic/hotel_detail.html'

# Activity PB Views Below  
class ActivityCreate(CreateView):
    model = Activity
    form_class = ActivityCreateForm
    template_name = 'gobasic/activity_create_form.html'

class ActivityEdit(UpdateView):
    model = Activity
    form_class = ActivityCreateForm
    template_name = 'gobasic/activity_create_form.html'
   
class ActivityDelete(DeleteView):
    model = Activity
    template_name = 'gobasic/activity_delete.html'
    success_url = reverse_lazy("index")
 
class ActivityList(ListView):
    model = Activity
    template_name = 'wheelio/activity_list.html'
    paginate_by = 10 
 
class ActivityDetail(DetailView):
    model = Activity
    template_name = 'gobasic/acitivity_detail.html'



   

   