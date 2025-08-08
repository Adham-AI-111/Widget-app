from django.shortcuts import render, redirect
from .models import User, Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'base/home.html')


@login_required(login_url='login')  
def profile(request):
    user = request.user

    context = {'user': user}
    return render(request, 'base/profile.html', context)

def gallery(request):
    return render(request, 'base/gallery.html')