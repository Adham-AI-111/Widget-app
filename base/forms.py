from .models import User, Order, OrderImages
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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone']


class GetOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['details', 'image', 'full_address', 'deposit', 'is_quick']
        labels = {
            'is_quick': 'quick order'
        }
        widgets = {
            'is_quick': forms.CheckboxInput(attrs={'class': 'toggle-checkbox', 'id': 'is_quick_toggle'}),
        }

# !---->
# class OrderImageForm(forms.ModelForm):
#     images = forms.FileField(
#         widget=forms.FileInput(attrs={
#             'multiple': True,
#             'accept': 'image/*',
#             'class': 'form-control'
#         }),
#         help_text='Select multiple images (max 5)'
#     )
    
    
#     class Meta:
#         model = OrderImages
#         fields = ['image']  # ← Keep this as 'image' (the actual model field)
    
#     def clean_images(self):  # ← Validation for the 'images' field
#         files = self.files.getlist('images')
        
#         if not files:
#             raise forms.ValidationError("Please select at least one image")
        
#         if len(files) > 5:  # ← Limit to 5 images
#             raise forms.ValidationError("Maximum 5 images allowed")
        
#         for file in files:
#             if file.size > 2 * 1024 * 1024:  # 2MB limit per file
#                 raise forms.ValidationError(f"File {file.name} is too large (max 2MB)")
            
#             if not file.content_type.startswith('image/'):
#                 raise forms.ValidationError(f"{file.name} is not a valid image file")
        
#         return files
