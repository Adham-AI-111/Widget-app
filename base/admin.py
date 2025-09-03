from django.contrib import admin
from .models import User, Order, OrderImages

# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderImages)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'product', 'status']
#     filter_horizontal = ('components_details',)  # Nice widget for M2M