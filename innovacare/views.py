from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DeleteView, UpdateView, CreateView, DetailView
from django.views import View
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.utils.timezone import now
from django.conf import settings
from innovacare.forms import (
                            AdminSignupForm, 
                            ClientUserForm, 
                            ClientForm, 
                            ClientAppointmentForm, 
                            ContactusForm,
                            PhysicianUserForm, 
                            PhysicianForm, 
                            AppointmentForm,
                            )

# Create your views here.
"""
def home_view(request):
    if request.user.is_authenticated: # checks if the user is authenticated
        return HttpResponseRedirect('afterlogin') # if user is authenticated, it redirects to the 'afterlogin' URL
    return render(request, 'innovacare/index.html') # if user is unauthenticated, it renders and returns the 'index.html' template
"""
class HomeView(View):
    template_name = 'innovacare/index.html'
    redirect_url = 'afterlogin'

    def get(self, request, *args, **kwargs):
        # Handle GET request
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_url)
        return render(request, self.template_name)

#for showing signup/login button for admin
"""
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('innovacare/afterlogin')
    return render(request,'innovacare/adminclick.html')
"""
class AdminClickView(View):
    template_name = 'innovacare/adminclick.html'
    redirect_url = 'innovacare/afterlogin'

    def get(self, request, *args, **kwargs):
        # Handle GET request
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_url)
        return render(request, self.template_name)


#for showing signup/login button for physician
"""
def physicianclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('innovacare/afterlogin')
    return render(request,'innovacare/physicianclick.html')
"""
class PhysicianClickView(View):
    template_name = 'innovacare/physicianclick.html'
    redirect_url = 'innovare/afterlogin'

    def get(self, request, *args, **kwargs):
        # Handle GET request
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_url)
        return render(request, self.template_name)


#for showing signup/login button for client
"""
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('innovacare/afterlogin')
    return render(request,'innovacare/clientclick.html')
"""
class ClientClickView(View):
    template_name = 'innovacare/clientclick.html'
    redirect_url = 'innovacare/afterlogin'

    def get(self, request, *args, **kwargs):
        # Handle GET request
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_url)
        return render(request, self.template_name)

"""
def admin_signup_view(request):
    # Initializes an instance of the AdminSignupForm with no data
    form = AdminSignupForm()
    # Checks if the request method is POST (indicating form submission)
    if request.method=='POST':
        # Reinitialize the form with POST data
        form = AdminSignupForm(request.POST)
        # Check if the form data is valid
        if form.is_valid():
            # Save the form data to create a new user instance but don't commit to the database yet
            user=form.save()
            # Set the user's password (hashes it and saves the hash)
            user.set_password(user.password)
            # Save the user instance to the database
            user.save()
            # Get or create a group named 'ADMIN'
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            # Add the newly created user to the 'ADMIN' group
            my_admin_group[0].user_set.add(user)
            # Redirect the user to the admin login page after successful signup
            return HttpResponseRedirect('/adminlogin/')
    # If the request is not a POST, or if the form is invalid, render the signup form again
    return render(request,'innovacare/adminsignup.html',{'form':form})
"""
class AdminSignupView(FormView):
    template_name = 'innovacare/adminsignup.html'
    form_class = AdminSignupForm
    success_url = '/adminlogin/'

    def form_valid(self, form):
        # Save the form and create a new user instance
        user = form.save(commit=False)
        # Set the user's password
        user.set_password(user.password)
        # Save the user instance to the database
        user.save()
        # Get or create the 'ADMIN' group and add the user to it
        my_admin_group = Group.objects.get_or_create(name='ADMIN')
        my_admin_group[0].user_set.add(user)
        # Redirect to the success URL after successful signup
        return HttpResponseRedirect(self.success_url)

"""
def physician_signup_view(request):
    # Initialize both forms with no data initially
    userForm = PhysicianUserForm()
    physicianForm = PhysicianForm()
    # Prepare the context dictionary to be passed to the template
    mydict={'userForm':userForm,'physicianForm':physicianForm}
    # Check if the request method is POST (indicating form submission)
    if request.method == 'POST':
        # Reinitialize the forms with POST data and file data (for the PhysicianForm)
        userForm = PhysicianUserForm(request.POST)
        physicianForm = PhysicianForm(request.POST,request.FILES)
        # Check if both forms are valid
        if userForm.is_valid() and physicianForm.is_valid():
            # Save the user form to create a new user instance
            user = userForm.save()
            # Set the user's password (hash it)
            user.set_password(user.password)
            # Save the user instance to the database
            user.save()
            # Save the physician form with the user linked to it
            physician = physicianForm.save(commit=False)
            physician.user = user
            physician.save()
            # Add the new user to the 'PHYSICIAN' group
            my_physician_group = Group.objects.get_or_create(name='PHYSICIAN')
            my_physician_group[0].user_set.add(user)
        # Redirect to the physician login page after successful signup
        return HttpResponseRedirect('/physicianlogin/')
    # Render the signup page with the forms
    return render(request,'innovacare/physiciansignup.html',context=mydict)
"""
class PhysicianSignupView(View):
    template_name = 'innovacare/physiciansignup.html'
    user_form_class = PhysicianUserForm
    physician_form_class = PhysicianForm
    success_url = '/physicianlogin/'

    def get(self, request, *args, **kwargs):
        # Initialize empty forms for GET request
        user_form = self.user_form_class()
        physicianForm = self.physician_form_class()
        return render(request, self.template_name, {'userForm':user_form, 'physicianForm':physicianForm})

    def post(self, request, *args, **kwargs):
        # Handle form submission with POST request
        user_form = self.user_form_class(request.POST)
        physicianForm = self.physician_form_class(request.POST, request.FILES)

        if user_form.is_valid() and physicianForm.is_valid():
            # Save user and set password
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Link physician form to user and save
            physician = physicianForm.save(commit=False)
            physician.user = user
            physician.save()
            # Add user to 'PHYSICIAN' group
            my_physician_group = Group.objects.get_or_create(name='PHYSICIAN')
            my_physician_group[0].user_set.add(user)
            # Redirect to the success URL
            return redirect(self.success_url)
        # If forms are invalid, re-render the page with errors
        return render(request, self.template_name, {'userForm':user_form, 'physicianForm':physicianForm})

"""
def client_signup_view(request):
    userForm = ClientUserForm()
    clientForm = ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method == 'POST':
        userForm = ClientUserForm(request.POST)
        clientForm = ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client = clientForm.save(commit=False)
            client.user = user
            #client.assignedPhysicianId=request.POST.get('assignedPhysicianId')
            client = client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('/clientlogin/')
    return render(request,'innovacare/clientsignup.html',context=mydict)
"""
class ClientSignupView(View):
    template_name = 'innovacare/clientsignup.html'
    user_form_class = ClientUserForm
    client_form_class = ClientForm
    success_url = '/clientlogin/'

    def get(self, request, *args, **kwargs):
        # Initialize empty forms for GET request
        user_form = self.user_form_class()
        clientForm = self.client_form_class()
        return render(request, self.template_name, {'userForm':user_form, 'clientForm':clientForm})

    def post(self, request, *args, **kwargs):
        # Handle form submission with POST request
        user_form = self.user_form_class(request.POST)
        clientForm = self.client_form_class(request.POST, request.FILES)

        if user_form.is_valid() and clientForm.is_valid():
            # Save user and set password
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Link client form to user and save
            client = clientForm.save(commit=False)
            client.user = user
            client.save()
            # Add user to 'CLIENT' group
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
            return redirect(self.success_url)
        return render(request, self.template_name, {'userForm':user_form, 'clientForm':clientForm})


