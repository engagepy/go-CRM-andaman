#django imports
from django.shortcuts import render, redirect
#import request
from django.http import HttpResponse, HttpResponseRedirect
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
from datetime import datetime
from users.models import User
from django.db.models import Count
from pypdf import PdfWriter

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.units import inch
from django.http import FileResponse



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
        username = request.POST.get('email')
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
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra QuerySets here
        user = User.objects.filter(first_name=self.request.user.first_name).first()
        current_month = datetime.now().month
        all_trips = Trip.objects.filter(entry_created__month=current_month)
        #all_trips = Trip.objects.all()
        all_trips_revenue = 0
        for trip in all_trips:
            if trip.booked:
                all_trips_revenue += trip.total_trip_cost
        context['all_trips_revenue'] = all_trips_revenue
        context['target_due_company'] = 3000000 - all_trips_revenue

        user_type = user.user_type
        all_sources = Customer.objects.values('source').annotate(count=Count('id'))
        for source in all_sources:
            src = source['source']
            context[src] = source['count']

        context['trips'] = all_trips
        if user_type != 1 and user_type != 7:
            user_trips = Trip.objects.filter(agent=user, entry_created__month=current_month)
            user_revenue = 0

            user_revenue_monthly = {}
            for trip in user_trips:
                if trip.booked:
                    trip_created_month = trip.entry_created.month
                    if trip_created_month in user_revenue_monthly:
                        user_revenue_monthly[trip_created_month] += trip.total_trip_cost
                    else:
                        user_revenue_monthly[trip_created_month] = 0
                        user_revenue_monthly[trip_created_month] += trip.total_trip_cost

            context['user_revenue_monthly'] = user_revenue_monthly



            
            for trip in user_trips:
                if trip.booked:
                    user_revenue += trip.total_trip_cost

            context['user_revenue'] = user_revenue
            context['target_due_user'] = 1000000 - user_revenue
            context['trips'] = user_trips

        context['name'] = "Go CRM"
        context['user_type'] = user_type

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
    context_object_name = 'trip'


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


