from django.urls import path, include
from rest_framework import routers
from gobasic.views import IndexView, ToolsView, SignUp, logoutUser, CustomerCreate, CustomerDelete, CustomerList, CustomerEdit,CustomerDetail, TripCreate, TripEdit, TripLists, TripDelete, TripDetail, HotelCreate, HotelDelete, HotelDetail, HotelEdit, HotelList, ActivityCreate, ActivityDelete, ActivityEdit, ActivityList, ActivityDetail,  loginPage 





urlpatterns = [

    path('signup/', SignUp.as_view(), name="signup"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),


    path('', IndexView.as_view(), name="index"),
    path('tools/', ToolsView.as_view(), name="tools"),

    #Customer URLs
    path('customer/create', CustomerCreate.as_view(), name="customer-create"),
    path('customer/update/<int:pk>', CustomerEdit.as_view(), name="customer-update"),
    path('customer/delete/<int:pk>', CustomerDelete.as_view(), name="customer-delete"),
    path('customer/list', CustomerList.as_view(), name="customer-list"),
    path('customer/detail/<int:pk>', CustomerDetail.as_view(), name="customer-detail"),
    
    # Hotel URLs
    path('hotel/create', HotelCreate.as_view(), name="hotel-create"),
    path('hotel/update/<int:pk>', HotelEdit.as_view(), name="hotel-edit"),
    path('hotel/delete/<int:pk>', HotelDelete.as_view(), name="hotel-delete"),
    path('hotel/list', HotelList.as_view(), name="hotel-list"),
    path('hotel/detail/<int:pk>', HotelDetail.as_view(), name="hotel-detail-pb"),

    #Activity URLs
    path('activity/create', ActivityCreate.as_view(), name="activity-create"),
    path('activity/update/<int:pk>', ActivityEdit.as_view(), name="activity-edit"),
    path('activity/delete/<int:pk>', ActivityDelete.as_view(), name="activity-delete"),
    path('activity/list', ActivityList.as_view(), name="activity-list"),
    path('activity/detail/<int:pk>', ActivityDetail.as_view(), name="activity-detail"),
 

    # Trip URLs
    path('trip/create', TripCreate.as_view(), name="trip-create"),
    path('trip/detail/<int:pk>', TripDetail.as_view(), name="trip-detail"),
    path('trip/delete/<int:pk>', TripDelete.as_view(), name="trip-delete"),
    path('trip/update/<int:pk>', TripEdit.as_view(), name="trip-update"),
    path('trip/lists', TripLists.as_view(), name="trip-lists"),
    
]