#-----------for checking user is physician, client or admin
"""
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_physician(user):
    return user.groups.filter(name='PHYSICIAN').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()
"""
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='ADMIN').exists()
class PhysicianRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='CLIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN, PHYSICIAN OR CLIENT
"""
def afterlogin_view(request):
    # Check if the user is an admin
    if is_admin(request.user):
        return redirect('admin-dashboard')
    # Check if the user is a physician
    elif is_physician(request.user):
        accountapproval=models.Physician.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('physician-dashboard')
        else:
            return render(request,'innovacare/doctor_wait_for_approval.html')
    # Check if the user is a client
    elif is_client(request.user):
        accountapproval=models.Client.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('client-dashboard')
        else:
            return render(request,'innovacare/patient_wait_for_approval.html')
"""
class AfterLoginView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        # Admin user
        if user.groups.filter(name='ADMIN').exists():
            return redirect('admin-dashboard')
        
        # Physician user
        elif user.groups.filter(name='PHYSICIAN').exists():
            accountapproval = models.Physician.objects.filter(user_id=user.id, status=True)
            if accountapproval.exists():
                return redirect('physician-dashboard')
            else:
                return render(request, 'innovacare/physician_wait_for_approval.html')
        
        # Client user
        elif user.groups.filter(name='CLIENT').exists():
            accountapproval = models.Client.objects.filter(user_id=user.id, status=True)
            if accountapproval.exists():
                return redirect('client-dashboard')
            else:
                return render(request, 'innovacare/client_wait_for_approval.html')
        # Default fallback (if user doesn't belong to any expected group)
        return redirect('login')



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # Fetch all physicians and clents, ordered by descending ID (newest first)
    physicians=models.Physician.objects.all().order_by('-id')
    clients=models.Client.objects.all().order_by('-id')
    # Count the number of approved physicians (status=True)
    physiciancount=models.Physician.objects.all().filter(status=True).count()
    # Count the number of pending physicians (status=False)
    pendingphysiciancount=models.Physician.objects.all().filter(status=False).count()
    # Count the number of approved clients (status=True)
    clientcount=models.Client.objects.all().filter(status=True).count()
    # Count the number of pending clients (status=False)
    pendingclientcount=models.Client.objects.all().filter(status=False).count()
    # Count the number of approved appointments
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    # Count the number of pending appointments
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    # Prepare a context dictionary withh all the data for the template
    mydict={
    'physicians':physicians,
    'clients':clients,
    'physiciancount':physiciancount,
    'pendingphysiciancount':pendingphysiciancount,
    'clientcount':clientcount,
    'pendingclientcount':pendingclientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    # Render the admin dashboard template with the context data
    return render(request,'innovacare/admin_dashboard.html',context=mydict)
"""
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/admin_dashboard.html'
    login_url = 'adminlogin'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()
    
    def get_context_data(self, **kwargs):
        # Get the context data for the template
        context = super().get_context_data(**kwargs)

        # Fetch physicians and clients ordered by descending ID
        context['physicians'] = models.Physician.objects.all().order_by('-id')
        context['clients'] = models.Client.objects.all().order_by('-id')

        # Get various counts for physicians, clients, and appointments
        context['physiciancount'] = models.Physician.objects.filter(status=True).count()
        context['pendingphysiciancount'] = models.Physician.objects.filter(status=False).count()

        context['clientcount'] = models.Client.objects.filter(status=True).count()
        context['pendingclientcount'] = models.Client.objects.filter(status=False).count()

        context['appointmentcount'] = models.Appointment.objects.filter(status=True).count()
        context['pendingappointmentcount'] = models.Appointment.objects.filter(status=False).count()

        return context

# this view for sidebar click on admin page
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_physician_view(request):
    # Renders the 'admin_physician.html' template
    return render(request,'innovacare/admin_physician.html')
"""
class AdminPhysicianView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/admin_physician.html'
    login_url = 'adminlogin'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_physician_view(request):
    # Fetch all physicians with status = True (approved physicians)
    physicians=models.Physician.objects.all().filter(status=True)
    # Render the 'admin_view_physician.html
    return render(request,'innovacare/admin_view_physician.html',{'physicians':physicians})
"""
class AdminViewPhysicianView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Physician
    template_name = 'innovacare/admin_view_physician.html'
    context_object_name = 'physicians'
    login_url = 'adminlogin'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()
    
    def get_queryset(self):
        # Filter the physicians to only those with status=True
        return models.Physician.objects.filter(status=True)

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_physician_from_records_view(request,pk):
    # Get the physician object using the primary key (pk)
    physician=models.Physician.objects.get(id=pk)
    # Get the associated user object using the physician's user_id
    user=models.User.objects.get(id=physician.user_id)
    # Delete the user and physician objects from the database
    user.delete()
    physician.delete()
    # Redirect to the 'admin-view-physician' page after deletion
    return redirect('admin-view-physician')
"""

class DeletePhysicianFromRecordsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Physician
    template_name = 'innovacare/admin_confirm_physician_record_delete.html' # Optional: Add a confirmation template
    context_object_name = 'physician'
    success_url = reverse_lazy('admin-view-physician')
    login_url = 'adminlogin'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()
    def delete(self, request, *args, **kwargs):
        # Get the physician object using the primary key (pk) from kwargs
        physician = self.get_object()
        # Get the associated user object using the physician's user_id
        user = models.User.objects.get(id=physician.user_id)
        # Delete the user and physician objects
        user.delete()
        physician.delete()
        return redirect(self.success_url)

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_physician_view(request,pk):
    # Fetch the physician and related user by primary key (pk)
    physician=models.Physician.objects.get(id=pk)
    user=models.User.objects.get(id=physician.user_id)
    # Initialize forms with existing data
    userForm=forms.PhysicianUserForm(instance=user)
    physicianForm=forms.PhysicianForm(request.FILES,instance=physician)
    mydict={'userForm':userForm,'physicianForm':physicianForm}

    # If the request is a POST, updatge the physician and user with the submitted data
    if request.method=='POST':
        userForm=forms.PhysicianUserForm(request.POST,instance=user)
        physicianForm=forms.PhysicianForm(request.POST,request.FILES,instance=physician)
        if userForm.is_valid() and physicianForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            physician=physicianForm.save(commit=False)
            physician.status=True
            physician.save()
            return redirect('admin-view-physician')
    # Render the form for updating physician details
    return render(request,'innovacare/admin_update_physician.html',context=mydict)
"""

class UpdatePhysicianView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Physician
    form_class = PhysicianForm
    template_name = 'innovacare/admin_update_physician.html'
    context_object_name = 'physician'
    success_url = reverse_lazy('admin-view-physician')
    login_url = 'adminlogin'

    # Method to get the form for the related User instance
    def get_user_form(self):
        # Get the User instance associated with the Physician being updated
        user = models.User.objects.get(id=self.get_object().user_id)
        # If the request is POST, return a form bound to the POST data
        if self.request.method == 'POST':
            return PhysicianUserForm(self.request.POST, instance=user)
        else:
            # Otherwise, return a form bound to the existing User instance
            return PhysicianUserForm(instance=user)
    
    # Override the get_context_data method to add additional context
    def get_context_data(self, **kwargs):
        # Get the default context data from the parent class
        context = super().get_context_data(**kwargs)
        # Add the User form to the context dictionary
        context['userForm'] = self.get_user_form()
        # Return the updated context dictionary
        return context
    
    # Override the form_valid method to save both the User and Physician forms
    def form_valid(self, form):
        # Get the User form
        user_form = self.get_user_form()
        # Check if the User form is valid
        if user_form.is_valid():
            # Save the User form and update the password
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        
        # Save the Physician form with the status set to True
        physician = form.save(commit=False)
        physician.status = True
        physician.save()

        # Call the parent class's form_valid method to handle the redirection
        return super().form_valid(form)

    # Override the test_func method to restrict access to Admin users only
    def test_func(self):
        # Check if user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_physician_view(request):
    # Initialize empty forms for creating a new Physician and User
    userForm=forms.PhysicianUserForm()
    physicianForm=forms.PhysicianForm()
    mydict={'userForm':userForm,'physicianForm':physicianForm}
    if request.method=='POST': # If the form is submitted
        # Bind the submitted data to the forms
        userForm=forms.PhysicianUserForm(request.POST)
        physicianForm=forms.PhysicianForm(request.POST, request.FILES)
        if userForm.is_valid() and physicianForm.is_valid(): # Validate the forms
            # Save the User form data to create a new User
            user=userForm.save()
            user.set_password(user.password) # Set the password
            user.save()

            # Save the Physician form data but don't commit yet
            physician=physicianForm.save(commit=False)
            physician.user=user # Associate the user with the physician
            physician.status=True # Set the physician status to active
            physician.save() # Save the Physician to the database

            # Add the user to the 'PHYSICIAN' group
            my_physician_group = Group.objects.get_or_create(name='PHYSICIAN')
            my_physician_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-physician') # Redirect after saving
    return render(request,'innovacare/admin_add_physician.html',context=mydict)
"""
class AdminAddPhysicianView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Define the model to create and the form class
    model = models.Physician
    form_class = PhysicianForm
    template_name = 'innovacare/admin_add_physician.html'
    success_url = reverse_lazy('admin-view-physician')
    login_url = 'adminlogin'

    def get_context_data(self, **kwargs):
        # Get the existing context data from the parent class
        context = super().get_context_data(**kwargs)
        # Add the PhysicianUserForm to the context, either with POST data or as unbound form
        context['userForm'] = PhysicianUserForm(self.request.POST or None)
        # Return the updated context
        return context
    
    def form_valid(self, form):
        # Handle saving of both the User and Physician forms
        # Bind the POST data to the PhysicianUserForm
        userForm = PhysicianUserForm(self.request.POST)
        if userForm.is_valid(): # Validate the user form
            # Save the User form, hash the password, and save it again
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            # Save the Physician form, linking it to the newly created user
            physician = form.save(commit=False)
            physician.user = user
            physician.status = True # Set the physician status to active
            physician.save() # Save the physician instance

            # Add the new user to the 'PHYSICIAN' group
            my_physician_group = Group.objects.get_or_create(name='PHYSICIAN')
            my_physician_group[0].user_set.add(user)
        # Call the parent class's form_valid method to handle redirection
        return super().form_valid(form)
    
    def test_func(self):
        # Restrict access to users in the 'ADMIN' group
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
def admin_approve_physician_view(request):
    # Retrieve all physiciabns whose status is False, meaning they need approval
    physicians=models.Physician.objects.all().filter(status=False)
    # Render the template with the list of physicians needing approval
    return render(request,'innovacare/admin_approve_physician.html',{'physicians':physicians})
"""

class AdminApprovePhysicianView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Physician
    template_name = 'innovacare/admin_approve_physician.html'
    context_object_name = 'physicians'
    login_url = 'adminlogin'

    def get_queryset(self):
        # Return the queryset for physicians needing approval
        return models.Physician.objects.all().filter(status=False)
    
    def test_func(self):
        # Restrict access to users in the 'ADMIN' group
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_physician_view(request,pk):
    # Retrieve the physician object by its primary key (id)
    physician=models.Physician.objects.get(id=pk)
    # Set the physician's status to True, meaning they are approved
    physician.status=True
    # Save the changes to the database
    physician.save()
    # Redirect the user to the admin approval page
    return redirect(reverse('admin-approve-physician'))
"""

class ApprovePhysicianView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Physician
    # Fields to update, in this case, only the 'status' field
    fields = ['status']
    # URL to redirect to after successful approval
    success_url = reverse_lazy('admin-approve-physician')
    login_url = 'adminlogin'

    def form_valid(self, form):
        # Set the physician's status to True (approved)
        form.instance.status = True
        # Save the form an redirect to the success URL
        return super.form_valid(form)
    
    def test_func(self):
        # Restrict access to users in the 'ADMIN' group
        return self.request.user.groups.filter(name='ADMIN').exists()
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_physician_view(request,pk):
    # Retrieve the physician object by its primary key (id)
    physician=models.Physician.objects.get(id=pk)
    # Retrieve the user objects associate with this physician
    user=models.User.objects.get(id=physician.user_id)
    # Delete the user objects associate with this physician
    user.delete()
    # Delete the physician object (removes the physician record)
    physician.delete()
    # Redirect to the admin approval page
    return redirect('admin-approve-physician')
"""

class RejectPhysicianView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Physician
    # URL to redirect to after successful rejection
    success_url = 'admin-approve-physician'
    login_url = 'adminlogin'

    def delete(self, request, *args, **kwargs):
        # Retrieve the physician object by its primary key (id)
        physician = self.get_object()
        # Retrieve the associate user object
        user = models.User.objects.get(id=physician.user_id)
        # Delete the user object (removes the user fro the system)
        user.delete()
        # Delete the physician object (removes the physician record)
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        # Retrieve access to users in the 'ADMIN' group
        return self.request.user.groups.filter(name='ADMIN').exists()
    
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_physician_specialisation_view(request):
    # Retrieve all physicians with a status of True (approved physicians)
    physicians=models.Physician.objects.all().filter(status=True)
    # Render the template with the list of physicians
    return render(request,'innovacare/admin_view_physician_specialisation.html',{'physicians':physicians})
"""

class AdminViewPhysicianSpecialisationView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Physician
    template_name = 'innovacare/admin_view_physician_specialisation.html'
    context_object_name = 'physicians'
    login_url = 'adminlogin'

    def get_queryset(self):
        # Filter the physicians to only those with status=True
        return models.Physician.objects.all().filter(status=True)
    
    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_client_view(request):
    # Render the template for the admin client page
    return render(request,'innovacare/admin_client.html')
"""

class AdminClientView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    # Define the template to render for the admin client page
    template_name = 'innovacare/admin_client.html'
    login_url = 'adminlogin'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_client_view(request):
    # Retrieve all clients with a status of True (approved clients)
    clients=models.Client.objects.all().filter(status=True)
    # Render the template with the list of clients
    return render(request,'innovacare/admin_view_client.html',{'clients':clients})
"""
class AdminViewClientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Client
    template_name = 'innovacare/admin_view_client.html'
    context_object_name = 'clients'
    login_url = 'adminlogin'

    def get_queryset(self):
        # Filter the clients to only those with status=True (approved clients)
        return models.Client.objects.filter(status=True)
    
    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_client_view(request,pk):
    # Retrieve the client object by primary key (pk)
    client = models.Client.objects.get(id=pk)
    # Retrieve the associate user object
    user=models.User.objects.get(id=client.user_id)
    # Delete the user object (removes the client's associated user account)
    user.delete()
    # Delete the client object
    client.delete()
    # Redirect to the 'admin-view-client' page after deletion
    return redirect('admin-view-client')
"""

class DeleteClientView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Client
    template_name = 'innovacare/admin_confirm_client_delete.html'
    success_url = reverse_lazy('admin-view-client')
    login_url = 'adminlogin'

    def delete(self, request, *args, **kwargs):
        # Retrieve the client object  by primary key (pk)
        client = self.get_object()
        # Retrieve the associated user object
        user = models.User.objects.get(id=client.user_id)
        # Delete the user object (removes the client's associated user account)
        user.delete()
        # Delete the client object
        client.delete()
        # Redirect to the success URL after deletion
        return redirect(self.success_url)

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_client_view(request,pk):
    # Retrieve the client object by primary key (pk)
    client = models.Client.objects.get(id=pk)
    # Retrieve the associated user object
    user = models.User.objects.get(id=client.user_id)
    # Initialize forms with existing user and client data
    userForm = forms.ClientUserForm(instance=user)
    clientForm = forms.ClientForm(request.FILES,instance=client)
    mydict={'userForm':userForm,'clientForm':clientForm}

    if request.method=='POST':
        # Populate the forms with the submitted data
        userForm=forms.ClientUserForm(request.POST,instance=user)
        clientForm=forms.ClientForm(request.POST,request.FILES,instance=client)
        # Check if both forms are valid
        if userForm.is_valid() and clientForm.is_valid():
            # Save the user form and update the password
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            # Save the client form, set the status to True, and assign a physician
            client = clientForm.save(commit=False)
            client.status=True
            client.assignedPhysicianId=request.POST.get('assignedPhysicianId')
            client.save()
            # Redirect to the 'admin-view-client' page after updating
            return redirect('admin-view-client')
    # Render the update client template with the form data
    return render(request,'innovacare/admin_update_client.html',context=mydict)
"""
class UpdateClientView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Client
    form_class = ClientForm
    template_name = 'innovacare/admin_update_client.html'
    context_object_name = 'client'
    success_url = reverse_lazy('admin-view-client')
    login_url = 'adminlogin'

    def get_user_form(self):
        # Get the related user form with instance data
        user = models.User.objects.get(id=self.get_object().user_id)
        if self.request.method == 'POST':
            return ClientUserForm(self.request.POST, instance=user)
        else:
            return ClientUserForm(instance = user)
    
    def get_context_data(self, **kwargs):
        # Add the user form to the context data
        context = super().get_context_data(**kwargs)
        context['userForm'] = self.get_user_form()
        return context
    
    def form_valid(self, form):
        # Save the user form
        user_form = self.get_user_form()  
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        # Save the client form and set additional fields
        client = form.save(commit=False)
        client.status = True
        client.save()

        return super().form_valid()

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_client_view(request):
    # Initialize the forms with empty data
    userForm = forms.ClientUserForm()
    clientForm = forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method == 'POST':
        # Populate the forms with the submitted data
        userForm = forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            # Save the user form and update the password
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            # Save the client form and link it to the user
            client = clientForm.save(commit=False)
            client.user=user
            client.status=True
            client.assignedPhysicianId=request.POST.get('assignedPhysicianId')
            client.save()

            # Add the user to the 'CLIENT' group
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-client')
    # Return the add client template with the form data
    return render(request,'innovacare/admin_add_client.html',context=mydict)
"""

class AdminAddClientView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Define the model to create and the form class
    model = models.Client
    form_class = ClientForm
    template_name = 'innovacare/admin_add_client.html'
    success_url = reverse_lazy('admin-view-client')
    login_url = 'adminlogin'

    def get_user_form(self):
        # Method to get the related User form
        if self.request.method == 'POST':
            return ClientUserForm(self.request.POST)
        return ClientUserForm()

    def get_context_data(self, **kwargs):
        # Get the existing context data from the parent class
        context = super().get_context_data(**kwargs)
        # Add the ClientUserForm to the context, either with POST data or as unbound form
        context['userForm'] = self.get_user_form()  # ClientUserForm(self.request.POST or None)
        # Return the updated context
        return context
    
    def form_valid(self, form):
        # Handle saving of both the User and Client forms
        # Bind the POST data to the ClientUserForm
        user_form = self.get_user_form() # ClientUserForm(self.request.POST)
        if user_form.is_valid(): # Validate the user form
            # Save the User form, hash the password, and save it again
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Save the Client form, linking it to the newly created user
            client = form.save(commit=False)
            client.user = user
            client.status = True # Set the client status to active
            client.assignedPhysicianId = self.request.POST.get('assignedPhysicianId')
            client.save() # Save the client instance

            # Add the new user to the 'CLIENT' group
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        # Call the parent class's form_valid method to handle redirection
        return super().form_valid(form)

    def test_fuc(self):
        # Restrict access to users in the 'ADMIN' group
        return self.request.user.groups.filter(name='ADMIN').exists()


#------------------FOR APPROVING CLIENT BY ADMIN----------------------
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_client_view(request):
    # Fetch clients that need approval (status=False)
    clients=models.Client.objects.all().filter(status=False)
    # Render the 'admin_approve_client.html' template with the clients needing approval
    return render(request,'innovacare/admin_approve_client.html',{'clients':clients})
"""

class AdminApproveClientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Client # Model to query for the list view
    template_name = 'innovacare/admin_approve_client.html' # Template to render
    context_object_name = 'clients' # Name of the context variable to pass the queryset
    login_url = 'adminlogin' # Login URL if the user is not authenticated

    def get_queryset(self):
        # Override get_queryset to filter clients needing approval
        return models.Client.objects.filter(status=False)

    def test_func(self):
        # Ensure that only admins can access this view
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_client_view(request,pk):
    client=models.Client.objects.get(id=pk) # Retrieve the Client object with the given primary key (pk)
    client.status=True # Set the status of the client to True (approve the client)
    client.save() # Save the changes to the database
    return redirect(reverse('admin-approve-client')) # Redirect to the 'admin-approve-client' URL
"""

class ApproveClientView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'adminlogin'

    def post(self, request, pk, *args, **kwargs):
        client = models.Client.objects.get(id=pk) # Retrieve the Client object with the given primary key (pk)
        client.status = True # Set the status of the client to True (approve the client)
        client.save() # Save the changes to the database
        return redirect(reverse('admin-approve-client')) # Redirect to the 'admin-approve-client' URL
    
    def test_func(self):
        # Check if ther user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-approve-client')

class RejectClientView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'adminlogin'

    def post(self, request, pk, *args, **kwargs):
        client = models.Client.objects.get(id=pk) # Retrieve the Client object with the given primary key (pk)
        user = models.User.objects.get(id=client.user_id) # Retrieve the User object associated with the Client
        client.delete(); # Delete the Client object
        user.delete() # Delete the User object
        return redirect(reverse('admin-approve-client')) # Redirect to the 'admin-approve-client' URL
    
    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

# Adding confirmation page
def reject_client_view(request, pk):
    client = models.Client.objects.get(id=pk)
    if request.method == 'POST':
        return redirect('reject-client', pk=pk) # Redirect to the reject view if confirmed
    return render(request, 'innovacare/admin_confirm_reject_client.html', {'client':client})
"""
class ConfirmRejectClientView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.Client
    template_name = 'innovacare/admin_confirm_reject_client.html'
    context_object_name = 'client'
    login_url = 'adminlogin'

    def post(self, request, *args, **kwargs):
        # Redirect to the reject view when the form is submitted
        return redirect('confirm-reject-client', pk=self.get_object().id)

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

class RejectClientView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Client
    template_name = 'innovacare/admin_approve_client.html'
    context_object_name = 'client'
    login_url = 'adminlogin'
    success_url = reverse_lazy('admin-approve-client')

    def delete(self, request, pk, *args, **kwargs):
        client = self.get_object()
        user = models.User.objects.get(id=client.user_id) # Retrieve the User object associated with the Client
        client.delete(); # Delete the Client object
        user.delete() # Delete the User object
        return super().delete(request, *args, **kwargs) # Redirect to the 'admin-approve-client' URL
    
    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

#--------------------- FOR DISCHARGING CLIENT BY ADMIN START-------------------------
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_client_view(request):
    clients=models.Client.objects.all().filter(status=True) # Retrieves all clients from the database whose status is 'True'
    return render(request,'innovacare/admin_discharge_client.html',{'clients':clients}) # Render the template. passing the list of active clients as context
"""
class AdminDischargeClientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Client
    template_name = 'innovacare/admin_discharge_client.html'
    context_object_name = 'clients'
    login_url = 'adminlogin'

    def get_queryset(self):
        # Override the default queryset to return only clients with status=True
        clients = models.Client.objects.filter(status=True)
        return clients

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()


"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_client_view(request,pk):
    client = models.Client.objects.get(id=pk) # Retrieves the Client object based on the primary key (pk)
    days = (date.today()-client.admitDate) # Calculates the number of days the client has been admitted
    assignedPhysician = models.User.objects.all().filter(id=client.assignedPhysicianId) # Retrieves the assigned Physician's User object
    d=days.days # Extracts the number of days as an integer
    clientDict={ # Creates a dictionary with client details to pass to the tempalte
        'clientId':pk,
        'name':client.get_name,
        'mobile':client.mobile,
        'address':client.address,
        'symptoms':client.symptoms,
        'admitDate':client.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedPhysicianName':assignedPhysician[0].first_name,
    }
    if request.method == 'POST': # If the request method is POST, meaning the form has been submitted
        feeDict ={ # Creates a dictionary with the billing details
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'physicianFee':request.POST['physicianFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['physicianFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        clientDict.update(feeDict) # Merges the fee details with the client details
        # for updating to database clientDischargeDetails (pDD)
        pDD=models.ClientDischargeDetails()
        pDD.clientId=pk
        pDD.clientName=client.get_name
        pDD.assignedPhysicianName=assignedPhysician[0].first_name
        pDD.address=client.address
        pDD.mobile=client.mobile
        pDD.symptoms=client.symptoms
        pDD.admitDate=client.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.physicianFee=int(request.POST['physicianFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['physicianFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'patient_final_bill.html',context=clientDict) # Renders the final bill with the context
    return render(request,'innovacare/patient_generate_bill.html',context=clientDict) # Renders the bill generation page with the context
"""
class DischargeClientView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'adminlogin'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()
    
    def get(self, request, pk, *args, **kwargs):
        # Retrieve client and calculate days spent
        client = models.Client.objects.get(id=pk)
        days = (now().date() - client.admitDate).days
        assignedPhysician = models.User.filter(id=client.assignedPhysicianId).first()

        # Create context dictionary with client details
        clientDict = {
            'clientId':pk,
            'name':client.get_name,
            'mobile':client.mobile,
            'address':client.address,
            'symptoms':client.symptoms,
            'admitDate':client.admitDate,
            'todayDate':now().date(),
            'day': days,
            'assignPhysicianName':assignedPhysician.first_name,
        }
        return render(request, 'innovacare/patient_generate_bill.html', context=clientDict)
    
    def post(self, request, pk, *args, **kwargs):
        # Retrieve client and calculate days spent
        client = models.Client.objects.get(id=pk)
        days = (now().date() - client.admitDate).days
        assignedPhysician = models.User.objects.filter(id=client.assignedPhysicianId).first()

        # Create context dictionary with client details
        clientDict = {
            'clientId':pk,
            'name':client.get_name,
            'mobile':client.mobile,
            'address':client.address,
            'symptoms':client.symptoms,
            'admitDate':client.admitDate,
            'todayDate':now().date(),
            'day': days,
            'assignPhysicianName':assignedPhysician.first_name,
        }

        # Create fee dictionary from the posted data
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']) * days,
            'physicianFee': request.POST['physicianFee'],
            'medicineCost': request.POST['medicinCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge']) * days) + int(request.POST['physicianFee']) + int(request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        }

        clientDict.update(feeDict) # Update the clientDct with fee details

        # Create and save the ClientDischargeDetails object
        pDD = models.ClientDischargeDetails(
            clientId=pk,
            clientName=client.get_name,
            assignedPhysicianName=assignedPhysician.first_name,
            address=client.address,
            mobile=client.mobile,
            symptons=client.symptoms,
            admitDate=client.admitDate,
            releaseDate=now().date(),
            daySpent=days,
            medicineCost=int(request.POST['medicineCost']),
            roomCharge=int(request.POST['roomCharge']) * days,
            physicianFee=int(request.POST['physicianFee']),
            OtherCharge=int(request.POST['OtherCharge']),
            total=feeDict['total']
        )
        pDD.save() # Save the discharge details

        return render(request, 'innovacare/patient_generate_bill.html', context=clientDict)