class TripPdf(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_trip'
    template_name = 'gobasic/trip_list.html'
    model = Trip
    """
    width/height take value in points
    1 point = 1/72 of an inch
    """
    width = 8.268 * 72
    height = 11.693 * 72
    hotel_headings = ["Hotel Name", "Room Name", "No. of Rooms", "No. of Nights", "Meal Plan"]
    activity_headings = ["Activity Name", "Location", "Description", "Cost"]
    trip_headings = ["Customer Name", "Start Date", "End Date", "Trip Duration", "Total Trip Cost"]


    def front_page(self, canvas, trip):
        canvas.drawImage(
            "gobasic/static/gobasic/images/1.jpg",
            0,
            0,
            preserveAspectRatio=True,
            anchor="sw",
            width=self.width,
            height=self.height,
        )
        canvas.setFont("Helvetica", 32)
        canvas.setFillColorRGB(255, 255, 255)  # White
        canvas.drawCentredString(self.width / 2.0, self.height / 2.0, trip.customer.name)
        canvas.showPage()


    def middle_page(self, canvas):
        # middle page
        canvas.drawImage(
            "gobasic/static/gobasic/images/2.jpg",
            0,
            0,
            preserveAspectRatio=True,
            anchor="sw",
            width=self.width,
            height=self.height,
        )


    def print_headings(self, canvas, x, y, headings):
        canvas.setFont("Helvetica-Bold", 12)

        for heading in headings:
            if heading == "Cost":
                x += 40
            canvas.drawString(x, y, str(heading))
            x += 110

    def print_hotel_details(self, x, y, canvas, trip, location, heading, dest_no):
        canvas.setFont("Helvetica-BoldOblique", 16)
        canvas.drawCentredString(self.width / 2.0, y, heading)
        
        self.print_headings(canvas, 60, y - 30.0, self.hotel_headings)
        
        canvas.setFont("Helvetica", 9)
        y -= 60.0

        if dest_no == 1:
            rooms = trip.pb_rooms
            nights = trip.pb_nights
            meal_plan = "Breakfast" if trip.plan_pb == "net_cp" else  "Breakfast + 1 Meal"
        elif dest_no == 2:
            rooms = trip.hv_rooms
            nights = trip.hv_nights
            meal_plan = "Breakfast" if trip.plan_hv == "net_cp" else  "Breakfast + 1 Meal"
        else:
            rooms = trip.nl_rooms
            nights = trip.nl_nights
            meal_plan = "Breakfast" if trip.plan_nl == "net_cp" else  "Breakfast + 1 Meal"

        details = [location.hotel_name, location.room_name, rooms, nights, meal_plan]
        for detail in details:
            canvas.drawString(x, y, str(detail))
            x += 110

        return y - 30.0


    def print_activity_details(self, canvas, activity, x, y):
        canvas.setFont("Helvetica", 9)

        details = [activity.activity_title, activity.activity_location, activity.description, f"INR {activity.net_cost}"]
        for detail in details:
            if detail == details[-1]:
                x += 40
            canvas.drawString(x, y, str(detail))
            x += 110


    def print_trip_details(self, canvas, trip, x, y):
        canvas.setFont("Helvetica", 9)
        details = [trip.customer.name, trip.start_date.strftime("%d/%m/%Y"), trip.end_date.strftime("%d/%m/%Y"), trip.duration, f"INR {trip.total_trip_cost}"]
        for detail in details:
            canvas.drawString(x, y, str(detail))
            x += 110


    def get(self, request, slug):
        trip = Trip.objects.filter(slug=slug).first()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{trip.customer.name}-itinerary.pdf"'
        c = canvas.Canvas(response, pagesize=A4)

        self.front_page(c, trip)
        self.middle_page(c)

        x = 60
        y = self.height - 110.0
        if trip.hotel_pb is not None:
            pb = trip.hotel_pb
            y = self.print_hotel_details(x, y, c, trip, pb, "Port Blair Hotel", 1)

        if trip.hotel_hv is not None:
            hv = trip.hotel_hv
            y = self.print_hotel_details(x, y, c, trip, hv, "Havelock Island Hotel", 2)

        if trip.hotel_nl is not None:
            nl = trip.hotel_nl
            y = self.print_hotel_details(x, y, c, trip, nl, "Neil Island Hotel", 3)

        c.showPage()

        c.drawImage(
            "gobasic/static/gobasic/images/3.jpg",
            0,
            0,
            preserveAspectRatio=True,
            anchor="sw",
            width=self.width,
            height=self.height,
        )

        c.setFont("Helvetica-BoldOblique", 16)
        c.drawCentredString(self.width / 2.0, self.height - 110.0, "Activity Details")
        if trip.activities.exists():
            self.print_headings(c, 60, self.height - 140.0, self.activity_headings)

            y = self.height - 160.0
            activities = trip.activities.all()
            for activity in activities:
                self.print_activity_details(c, activity, x, y)
                y -= 20

        no_of_activities = len(trip.activities.all()) if trip.activities.exists() else 1
        c.setFont("Helvetica-BoldOblique", 16)
        c.drawCentredString(self.width / 2.0, y - 40.0, "Trip Details")
        self.print_headings(c, 40, y - 70.0, self.trip_headings)
        self.print_trip_details(c, trip, 40, y - (no_of_activities * 20.0) - 50.0)


        c.showPage()

        # last page
        c.drawImage(
            "gobasic/static/gobasic/images/4.jpg",
            0,
            0,
            preserveAspectRatio=True,
            anchor="sw",
            width=self.width,
            height=self.height,
        )

        c.save()

        return response


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
    permission_required = 'gobasic.add_locations'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Locations
    form_class = LocationCreateForm
    template_name = 'gobasic/create_form.html'


class LocationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gobasic.view_locations'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Locations
    template_name = 'gobasic/location_list.html'
    paginate_by = 10 


class LocationEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'gobasic.change_locations'
    login_url = '/login/'
    redirect_field_name = 'index'
    model = Locations
    form_class = LocationCreateForm
    template_name = 'gobasic/create_form.html'


# Activity Views Below  

class ActivityCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'gobasic.add_activity'
    permission_denied_message = HttpResponseRedirect(redirect_to='gobasic/403.html')
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
