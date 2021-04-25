from django.contrib import admin
from .models import Buy,Sell,Rent,Filter,Tenant,Appointment

admin.site.register(Appointment)
admin.site.register(Filter)
admin.site.register(Buy)
admin.site.register(Sell)
admin.site.register(Rent)
admin.site.register(Tenant)
