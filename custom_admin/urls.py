from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('useradmin/', views.admin_cards, name='admin_cards'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('delay-orders/', views.delayed_balance_orders, name='delay_orders'),
    path('quick-orders/', views.quick_orders, name='quick_orders'),
    path('edit-order/<int:pk>/', views.edit_order, name='edit_order'),
    path('add-order/', views.add_order, name='add_order'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)