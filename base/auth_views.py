from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import User
from django.contrib import messages
# --- for reset password ---
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .services.emails import EmailServices
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


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


class CoustomPasswordResetView(PasswordResetView, SuccessMessageMixin):
    template_name = 'base/reset_password/reset_password_form.html'
    success_url = reverse_lazy('confirm-view')
    success_message = 'check your email to reset password link'
    email_template_name = 'base/emails/reset_password_email.html'
    # subject_template_name = 'base/emails/reset_password_email.txt'
    html_email_template_name = 'base/emails/reset_password_email.html'

    def form_valid(self, form):
        # ? another way to send reset password email by your own class
        email = form.cleaned_data['email']
        # # Django's built-in method that finds active users with this email, Returns a list (usually one user, but could be multiple)
        users = form.get_users(email)

        for user in users:
            # Create context for your service
            context = {
                'user': user,
                'domain': self.request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
            
        #     # Use your existing email service
            email_service = EmailServices()
            email_service.send_password_reset_email(user.email, context)
        return super().form_valid(form)


class CoustomPasswordResetDoneView(PasswordResetDoneView):
    # we will merge the confirm-password temp in email message
    template_name = 'base/reset_password/reset_password_done.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class CoustomPasswordResetConfirmView(PasswordResetConfirmView, SuccessMessageMixin): 
    template_name = 'base/reset_password/reset_password_confirm.html'
    success_url = reverse_lazy('complete-view')
    success_message = 'password reset successfully'
    form_class = SetPasswordForm

    def form_valid(self, form):
        return super().form_valid(form)

class CoustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'base/reset_password/reset_password_complete.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)