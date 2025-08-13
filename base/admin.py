from django.contrib import admin
from .models import User, Products, Components, Cps_details, Order

# Register your models here.
admin.site.register(User)
admin.site.register(Products)
admin.site.register(Components)
admin.site.register(Cps_details)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'status']
    filter_horizontal = ('components_details',)  # Nice widget for M2M