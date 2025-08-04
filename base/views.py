from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def home(request):
    return render(request, 'base/home.html')