#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

"""
def render_to_pdf(template_src, context_dict):
    # 1. Fetch the template specified by 'template_src'
    template = get_template(template_src)
    # 2. Render the template with the provided context dictionary.
    html  = template.render(context_dict)
    # 3. Create an in-memory buffer to hold the PDF data
    result = io.BytesIO()
    # 4. Use 'pisa.pisaDocument' to convert the HTML to a PDF, writing the output to 'result'
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    # 5. Check if there were any errors during PDF generation
    if not pdf.err:
        # 6. If no errors, return an HTTP respons with the PDF content and the appropriate content type
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    # 7. If there were errors, return 'None' (indicating PDF generation failed)
    return None
"""

"""
class RenderToPDFView(View):
    template_name = None # This should be overridden by the view that inherits from this

    def get_context_data(self, **kwargs):
        # Override this method to provide the context for the template
        return 
    
    def render_to_pdf(self, template_src, context_dict):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), context_type='application/pdf')
        return None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_pdf(self.template_name, context)
"""
"""
def download_pdf_view(request,pk):
    # Fetch the most recent ClientDischargeDetails object for the client with the given primary key
    dischargeDetails=models.ClientDischargeDetails.objects.all().filter(clientId=pk).order_by('-id')[:1]
    # 2. Create a dictionary with client details to pass as context to the PDF rendering function
    context_dict={
        'clientName':dischargeDetails[0].clientName,
        'assignedPhysicianName':dischargeDetails[0].assignedPhysicianName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'physicianFee':dischargeDetails[0].physicianFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    # 3. Render the context to a PDF using the template 'innovacare/download_bill.html'
    return render_to_pdf('innovacare/download_bill.html',context_dict)
"""
class DownloadPDFView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.ClientDischargeDetails
    template_name = 'innovacare/download_bill.html'
    context_object_name = 'dischargeDetails'

    def test_func(self):
        # Check if the user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()
    
    def get_object(self, queryset=None):
        # Fetch the most recent ClientDischargeDetails for the given client (pk)
        pk = self.kwargs.get('pk')
        return get_object_or_404(models.ClientDischargeDetails.objects.filter(clientId=pk).order_by('-id'))
    
    def render_to_pdf(template_src, context_dict):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
    
    def render_to_response(self, context, **response_kwargs):
        # 1. Extract discharge details from the context
        dischargeDetails = context['dischargeDetails']
        context_dict={
        'clientName':dischargeDetails[0].clientName,
        'assignedPhysicianName':dischargeDetails[0].assignedPhysicianName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'physicianFee':dischargeDetails[0].physicianFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        # 2. Render the context to a PDF using the template
        pdf = self.render_to_pdf(self.template_name, context_dict)
        # 3. Return the PDF as a response
        return HttpResponse(pdf, content_type='application/pdf')


#-----------------APPOINTMENT START--------------------------------------------------------------------
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'innovacare/admin_appointment.html')
"""
class AdminAppointmentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/admin_appointment.html' # Specify the template to be rendered
    login_url = 'adminlogin' # URL to redirect to if the user is not logged in

    def test_func(self): # Define a custom test function to check if the user is admin
        # Check if the current user belongs to the 'ADMIN' group
        return self.request.user.groups.filter(name='ADMIN').exists()
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    # Retrieve all approved appointments from the database
    appointments=models.Appointment.objects.all().filter(status=True)
    # Render the template with the appointments data
    return render(request,'innovacare/admin_view_appointment.html',{'appointments':appointments})
"""
class AdminViewAppointmentView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Appointment # Specify the model to retrieve data from
    template_name = 'innovacare/admin_view_appointment.html' # Specify the template to render
    context_object_name = 'appointments' # Define the context variable name to use in the template
    login_url = 'adminlogin' # Redirect URL if the user is logged in

    def get_queryset(self):
        appointments = models.Appointment.objects.filter(status=True)
        return appointments

    def test_func(self):
        # Check if the user is an admin; allow access if true
        return self.request.user.groups.filter(name='ADMIN').exists()
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    # Initialize an empty AppointmentForm to be used in the template
    appointmentForm=forms.AppointmentForm()
    # Create a context dictionary to pass the form to the template
    mydict={'appointmentForm':appointmentForm,}
    # Check if the request method is POST (indicating form submission)
    if request.method=='POST':
        # Re-initialize the AppointmentForm with the POST data
        appointmentForm=forms.AppointmentForm(request.POST)
        # Check if the form data is valid
        if appointmentForm.is_valid():
            # Create an appointment object without saving it to th database yet
            appointment=appointmentForm.save(commit=False)

            # Manually set additional fields that are not handled by the form
            appointment.physicianId=request.POST.get('physicianId')
            appointment.clientId=request.POST.get('clientId')
            appointment.physicianName=models.User.objects.get(id=request.POST.get('physicianId')).first_name
            appointment.clientName=models.User.objects.get(id=request.POST.get('clientId')).first_name
            appointment.status=True # Set the appointment status to True (approved)
            # Save th appointment to the database
            appointment.save()
        # Redirect to the 'admin-view-appointment' URL after saving the appointment
        return HttpResponseRedirect('admin-view-appointment')
    # Render the template with the context containing the form
    return render(request,'innovacare/admin_add_appointment.html',context=mydict)
