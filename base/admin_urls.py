from django.urls import path
from . import admin_views

urlpatterns = [
    path('useradmin/', admin_views.admin, name='admin'),
]