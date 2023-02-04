from django.urls import path, include
from rest_framework import routers
from gobasic.views import IndexView, ToolsView, logoutUser, CustomerCreate, LocationCreate, TransferCreate, TransferList, LocationEdit, LocationList, CustomerDelete, CustomerList, CustomerEdit,CustomerDetail, TripCreate, TripEdit, TripLists, TripDelete, TripDetail, HotelCreate, HotelDelete, HotelDetail, HotelEdit, HotelList, ActivityCreate, ActivityDelete, ActivityEdit, ActivityList, ActivityDetail,  loginPage 


urlpatterns = [

    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),


    path('', IndexView.as_view(), name="index"),

    #Customer URLs
    path('customer/create', CustomerCreate.as_view(), name="customer-create"),
    path('customer/update/<slug:slug>', CustomerEdit.as_view(), name="customer-update"),
    path('customer/delete/<slug:slug>', CustomerDelete.as_view(), name="customer-delete"),
    path('customer/list', CustomerList.as_view(), name="customer-list"),
    path('customer/detail/<slug:slug>', CustomerDetail.as_view(), name="customer-detail"),
    
    # Hotel URLs
    path('hotel/create', HotelCreate.as_view(), name="hotel-create"),
    path('hotel/update/<slug:slug>', HotelEdit.as_view(), name="hotel-edit"),
    path('hotel/delete/<slug:slug>', HotelDelete.as_view(), name="hotel-delete"),
    path('hotels/list', HotelList.as_view(), name="hotels-list"),
    path('hotel/detail/<slug:slug>', HotelDetail.as_view(), name="hotel-detail-pb"),

    #Activity URLs
    path('activity/create', ActivityCreate.as_view(), name="activity-create"),
    path('activity/update/<slug:slug>', ActivityEdit.as_view(), name="activity-edit"),
    path('activity/delete/<slug:slug>', ActivityDelete.as_view(), name="activity-delete"),
    path('activitys/list', ActivityList.as_view(), name="activitys-list"),
    path('activity/detail/<slug:slug>', ActivityDetail.as_view(), name="activity-detail"),
 

    # Trip URLs
    path('trip/create', TripCreate.as_view(), name="trip-create"),
    path('trip/detail/<slug:slug>', TripDetail.as_view(), name="trip-detail"),
    path('trip/delete/<slug:slug>', TripDelete.as_view(), name="trip-delete"),
    path('trip/update/<slug:slug>', TripEdit.as_view(), name="trip-update"),
    path('trip/lists', TripLists.as_view(), name="trip-lists"),

    #Location URLs

    path('location/create', LocationCreate.as_view(), name="location-create"),
    path('location/list', LocationList.as_view(), name="location-list"),
    path('location/update/<slug:slug>', LocationEdit.as_view(), name="location-update"),


    # Transfer URLs Here : 

    path('transfer/create', TransferCreate.as_view(), name="transfer-create"),
    path('transfer/list', TransferList.as_view(), name="transfer-list"),
]