"""
class AdminAddAppointmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Appointment # Specify the model to be used
    form_class = AppointmentForm # Specify the form class to be used
    template_name = 'innovacare/admin_add_appointment.html' # Specify the template to render
    success_url = reverse_lazy('admin-view-appointment') # Redirect to this URL on successful form submission

    def test_func(self):
        # Check if the user is an admin; allow access if true
        return self.request.user.groups.filter(name='ADMIN').exists()
    
    def form_valid(self, form):
        # Create the appointment object without saving it to the database yet
        appointment = form.save(commit=False)

        # Manually set additional fields that are not handled by the form
        appointment.physicianId = self.request.POST.get('physicianId')
        appointment.clientId = self.request.POST.get('clientId')
        appointment.physicianName = models.User.objects.get(id=self.request.POST.get('physicianId')).first_name
        appointment.clientName = models.User.objects.get(id=self.request.POST.get('clientId')).first_name
        appointment.status = True # Set the appointment status to True (approved)

        # Save the appointment to the database
        appointment.save()

        # redirect to the success URL after saving the appointment
        return HttpResponseRedirect(self.get_success_url)
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    # Retrieve all Appointment objects that have a status of False (pending approval)
    appointments=models.Appointment.objects.all().filter(status=False)
    # render the template, passing in the retrieved appointments
    return render(request,'innovacare/admin_approve_appointment.html',{'appointments':appointments})
"""
class AdminApproveAppointmentView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Appointment # Specify the model to be used
    template_name = 'innovacare/admin_approve_appointment.html' # Specify the template to render
    context_object_name = 'appointments' # Set the name of the context variable to be used in the template
    login_url = 'adminlogin' # Redirect to this URL if the user is logged in

    def get_queryset(self):
        # Return the queryset of Appointment objects where status is False (pending approval)
        appointments = models.Appointment.objects.filter(status=False)
        return appointments

    def test_func(self):
        # check if the user is an admin; allow access if true
        return self.request.user.groups.filter(name='ADMIN').exists()
