from django.shortcuts import render, redirect

def admin(request):
    return render(request, 'base/admin.html')