from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CustomerCreateForm, TripCreateForm, HotelCreateForm,  ActivityCreateForm
from .models import  Trip, Customer, Hotel, Activity

from django.contrib.auth.models import User, Group




# Create your views here, leave global variables below.
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
            messages.error(request, 'Something is off, No Records Found!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Some detail is incorrect, retry!')

    loginPage_data = {'page':page}
    return render(request, 'gobasic/login_register.html', loginPage_data )

def logoutUser(request):
    logout(request)
    return redirect('signup')

 
class IndexView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    redirect_field_name = 'index'
    template_name = "gobasic/prodindex.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra QuerySets here
        #context['book_list'] = Book.objects.all()
        context['name'] = "Go CRM"
        return context

class SignUp(TemplateView):
    template_name = "gobasic/signup.html"


# Customer Views Below

class CustomerCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'gobasic/customer_create_form.html'


class CustomerEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'gobasic/customer_create_form.html'


class CustomerDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    template_name = 'gobasic/customer_delete.html'
    success_url = reverse_lazy("index")


class CustomerList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index'
    login_required = True
    model = Customer
    template_name = 'gobasic/customer_list.html'
    paginate_by = 10 


class CustomerDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Customer
    template_name = 'gobasic/customer_detail.html'

# Trip Views Below

class TripCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    form_class = TripCreateForm
    template_name = 'gobasic/trip_create_form.html'


class TripEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    form_class = TripCreateForm
    template_name = 'gobasic/trip_create_form.html'


class TripDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    template_name = 'gobasic/trip_delete.html'
    success_url = reverse_lazy("index")


class TripLists(LoginRequiredMixin, ListView):
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

        return context    

   

class TripDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Trip
    template_name = 'gobasic/trip_detail.html'   

# Hotel PB Views Below    

class HotelCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'gobasic/hotel_create_form.html'
  

class HotelEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'gobasic/hotel_create_form.html'


class HotelDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    template_name = 'gobasic/hotel_delete.html'
    success_url = reverse_lazy("index")
 

class HotelList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    template_name = 'gobasic/hotel_list_pb.html'
    paginate_by = 10 


class HotelDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Hotel
    template_name = 'gobasic/hotel_detail.html'

# Activity PB Views Below  

class ActivityCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    form_class = ActivityCreateForm
    template_name = 'gobasic/activity_create_form.html'


class ActivityEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    form_class = ActivityCreateForm
    template_name = 'gobasic/activity_create_form.html'

class ActivityDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    template_name = 'gobasic/activity_delete.html'
    success_url = reverse_lazy("index")

class ActivityList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Activity
    template_name = 'wheelio/activity_list.html'
    paginate_by = 10 

class ActivityDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'index'   
    model = Activity
    template_name = 'gobasic/acitivity_detail.html'



   