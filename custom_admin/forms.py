from django import forms
from base.models import Order
from django.core.exceptions import ValidationError


class AdminOrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['price', 'status', 'paid', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'full_address': forms.TextInput(attrs={'placeholder': 'Enter full address'}),
            # 'is_paid': forms.CheckboxInput(attrs={'type':'checkbox', 'class': 'toggle-checkbox'}),
        }

class AdminOrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['details', 'full_address', 'is_quick', 'deposit', 'price', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'full_address': forms.TextInput(attrs={'placeholder': 'Enter full address'}),
            'is_quick': forms.CheckboxInput(attrs={'class': 'toggle-checkbox', 'id': 'is_quick_toggle'}),
        }
        labels = {
            'is_quick': 'quick order'
        }
