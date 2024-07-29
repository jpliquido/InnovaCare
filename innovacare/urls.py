from django.contrib import admin
from django.urls import path
from innovacare import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view,name='home'),

    path('aboutus/', views.aboutus_view, name='about-us'),
    path('contactus/', views.contactus_view, name='contact-us'),

    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('physicianclick/', views.physicianclick_view, name='physicianclick'),
    path('clientclick/', views.clientclick_view, name='clientclick'),

    path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path('physiciansignup/', views.physician_signup_view,name='physiciansignup'),
    path('clientsignup/', views.client_signup_view, name='clientsignup'),
    
    path('adminlogin/', LoginView.as_view(template_name='innovacare/adminlogin.html'), name='adminlogin'),
    path('physicianlogin/', LoginView.as_view(template_name='innovacare/physicianlogin.html'), name='physicianlogin'),
    path('clientlogin/', LoginView.as_view(template_name='innovacare/clientlogin.html'), name='clientlogin'),


    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='index.html'),name='logout'),


    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),

    path('admin-physician/', views.admin_physician_view,name='admin-physician'),
    path('admin-view-physician/', views.admin_view_physician_view,name='admin-view-physician'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-physician', views.admin_add_physician_view,name='admin-add-physician'),
    path('admin-approve-physician', views.admin_approve_physician_view,name='admin-approve-physician'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-physician-specialisation',views.admin_view_physician_specialisation_view,name='admin-view-physician-specialisation'),


    path('admin-client', views.admin_client_view,name='admin-client'),
    path('admin-view-client/', views.admin_view_client_view,name='admin-view-client'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('physician-dashboard', views.physician_dashboard_view,name='physician-dashboard'),

    path('physician-client', views.physician_client_view,name='physician-client'),
    path('physician-view-client', views.physician_view_client_view,name='physician-view-client'),
    path('physician-view-discharge-client',views.physician_view_discharge_client_view,name='physician-view-discharge-client'),

    path('physician-appointment', views.physician_appointment_view,name='physician-appointment'),
    path('physician-view-appointment', views.physician_view_appointment_view,name='physician-view-appointment'),
    path('physician-delete-appointment',views.physician_delete_appointment_view,name='physician-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='client-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.client_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]