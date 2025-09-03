from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', auth_views.signup, name='signup'),
    path('login/', auth_views.log_in, name='login'),
    path('logout/', auth_views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('orders/', views.user_orders, name='user_orders'),
    path('get-order/', views.get_order, name='get_order'),
    path('upload_images/<int:order_id>/', views.upload_order_images, name='upload_images'),
    path('uedit-order/<int:pk>/', views.user_edit_order, name='uedit_order'),
    path('reset-password/', auth_views.CoustomPasswordResetView.as_view(), name='reset-password'),
    path('reset-password/done', auth_views.CoustomPasswordResetDoneView.as_view(), name='confirm-view'),
    path('confirm-password/<uidb64>/<token>/', auth_views.CoustomPasswordResetConfirmView.as_view(), name='confirm-password'),
    path('confirm-password/done', auth_views.CoustomPasswordResetCompleteView.as_view(), name='complete-view')
]