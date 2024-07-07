from django import forms
from django.contrib.auth import get_user_model
from django.db import models
from .models import Physician, Client, Appointment

# Create your models here.
class PhysicianUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }

class PhysicianForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = ['address', 'mobile', 'title', 'status', 'profile_pic']


class ClientUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['address', 'mobile', 'health_details', 'profile_pic']


class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }

class AppointmentForm(forms.ModelForm):
    physicianId = forms.ModelChoiceField(queryset=Physician.objects.all().filter(status=True),empty_label="Physician Name and Title", to_field_name="user_id")
    clientId = forms.ModelChoiceField(queryset=Client.objects.all().filter(status=True),empty_label="Client Name and Health Status", to_field_name="user_id")
    class Meta:
        model = Appointment
        fields=['description','status']


class ClientAppointmentForm(forms.ModelForm):
    physicianId = forms.ModelChoiceField(queryset=Physician.objects.all().filter(status=True),empty_label="Physician Name and Title", to_field_name="user_id")
    class Meta:
        model= Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))