"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk): # Define the function-based view to approve an appointment
    appointment=models.Appointment.objects.get(id=pk) # Retrieve the appointment object using the provided primary key (pk)
    appointment.status=True # Set the status of the appointment to True (approved)
    appointment.save() # Save the changes to the database
    return redirect(reverse('admin-approve-appointment')) # Redirect the user to the admin approval page after the changes are saved
"""
class ApproveAppointmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Appointment # Specify the model being used for the view (Appointment)
    fields = [] # We don't need a form for this view, just updating status directly
    success_url = reverse_lazy('admin-approve-appointment')
    login_url = 'adminlogin'

    def test_func(self):
        # Checks if the current user is an admin
        return self.request.user.groups.filter(name='ADMIN').exists()

    def form_valid(self, form): # This method is called when the form is valid (overrides default method)
        # Get the appointment object that is being  updated
        appointment = self.get_object()
        # Approve the appointment by setting its status to True
        appointment.status = True
        # Save the changes to the database
        appointment.save()
        # Proceed with the default behavior (success redirect)
        return super().form_valid(form)
    
    def get_successful_url(self):
        return self.success_url

"""
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk): # Define a view function to reject an appointment by deleting it
    # Retrieve the appointment object from the database using its primary key (pk)
    appointment=models.Appointment.objects.get(id=pk)
    # Delete the retrieved appointment from the database
    appointment.delete()
    # After delete, redirect the user to the 'admin-approve-appointment' URL
    return redirect('admin-approve-appointment')
