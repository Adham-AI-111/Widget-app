from django.urls import path
from . import admin_views

urlpatterns = [
    path('useradmin/', admin_views.admin, name='admin'),
    path('add-product/', admin_views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', admin_views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', admin_views.delete_product, name='delete_product'),
    path('access-components/', admin_views.full_access_components, name='access_components'),
]