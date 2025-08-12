from .models import User, Products, Components, Cps_details, Order, Address
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
            # or 'components': forms.SelectMultiple(),
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


class OrderForm(forms.ModelForm):
    def __init__(self, product=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if product:
            self.create_component_choice_fields(product)
    
    def create_component_choice_fields(self, product):
        # Loop through all components of the product
        for component in product.components.all():
            field_name = f'component_{component.id}_choice'
            
            # Get choices for this component (its Cps_details)
            choices = self.get_choices_for_component(component)
            
            # generate a choice field for each component
            self.fields[field_name] = forms.ChoiceField(
                choices=choices,
                required=False,
                label=f"{component.item} Options",
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'data-component-id': component.id
                })
            )
    
    def get_choices_for_component(self, component):
        choices = [('', f'--- Select {component.item} ---')]
        
        # Add choices from Cps_details related to this component
        for detail in component.cps_details_set.all():
            choices.append((detail.id, f"{detail.part_name}: ${detail.price:.2f}"))
        
        return choices

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            
            # Handle the selected component details
            selected_details = []
            selected_components = []
            
            for field_name, value in self.cleaned_data.items():
                if field_name.startswith('component_') and field_name.endswith('_choice') and value:
                    try:
                        detail = Cps_details.objects.get(id=value)
                        selected_details.append(detail)
                        selected_components.append(detail.component)
                    except Cps_details.DoesNotExist:
                        pass
            
            # Set the relationships
            if selected_details:
                instance.components_details.set(selected_details)
            if selected_components:
                instance.components.set(selected_components)
        
        return instance

    class Meta:
        model = Order
        fields = ['amount', 'due_date']  # Removed 'components' from here
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }