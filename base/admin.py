from django.contrib import admin
from .models import User, Products, Components, Cps_details

# Register your models here.
admin.site.register(User)
admin.site.register(Products)
admin.site.register(Components)
admin.site.register(Cps_details)