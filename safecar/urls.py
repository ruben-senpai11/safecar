from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('agencies/',views.agencies,name="agencies"),
    
    
    path('reader/',views.reader,name="reader"),
    path('reader/add/',views.reader_add,name="reader_add"),
    path('reader/delete/',views.reader_delete,name="reader_delete"),
    
    path('my/vehicle/<int:id>/get/',views.get_my_vehicle,name="my_vehicle"),
    path('my/vehicles/get/',views.get_my_vehicles,name="my_vehicles"),
   
    path('agency/add/',views.agency_add,name="agency_add"),
    
    
    # assurance path
    path('assurances',views.assurances,name="assurances"),
    path('assurance/add/',views.assurance_add,name="assurance_add"),
       path('assurance/delete/',views.assurance_delete,name="assurance_delete"),
    
    # peage
    path('toll/add/',views.toll_add,name="toll_add"),
    path('tolls',views.tolls,name="tolls"),
    path('tolls/delete/',views.toll_delete,name="toll_delete"),
    
    # visite
    path('technical_visit/add/',views.technical_visit_add,name="technical_visit_add"),
    path('technical_visits',views.technical_visits,name="technical_visits"),
    path('technical_visit/delete/',views.technical_visit_delete,name="technical_visit_delete"),
    
    # avis de recherche
    path('stealing/add/',views.stealing_add,name="stealing_add"),
    path('stealings',views.stealings,name="stealings"),
    path('stealing/delete',views.stealing_delete,name="stealing_delete"),
    
    
    
    
    path('report/add/',views.report_add,name="report_add"),
    path('reports/',views.reports,name="reports"),
    path('report/delete/',views.report_delete,name="report_delete"),
    
    path('notify/',views.notify,name="notify"),
    path('notify/get/',views.notify_get,name="notify_get"),
   
    path('anomaly/add/',views.anomaly_add,name="anomaly_add"),
    path('anomalies/',views.anomalies,name="anomalies"),
    path('anomaly/delete/',views.anomaly_delete,name="anomaly_delete"),
    
    path('check/reader/<int:id>/',views.check_reader,name="check_reader"),
    path('check/reader/get/',views.check_reader_get,name="check_reader_get"),
   
    
    # login url 
    path('login/',views.log,name="login"),
    path('logout/',views.logout_user,name="logout"),
    
    path('profile/<int:id>/get/',views.get_profile,name="get_profile"),
   
    path('vehicle/edit/',views.vehicle_edit,name="vehicle_edit"),
    path('vehicle/delete/',views.vehicle_delete,name="vehicle_delete"),
  
    path('',views.profile,name="profile"),
    path('agency/<int:id>/edit/',views.agency_edit,name="agency_edit"),
    
    path('agency/delete/',views.agency_delete ,name="agency_delete"),
    
    path('vehicle/<int:id>/get/',views.get_vehicle,name="vehicle"),
    path('vehicles/get/',views.get_vehicles,name="vehicles"),
    path('vehicle/search/',views.search_car,name="search_car"),
   
   
    path('owner/delete/',views.owner_delete,name="owner_delete"),
    path('owner/add/',views.owner_add,name="owner_add"),
    path('owners',views.owners,name="owners"),
    path('owner/<int:id>/edit/',views.owner_edit,name="owner_edit"),
   
   
    #api register tag
    path('tag/',views.tag_register,name="tag_register"),
    path('tag/done/',views.tag_done,name="tag_done"),
    path('api/test/',views.api_test,name="api_test"),
    path('number/notification/',views.number_notification,name="number_notification"),
    

]

