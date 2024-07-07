from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
title = [('Primary Care Physician','Primary Care Physician'),
         ('Specialist', 'Specialist')]

class Physician(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/PhysicianProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    title = models.CharField(max_length=50,choices=title,default='Primary Care Physician')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.title)

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/ClientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    health_details = models.CharField(max_length=500,null=False)
    assignedPhysicianId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.health_details+")"
    
class Appointment(models.Model):
    clientId = models.PositiveIntegerField(null=True)
    physicianId = models.PositiveIntegerField(null=True)
    clientName = models.CharField(max_length=40,null=True)
    physicianName = models.CharField(max_length=40,null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

class ClientDischargeDetails(models.Model):
    clientId = models.PositiveIntegerField(null=True)
    clientName = models.CharField(max_length=40)
    assignedPhysicianName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    health_status = models.CharField(max_length=100,null=True)

    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)

    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    professionalFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)