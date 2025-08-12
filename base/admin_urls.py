from django.urls import path
from . import admin_views

urlpatterns = [
    path('useradmin/', admin_views.admin, name='admin'),
    path('add-product/', admin_views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', admin_views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', admin_views.delete_product, name='delete_product'),
    path('components-shapes/', admin_views.components_shapes, name='components_shapes'),
    path('access-components/', admin_views.full_access_components_shapes, name='access_components'),
    path('delete-component/<int:pk>/', admin_views.delete_component, name='delete_component'),
    path('delete-shape/<int:pk>/', admin_views.delete_shape, name='delete_shape'),
]