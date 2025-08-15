from django import forms
from base.models import Products, Components, Cps_details

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