"""
class RejectAppointmentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Appointment # Specify the model that this view will be working with (Appointment)
    template_name = 'innovacare/admin_confirm_reject_appointment.html' # Template to confirm deletion (if needed). replace with the correct template path
    login_url = 'adminlogin' # If tnhe user is not logged in, redirect them to the 'adminlogin' page
    success_url = reverse_lazy('admin-approve-appointment')
    
    def test_func(self):
        # Check if the user passes the specified test
        return self.request.user.groups.filter(name='ADMIN').exists()
    
    def get_successful_url(self):
        # After deleting the appointment, redirect to 'admin-approve-appointment'
        return self.success_url
    

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_dashboard_view(request): # Define a view function for the physician's dashboard
    # Count the number of clients assigned to the current logged-in physician
    clientcount=models.Client.objects.all().filter(status=True,assignedPhysicianId=request.user.id).count()
    # Count the number of active appointments for the current logged-in physician
    appointmentcount=models.Appointment.objects.all().filter(status=True,physicianId=request.user.id).count()
    # Count the number of discharged clients associated with the current logged-in physician
    clientdischarged=models.ClientDischargeDetails.objects.all().distinct().filter(assignedPhysicianName=request.user.first_name).count()

    # Retrieve all active appointments for the logged-in physician, oredered by the most recent
    appointments=models.Appointment.objects.all().filter(status=True,physicianId=request.user.id).order_by('-id')
    # Prepare a list to hold the client IDs associated with each appointment
    clientid=[]
    for a in appointments:
        clientid.append(a.clientId) # Append each client's ID to the list
    # Retrieve all active clients whose IDs are in the 'clientid' list, ordered by the most recent
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid).order_by('-id')
    # Combine appointments and their associated clients into pairs using 'zip'
    appointments=zip(appointments,clients)
    # Prepare the context dictionary to pass data to the template
    mydict={
    'clientcount':clientcount,
    'appointmentcount':appointmentcount,
    'clientdischarged':clientdischarged,
    'appointments':appointments,
    'physician':models.Physician.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    # Render the dashboard template with the context data
    return render(request,'innovacare/physician_dashboard.html',context=mydict)
"""
class PhysicianDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/physician_dashboard.html'
    login_url = 'physicianlogin'

    def test_func(self):
        # Check if the user is part of the PHYSICIAN group, allow access if True
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    
    def get_context_data(self, **kwargs): # Method to add custom context data to the view
        # Get the existing context
        context = super().get_context_data(**kwargs)

        # Count the number of clients assigned to the current logged-in physician
        clientcount = models.Client.objects.filter(status=True, assignedPhysicianId=self.request.user.id).count()
        # Count the number of active appointents for the current logged-in physician
        appointmentcount = models.Appointment.objects.filter(status=True, physicianId=self.request.user.id).count()
        # Count the number of discharged clients associated with the current logged-in physician
        clientdischarged = models.ClientDischargeDetails.objects.distinct().filter(assignedPhysicianName=self.request.user.first_name).count()
        # Retrieve all active appointments for the loggedd-in physician, ordered by the most recent
        appointments = models.Appointment.objects.all().filter(status=True, physicianId=self.request.user.id).order_by('-id')

        # Prepare a list to hold the client IDs associated with each appointment
        clientid = []
        for a in appointments:
            clientid.append(a.clientId) # Append each client's ID to the list
        # Retrieve all active clients whose IDs are in the 'clientid' list, ordered by the most recent
        clients = models.Client.objects.all().filter(status=True, user_id__in=clientid).order_by('-id')

        # Combine appointments and their associated clients into pairs using 'zip'
        appointments = zip(appointments, clients)
        # Add all the calculated data to the context
        context['clientcount'] = clientcount
        context['appointmentcount'] = appointmentcount
        context['clientdoscharged'] = clientdischarged
        context['appointments'] = appointments
        context['physician'] = models.Physician.objects.get(user_id=self.request.user.id) # Get the logged-in physician's details (for profile picture, etc.)

        return context # Return the updated context

"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_client_view(request):
    # Create a dictionary to pass context to the template
    mydict={
    'physician':models.Physician.objects.get(user_id=request.user.id), # Get the Physician object for the logged-in user to display their profile picture in the sidebar
    }
    # Render the template with the context dictionary
    return render(request,'innovacare/physician_client.html',context=mydict)
"""
class PhysicianClientView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/physician_client.html'
    login_url = 'physicianlogin'

    def test_func(self):
        # Check if the user belongs to PHYSICIAN groups, allow access if True
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    
    def get_context_data(self, **kwargs): # Method to add custom context data to the view
        context = super().get_context_data(**kwargs) # Get the existing content
        # Fetch the physician's data based on the logged-in user's ID for displaying their profile picture
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        context['physician'] = physician
        return context # Return the updated context to be passed to the template

"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_view_client_view(request):
    # Query all Client objects that have status=True and are assigned to the currently logged-in Physician
    clients=models.Client.objects.all().filter(status=True,assignedPhysicianId=request.user.id)
    # Get the Physician object for the logged-in user (used to display the profile picture in the sidebar)
    physician=models.Physician.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # Render the template, passing the clients and physician objects
    return render(request,'innovacare/physician_view_client.html',{'clients':clients,'physician':physician})

# Alternative Generic Class-based Views
class PhysicianViewClientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Client
    template_name = 'innovacare/physician_view_client.html' # Specify the template to be used
    context_object_name = 'clients' # The context variable name to use in the template for the list of clients
    login_url = 'physicianlogin' # URL to redirect to if the user is not logged in

    def get_queryset(self):
        # Query to get all Client objects that have status=True and are assigned to the currently logged-in physician
        return models.Client.objects.all().filter(status=True, assignedPhysicianId=self.request.user.id)

    # Method to check if the user is a physician
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    
    def get_context_data(self, **kwargs):
        # Get the default context data from the parent class (which inclues the client list)
        context = super().get_context_data(**kwargs)

        # Add the physician object to the context for displaying the profile picture in the sidebar
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        context['physician'] = physician
        return context
"""
# get_queryset() is used to define the query for retrieving the data that will be used in the view
# get_context_data() is used to add extra context variables to the template
class PhysicianViewClientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Client
    template_name = 'innovacare/physician_view_client.html' # Specify the template to be used
    context_object_name = 'clients' # The context variable name to use in the template for the list of clients
    login_url = 'physicianlogin' # URL to redirect to if the user is not logged in

    # Method to check if the user is a physician
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    
    def get_context_data(self, **kwargs):
        # Get the default context data from the parent class
        context = super().get_context_data(**kwargs)
        # Perform the query for clients directly in get_context_data
        clients = models.Client.objects.all().filter(status=True, assignedPhysicianId=self.request.user.id)
        # Add the physician object to the context for displaying the profile picture in the sidebar
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        context['clients'] = clients
        context['physician'] = physician
        return context
"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_view_discharge_client_view(request):
    # Query the ClientDischargeDetails model for all distinct entries where the assigned physician's name matches the current user's first name
    dischargedclients=models.ClientDischargeDetails.objects.all().distinct().filter(assignedPhysicianName=request.user.first_name)
    # Query the Physician model to get the current physician's details, used for profile picture
    physician=models.Physician.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # Render the template with the context containing the discharged clients and physician details
    return render(request,'innovacare/physician_view_discharge_client.html',{'dischargedclients':dischargedclients,'physician':physician})
"""
class PhysicianViewDischargeClientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.ClientDischargeDetails # Specify the primary model this view is working
    template_name = 'innovacare/physician_view_discharge_client.html' # Template to render
    context_object_name = 'dischargedclients' # Name of the context variable for the discharged clients
    login_url = 'physicianlogin' # URL to redirect to if the user is not logged in

    # Method to check if the user is a physician
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    
    def get_queryset(self):
        # Filter the ClientDischargeDetails where the assigned physician's name matches the current user's first name
        return super().get_queryset().distinct().filter(assignedPhysicianName=self.request.user.first_name)
    
    # Add additional context context data to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the physician object to the context for displaying the profile picture in the sidebar
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        context['physician'] = physician
        # Return the updated context with discharged clients and physician details
        return context

"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_appointment_view(request):
    # Retrieve the current physician's details based on the logged-in user
    physician=models.Physician.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # Render the template, passing the physician details to the template
    return render(request,'innovacare/physician_appointment.html',{'physician':physician})
"""
class PhysicianAppointmentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/physician_appointment.html'
    login_url = 'physicianlogin'

    # Method to check if the user is a physician
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    # Add context data to the template
    def get_context_data(self, **kwargs):
        # Start with the default context data
        context = super().get_context_data(**kwargs)
        # Add the physician object to the context for displaying the profile picture in the sidebar
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        context['physician'] = physician
        # Return the updated context with the physician details 
        return context


