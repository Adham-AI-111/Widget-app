from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password1', 'password2']
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError('email was already existed!!')
            return email