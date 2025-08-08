from django.urls import path
from . import admin_views

urlpatterns = [
    path('useradmin/', admin_views.admin, name='admin'),
    path('add-product/', admin_views.add_product, name='add_product'),
    path('access-components/', admin_views.full_access_components, name='access_components'),
]