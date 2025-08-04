from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', auth_views.signup, name='signup'),
    path('login/', auth_views.log_in, name='login'),
    path('logout/', auth_views.log_out, name='logout'),
]