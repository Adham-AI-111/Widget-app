from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import User
from django.contrib import messages


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()  # This returns the user object with hashed password
            login(request, user)  # Login with the user object, not the form
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Redirect to home after successful registration
    context = {'form': form}
    return render(request, 'base/register.html', context)

def log_in(request):
    page = 'login'
    context = {'page': page}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        auth = authenticate(request, username=email, password=password)
        if auth is not None:
            login(request, auth)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'base/register.html', context)  
    return render(request, 'base/register.html', context)

@login_required(login_url='login')
def log_out(request):
    logout(request)
    messages.success(request, 'you logged out!')
    return render(request, 'base/home.html')

