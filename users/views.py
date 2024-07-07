from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm

from innovacare.forms import PhysicianUserForm, PhysicianForm, ClientUserForm, ClientForm, AdminSignupForm
from django.contrib.auth.models import Group

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def physicianclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'physicianclick.html')

def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'clientclick.html')

def physician_signup_view(request):
    userForm = PhysicianUserForm()
    physicianForm = physicianForm()
    mydict = {
        'userForm':userForm,
        'physicianForm':physicianForm
    }
    if request.method == 'POST':
        userForm = PhysicianUserForm(request.POST)
        physicianForm = PhysicianForm(request.POST, request.FILES)
        if userForm.is_valid() and physicianForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            physician = physicianForm.save(commit=False)
            physician.user = user
            physician = physician.save()
            my_physician_group = Group.objects.get_or_create(name='PHYSICIAN')
            my_physician_group[0].user_set.add(user)
        return HttpResponseRedirect('physician_login')
    return render(request, 'physiciansignup.html', context=mydict)


def client_signup_view(request):
    userForm = ClientUserForm()
    clientForm = ClientForm()

    mydict = {
        'userForm':userForm,
        'clientForm':clientForm
        }
    if request.method == 'POST':
        userForm = ClientUserForm(request.POST)
        sellerForm = ClientForm(request.POST, request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            client = clientForm.save(commit=False)
            client.user = user
            client = client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('client_login')
    return render(request, 'clientsignup.html', context=mydict)

def admin_signup_view(request):
    form = AdminSignupForm()
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
        return HttpResponseRedirect('admin_login')
    return render(request, 'admin_signup.html', {'form':form})
            