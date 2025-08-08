from .models import User, Products, Components, Cps_details
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
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.split()) < 2:
            raise forms.ValidationError('Please enter your full name at least first and last name.')
        return full_name
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'describe', 'image','components']
        widgets = {
            'components': forms.CheckboxSelectMultiple(),
        }


class CreateComponentForm(forms.ModelForm):
    class Meta:
        model = Components
        fields = ['item', 'salary']
        widgets = {
            'item': forms.TextInput(attrs={'placeholder': 'Enter component name'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'Enter component salary'}),
        }
    
    def clean_item(self):
        item = self.cleaned_data.get('item')
        if Components.objects.filter(item__iexact=item).exists():
            raise forms.ValidationError('Component with this name already exists.')
        return item


class CreateCpsDetailsForm(forms.ModelForm):
    class Meta:
        model = Cps_details
        fields = "__all__"
        labels = {
            'part_name': 'Shape Name',
        }