"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_view_appointment_view(request):
    # Retrieve the current physician's details based on the logged-in user
    physician=models.Physician.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # Retrieve all the appointments for the logged-in physician that have a status of True
    appointments=models.Appointment.objects.all().filter(status=True, physicianId=request.user.id)
    # Create a list to hold client IDs associated with the Physician's appointments
    clientid=[]
    # Loop through each appointment and append the corresponding client ID to the list
    for a in appointments:
        clientid.append(a.clientId)
    # Retrieve the clients whose IDs are in the clientid list and who have an active status
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid)
    # Zip the appointments and clients together for paired iteration in the template
    appointments=zip(appointments,clients)
    # Render the template, passing the appointments and physician details
    return render(request,'innovacare/physician_view_appointment.html',{'appointments':appointments,'physician':physician})
"""
class PhysicianViewAppointmentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/physician_view_appointment.html'
    login_url = 'physicianlogin'

    # Method to check if the user is a physician
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    # Add context data to the template
    def get_context_data(self, **kwargs):
        # Start with the default context data
        context = super().get_context_data(**kwargs)
        # Retrieive the current physician's details based on the logged-in user
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        # Retrieve the all the appointments for the logged-in physician that have a status of True
        appointments = models.Appointment.objects.all().filter(status=True, physicianId=self.request.user.id)
        # Create a list to hold client IDs associated with the physician's appointments
        clientid = [a.clientId for a in appointments]
        # Retrieive the clients whose IDs are in the clientid list and who have an active status
        clients = models.Client.objects.all().filter(status=True, user_id__in=clientid)
        # Zip the appointments and clients together for paired iteration in the templlate
        appointments = zip(appointments, clients)
        context['physician'] = physician
        context['appointments'] = appointments
        context['clients'] = clients
        # Return the updagted context with the physician details and appointments
        return context

"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def physician_delete_appointment_view(request):
    # Retrieve the physician's details based on the logged-in user (used for the sidebar profile picture)
    physician=models.Physician.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # Retrieve all appointments forthe current physician thatr have an active status (status=True)
    appointments=models.Appointment.objects.all().filter(status=True,physicianId=request.user.id)
    # Create a list to store clients IDs associated with theappointments
    clientid=[]
    # Loop through each appointment and append the clientId to the list
    for a in appointments:
        clientid.append(a.clientId)
    # retrieve clients whose IDs are in the clientid list and have an active status
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid)
    # Zip the appointments and clients together so they can be displayed in the template side by side
    appointments=zip(appointments,clients)
    # Render the template, passing the appointments and physician details
    return render(request,'innovacare/physician_delete_appointment.html',{'appointments':appointments,'physician':physician})
"""
class PhysicianDeleteAppointmentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/physician_delete_appointment.html' # Specify the template to render
    login_url = 'physicianlogin' # URL to redirect to if the user is not logged in 
    # Method to check if the user is a physician
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    # Overide get_context_data to add context for the templates
    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)
        # Retrieve the current physician's details based on the logged-in user
        physician = models.Physician.objects.get(user_id=self.request.user.id)
        # Retrieve all appointments for the logged-in physician that have an active status
        appointments = models.Appointment.objects.all().filter(status=True, physicianId=self.request.user.id)
        # Create a list to hold client IDs associated with the appointments
        clientid = [a.clientId for a in appointments]
        # Retrieve clients whose IDs are in the clientid listand have an active status
        clients = models.Client.objects.all().filter(status=True, user_id__in=clientid)
        # Zip the appointments and client together for displaying them in the template
        appointments = zip(appointments, clients)
        context['physician'] = physician
        context['appointments'] = appointments
        context['clients'] = clients
        # Return the updated context
        return context


"""
@login_required(login_url='physicianlogin')
@user_passes_test(is_physician)
def delete_appointment_view(request,pk):
    # Get the appointment based on the provided primary key (pk) and delete it
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    # Retrieve the physician's details based on the logged-in user (used for the sidebar profile)
    physician=models.Physician.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # Retrieve all appointments with an active status for the logged-in physician
    appointments=models.Appointment.objects.all().filter(status=True,physicianId=request.user.id)
    clientid = [a.clientId for a in appointments]
    # Retrieive clients whose IDs are in the patientid list and have an active status
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid)
    # Zip the appointments and clients together so they can be displayed in the template side profile
    appointments=zip(appointments,clients)
    # Render the template with the list of appointments and the physician details
    return render(request,'innovacare/doctor_delete_appointment.html',{'appointments':appointments,'physician':physician})
"""
class DeleteAppointmentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Appointment
    template_name = 'innovacare/doctor_delete_appointment.html'
    success_url = reverse_lazy('physician_delete_appointment') # Redirect to a sucess URL after deletion
    login_url = 'physicianlogin' # URL to redirect to if the user is not logged in

    # Ensure that only physicians can access this view
    def test_func(self):
        return self.request.user.groups.filter(name='PHYSICIAN').exists()
    
    # Override get_object to retrieve the specific appointment using the primary key (pk)
    def get_object(self, queryset=None):
        # Get the appointment by ID (pk), or return a 404 if not found
        appointment = get_object_or_404(models.Appointment, id=self.kwargs['pk'])
        return appointment
    
    # Override get_context_data to add additional context for the template
    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Retrieve the physician's details based on the logged-in user
        context['physician'] = models.Physician.objects.get(user_id=self.request.user.id)
        # Retrieve all appointments for the logged-in physician with an active status
        appointments = models.Appointment.objects.filter(status=True, physicianId=self.request.user.id)
        # Get the list of client IDs associated with the physician's appointments
        clientid = [a.clientId for a in appointments]
        # Retrieve all clients whose user IDs are in the clientid list and have an active status
        context['clients'] = models.Client.objects.filter(status=True, user_id__in=clientid)
        # Zip the appointments and clients together to display them in the template side by side
        context['appointments'] = zip(appointments, context['clients'])
        # Return the updated context
        return context

#---------------------------------------------------------------------------------
#------------------------ PHYSICIAN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ CLIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
"""
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_dashboard_view(request):
    # Retrieive the Client instance associated with the logged-in user
    client=models.Client.objects.get(user_id=request.user.id)
    # Retrieive the assigned physician's information if needed (currently commented out)
    #physician=models.Physician.objects.get(user_id=client.assignedPhysicianId)
    # Create a context dictionary to pass client and physician details to the template
    mydict={
    'client':client,
    # The physician's details (currently commented out) could be added to the context if needed
    #'physicianName':physician.get_name,
    #'physicianMobile':physician.mobile,
    #'physicianAddress':physician.address,
    #'symptoms':client.symptoms,
    #'physicianDepartment':physician.department,
    #'admitDate':client.admitDate,
    }
    # Render the template with the context dictionary
    return render(request,'innovacare/client_dashboard.html',context=mydict)
"""
class ClientDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/client_dashboard.html'
    login_url = 'clientlogin'

    # Ensure that only clients can access this view
    def test_func(self):
        # Check if the user is belong to the Client group, allow access if True
        return self.request.user.groups.filter(name='CLIENT').exists()
    
    # Override the get_context_data method to pass data to the template
    def get_context_data(self, **kwargs):
        # Get the default context data (if any)
        context = super().get_context_data(**kwargs)
        # Retrieive the Client instance associated with the logged-in user
        client = models.Client.objects.get(user_id=self.request.user.id)
        # Add the client information to the context
        context['client'] = client
        # If needed, you could also retrieive the assigned physician's information and add it to the context (currently commented out)
        # physician = models.Physician.objects.get(user_id=client.assignedPhysicianId)
        # context.update({
        #'physicianName':physician.get_name,
        #'physicianMobile':physician.mobile,
        #'physicianAddress':physician.address,
        #'symptoms':client.symptoms,
        #'physicianDepartment':physician.department,
        #'admitDate':client.admitDate,})
        # Return the updated context to the template
        return context

"""
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_appointment_view(request):
    # Retrieive the Client instance associated with the logged-in user (used to display the profile)
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    # Render the template and pass the client object to thr context
    return render(request,'innovacare/client_appointment.html',{'client':client})
"""
class ClientAppointmentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/client_appointment.html'
    login_url = 'clientlogin'

    # Ensure that only clients can access this view
    def test_func(self):
        # Check if the user is belong to the CLIENT group, allow access if True
        return self.request.user.groups.filter(name='CLIENT').exists()
    
    # Override the get_context_data method to pass data to the template
    def get_context_data(self, **kwargs):
        # Get the default context data (if any)
        context = super().get_context_data(**kwargs)
        # Retrieive the Client instance associated with the logged-in user (for the profile)
        client = models.Client.objects.get(user_id=self.request.user.id)
        # Add the client information to the context
        context['client'] = client
        # Return the updated context
        return context

