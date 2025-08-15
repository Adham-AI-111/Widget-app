from django.urls import path
from . import views

urlpatterns = [
    path('useradmin/', views.admin_cards, name='admin_cards'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('admin_products/', views.admin_products, name='admin_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('components-shapes/', views.components_shapes, name='components_shapes'),
    path('access-components/', views.full_access_components_shapes, name='access_components'),
    path('edit-component/<int:pk>/', views.edit_component, name='edit_component'),
    path('edit-shape/<int:pk>/', views.edit_shape, name='edit_shape'),
]