from django.contrib import admin
from .models import Physician, Client, Appointment, ClientDischargeDetails

# Register your models here.
class PhysicianAdmin(admin.ModelAdmin):
    pass
admin.site.register(Physician, PhysicianAdmin)

class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class ClientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClientDischargeDetails, ClientDischargeDetailsAdmin)