"""
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_book_appointment_view(request):
    # Initialize the appointment form for the client
    appointmentForm=forms.ClientAppointmentForm()
    # Retrieve the Client instance associated with the logged-in user (used to display the profile picture)
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    # Create a dictionary to pass the form and client information to the template
    mydict={'appointmentForm':appointmentForm,'client':client}
    # If the form is submitted via a POST request
    if request.method=='POST':
        # Re-initialize the form with the submitted data
        appointmentForm=forms.ClientAppointmentForm(request.POST)
        # Check if the form data is valid
        if appointmentForm.is_valid():
            # Save the form data to create an appointment object, but don't commit to the database yet
            appointment=appointmentForm.save(commit=False)
            # Set the physician ID based on the submitted form data
            appointment.physicianId=request.POST.get('physicianId')
            # Set the client ID to the logged-in user's ID
            appointment.clientId=request.user.id #----user can choose any patient but only their info will be stored
            # Set the physician's name based on the selected physician in the form
            appointment.physicianName=models.User.objects.get(id=request.POST.get('physicianId')).first_name
            # Set the client's name based on the logged-in user's name
            appointment.clientName=request.user.first_name #----user can choose any patient but only their info will be stored
            # Set the appointment status to False (pending approval)
            appointment.status=False
            # Save the appointment to the database
            appointment.save()
        # Redirect to the 'patient-view-appointment' page after form submission
        return HttpResponseRedirect('patient-view-appointment')
    # Render the template and pass the form and client information
    return render(request,'innovacare/patient_book_appointment.html',context=mydict)
"""
class ClientBookAppointmentView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    # Specify the form class to be used
    form_class = ClientAppointmentForm
    # Set the template to be rendered
    template_name = 'innovacare/patient_book_appointment.html'
    # Set the login URL for clientsif not logged in
    login_url = 'clientlogin'

    # Override the test_func method to ensure only clients can access this view
    def test_func(self):
        return self.request.user.groups.filter(name='CLIENT').exists()
    
    # Override the get_context_data method to pass additional context to the template
    def get_context_data(self, **kwargs):
        # Get the default context data (if any)
        context = super().get_context_data(**kwargs)

        # Retrieive the client instance associated with the logged-in user for the profile
        context['client'] = models.Client.objects.get(user_id=self.request.user.id)
        # Return the updated context to the template
        return context
    
    # Handle form submission for booking an appointment (POST request)
    def form_valid(self, form):
        # Save the form data but don't commit to the database yet
        appointment = form.save(commit=False)
        # Set the physician ID from the POST data
        appointment.physicianId = self.request.POST.get('physicianId')
        # Set the client ID to the logged-in client's ID
        appointment.clientId = self.request.user.id
        # Set the physician's name based on the selected physician
        appointment.physicianName = models.User.objects.get(id=self.request.POST.get('physicianId')).first_name
        # Set the client's name to the logged-in user's first name
        appointment.clientName = self.request.user.first_name
        # Set the appointment status to False (pending)
        appointment.status = False
        # Save the appointment to the database
        appointment.save()
        # Redirect to the 'patient-view-appointment' page after successful form submission
        return HttpResponseRedirect(reverse('patient-view-appointment'))

"""
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_view_appointment_view(request):
    # Retrieve the Client instance associatedwith the logged-in user (for profile picture)
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    # Get all appointments that belong to the logged-in client
    appointments=models.Appointment.objects.all().filter(clientId=request.user.id)
    # Render the template
    return render(request,'innovacare/patient_view_appointment.html',{'appointments':appointments,'client':client})
"""
class ClientViewAppointmentView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Appointment
    context_object_name = 'appointments'
    template_name = 'innovacare/client_view_appointment.html'
    login_url = 'clientlogin'

    def test_func(self):
        # Check if user is belong to the CLIENT group, allow access if True
        return self.request.user.groups.filter(name='CLIENT').exists()
    
    # Override the get_queryset method to filter appointments by the logged-in client
    def get_queryset(self):
        # Return the queryset filtered to only show appointments for the logged-in client
        return models.Appointment.objects.filter(clientId=self.request.user.id)
    # Override the get_context_data method to pass additional data to the template
    def get_context_data(self, **kwargs):
        # Get the default context data (if any)
        context = super().get_context_data(**kwargs)
        # Retrieive the client instance associated with the logged-in user for the profile picture
        client = models.Client.objects.get(user_id=self.request.user.id)
        context['client'] = client
        return context
"""
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_discharge_view(request):
    # Retrieive the Client instance associated with the logged-in user (for profile picture)
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    # Retrieive the most recent discharge details for the logged-in client, ordering by desacending ID and limiting to 1
    dischargeDetails=models.ClientDischargeDetails.objects.all().filter(clientId=client.id).order_by('-id')[:1]
    # Initialize a variable to hold discharge details to be passed to the template
    clientDict=None
    # Check if there are discharge details available for the client
    if dischargeDetails:
        # If discharge details exist, construct a dictionary with all required data
        patientDict ={
        'is_discharged':True,
        'client':client,
        'clientId':client.id,
        'pclientName':client.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':client.address,
        'mobile':client.mobile,
        'symptoms':client.symptoms,
        'admitDate':client.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        # Optional print statement for debugging (can be removed in production)
        print(patientDict)
    else:
        # If no discharge details, create a default dictionary indicating that the client is not discharged
        clientDict={
            'is_discharged':False,
            'client':client,
            'clientId':request.user.id,
        }
    return render(request,'innovacare/patient_discharge.html',context=clientDict)
"""

class ClientDischargeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'innovacare/patient_discharge.html'
    login_url = 'clientlogin'

    # Ensure only clients can access this view
    def test_func(self):
        return self.request.user.groups.filter(name='CLIENT').exists()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        # Retrieve the Client instance associated with the logged-in user for the sidebar/profile
        client = models.Client.objects.get(user_id=self.request.user.id)
        # Retrieive the most recent discharge details for the client, ordering by descending ID, limiting to 1
        discharge_details = models.ClientDischargeDetails.objects.filter(clientId=client.id).order_by('-id')[:1]

        # Check if the client has any discharge details
        if discharge_details:
            # If discharge details exist, construct a dictionary with all required data
            context['is_discharged'] = True
            context['client'] = client
            context['clientId'] = client.id
            context['clientName'] = client.get_name
            context['assignedDoctorName'] = discharge_details[0].assignedDoctorName
            context['address'] = client.address
            context['mobile'] = client.mobile
            context['symptoms'] = client.symptoms
            context['admitDate'] = client.admitDate
            context['releaseDate'] = discharge_details[0].releaseDate
            context['daySpent'] = discharge_details[0].daySpent
            context['medicineCost'] = discharge_details[0].medicineCost
            context['roomCharge'] = discharge_details[0].roomCharge
            context['doctorFee'] = discharge_details[0].doctorFee
            context['OtherCharge'] = discharge_details[0].OtherCharge
            context['total'] = discharge_details[0].total
        else:
            # If no discharge details, pass a default context indicating the client is not discharged
            context['is_discharged'] = False
            context['client'] = client
            context['clientId'] = self.request.user.id
        
        return context

#------------------------ CLIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
"""
def aboutus_view(request):
    return render(request,'innovacare/aboutus.html')
"""
class AboutUsView(TemplateView):
    template_name = 'innovacare/aboutus.html'

def contactus_view(request):
    # Create an instance of the ContactusForm
    sub = forms.ContactusForm()
    # Check if the form is submitted via POST method
    if request.method == 'POST':
        # Recreate the form with the submitted data
        sub = forms.ContactusForm(request.POST)
        # Validate the form data
        if sub.is_valid():
            # Extract the cleaned data from the form
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            # Send an email with the form details
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            # Render the success page after sending the email
            return render(request, 'innovacare/contactussuccess.html')
    # Render the contact form page
    return render(request, 'innovacare/contactus.html', {'form':sub})

class ContactUsView(FormView):
    # Specify the form class
    form_class = ContactusForm
    # Specify the template to render
    template_name = 'innovacare/contactus.html'
    # Success URL to redirect upon successful form submission
    success_url = reverse_lazy('contactus_success')

    # Process the form submission
    def form_valid(self, form):
        # Extract data from the form
        email = form.cleaned_data['Email']
        name = form.cleaned_data['Name']
        message = form.cleaned_data['Message']

        # Send an email with the form data
        send_mail(
            str(name) + ' || ' + str(email), # Email subject
            message, # Email message body
            settings.EMAIL_HOST_USE, # Sender email
            settings.EMAIL_RECEIVING_USER, # Recipient email
            fail_silently = False # Raise error if sending fails
        )
        # Return the default form_valid behavior (redirect to success URL)
        return super().form_valid(form)


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
