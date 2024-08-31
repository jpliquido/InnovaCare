from django.contrib import admin
from django.urls import path
from innovacare import views
from django.contrib.auth.views import LoginView,LogoutView
from .views import (
                    AdminAddPhysicianView,
                    AdminClickView,
                    AdminDashboardView,
                    AdminPhysicianView,
                    AdminSignupView,
                    AdminViewPhysicianView,
                    AfterLoginView,
                    ClientClickView,
                    ClientSignupView,
                    DeletePhysicianFromRecordsView,
                    HomeView,
                    PhysicianClickView,
                    PhysicianSignupView,
                    UpdatePhysicianView,
                    AdminApprovePhysicianView,
                    ApprovePhysicianView,
                    RejectPhysicianView,
                    AdminViewPhysicianSpecialisationView,
                    AdminClientView,
                    AdminViewClientView,
                    DeleteClientView,
                    UpdateClientView,
                    AdminAddClientView,
                    AdminApproveClientView,
                    ApproveClientView,
                    RejectClientView,
                    ConfirmRejectClientView,
                    AdminDischargeClientView,
                    DischargeClientView,
                    AdminAppointmentView,
                    AdminViewAppointmentView,
                    AdminAddAppointmentView,
                    AdminApproveAppointmentView,
                    )


#-------------FOR ADMIN RELATED URLS ------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home_view,name='home'),
    path('', HomeView.as_view(), name='home'),

    path('aboutus/', views.aboutus_view, name='about-us'),
    path('contactus/', views.contactus_view, name='contact-us'),

    # path('adminclick/', views.adminclick_view, name='adminclick'),
    path('adminclick/', AdminClickView.as_view(), name='adminclick'),
    # path('physicianclick/', views.physicianclick_view, name='physicianclick'),
    path('physicianclick/', PhysicianClickView.as_view(), name='physicianclick'),

    # path('clientclick/', views.clientclick_view, name='clientclick'),
    path('clientclick/', ClientClickView.as_view(), name='clientclick'),

    # path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path('adminsignup/', AdminSignupView.as_view(), name='adminsignup'),
    # path('physiciansignup/', views.physician_signup_view,name='physiciansignup'),
    path('physiciansignup/', PhysicianSignupView.as_view(), name='physiciansignup'),
    # path('clientsignup/', views.client_signup_view, name='clientsignup'),
    path('clientsignup/', ClientSignupView.as_view(), name='clientsignup'),
    
    path('adminlogin/', LoginView.as_view(template_name='innovacare/adminlogin.html'), name='adminlogin'),
    path('physicianlogin/', LoginView.as_view(template_name='innovacare/physicianlogin.html'), name='physicianlogin'),
    path('clientlogin/', LoginView.as_view(template_name='innovacare/clientlogin.html'), name='clientlogin'),

    # path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('afterlogin/', AfterLoginView.as_view(), name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='index.html'),name='logout'),

    # path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-dashboard', AdminDashboardView.as_view(), name='admin-dashboard'),

    # path('admin-physician/', views.admin_physician_view,name='admin-physician'),
    path('admin-dashboard', AdminPhysicianView.as_view(), name='admin-physician'),
    # path('admin-view-physician/', views.admin_view_physician_view,name='admin-view-physician'),
    path('admin-view-physician/', AdminViewPhysicianView.as_view(), name='admin-view-physician'),
    # path('delete-physician-from-records/<int:pk>', views.delete_physician_from_records_view,name='delete-physician-from-records'),
    path('delete-physician-from-records/<int:pk>', DeletePhysicianFromRecordsView.as_view(), name='delete-physician-from-records'),
    # path('update-physician/<int:pk>', views.update_physician_view,name='update-physician'),
    path('update-physician/<int:pk>', UpdatePhysicianView.as_view(), name='update-physician'),
    # path('admin-add-physician', views.admin_add_physician_view,name='admin-add-physician'),
    path('admin-add-physician', AdminAddPhysicianView.as_view(), name='admin-add-physician'),
    #path('admin-approve-physician', views.admin_approve_physician_view,name='admin-approve-physician'),
    path('admin-approve-physician', AdminApprovePhysicianView.as_view(), name='admin-approve-physician'),
    # path('approve-physician/<int:pk>', views.approve_physician_view,name='approve-physician'),
    path('approve-physician/<int:pk>', ApprovePhysicianView.as_view(), name='approve-physician'),
    # path('reject-physician/<int:pk>', views.reject_physician_view,name='reject-physician'),
    path('reject-physician/<int:pk>', RejectPhysicianView.as_view(), name='reject-physician'),
    # path('admin-view-physician-specialisation',views.admin_view_physician_specialisation_view,name='admin-view-physician-specialisation'),
    path('admin-view-physician-specialisation', AdminViewPhysicianSpecialisationView.as_view(), name='admin-view-physician-specialisation'),

    # path('admin-client', views.admin_client_view,name='admin-client'),
    path('admin-client', AdminClientView.as_view(), name='admin-client'),
    # path('admin-view-client/', views.admin_view_client_view,name='admin-view-client'),
    path('admin-view-client', AdminViewClientView.as_view(), name='admin-view-client'),
    # path('delete-client/<int:pk>/', views.delete_client_view,name='delete-client'),
    path('delete-client/<int:pk>/', DeleteClientView.as_view(), name='delete-client'),
    # path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('update-client-view/<int:pk>', UpdateClientView.as_view(), name='update-client'),
    # path('admin-add-client/', views.admin_add_client_view,name='admin-add-client'),
    path('admin-add-client/', AdminAddClientView.as_view(), name='admin-add-client'),
    # path('admin-approve-client/', views.admin_approve_client_view,name='admin-approve-client'),
    path('admin-approve-client/', AdminApproveClientView.as_view(), name='admin-approve-client'),
    # path('approve-client/<int:pk>', views.approve_client_view,name='approve-client'),
    path('approve-client/<int:pk>', ApproveClientView.as_view(), name='approve-client'),
    # path('reject-client/<int:pk>', views.reject_client_view,name='reject-client'),
    path('confirm-reject-client/<int:pk>', ConfirmRejectClientView.as_view(), name='confirm-reject-client'),
    path('reject-client/<int:pk>', RejectClientView.as_view(), name='reject-client'),
    # path('admin-discharge-client/', views.admin_discharge_client_view,name='admin-discharge-client'),
    path('admin-discharge-client/', AdminDischargeClientView.as_view(), name='admin-discharge-client'),
    # path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('discharge-client/<int:pk>', DischargeClientView.as_view(), name='discharge-client'),
    # path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

    # path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-appointment', AdminAppointmentView.as_view(), name='admin-appointment'),
    # path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-view-appointment', AdminViewAppointmentView.as_view(), name='admin-view-appointment'),
    # path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-add-appointment', AdminAddAppointmentView.as_view(), name='admin-add-appointment'),
    # path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('admin-approve-appointment', AdminApproveAppointmentView.as_view(), name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR PHYSICIAN RELATED URLS-------------------------------------
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


#---------FOR CLIENT RELATED URLS-------------------------------------
urlpatterns +=[
    path('client-dashboard', views.client_dashboard_view,name='client-dashboard'),
    path('client-appointment', views.client_appointment_view,name='client-appointment'),
    path('client-book-appointment', views.client_book_appointment_view,name='client-book-appointment'),
    path('client-view-appointment', views.client_view_appointment_view,name='client-view-appointment'),
    path('client-discharge', views.client_discharge_view,name='client-discharge'),

]