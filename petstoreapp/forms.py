from django import forms 
from .models import Pet, Product

class PetForm(forms.ModelForm):
    
    class Meta:
        model = Pet
        fields =  ['name', 'breed', 'price', 'image', 'category']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PetSearchForm(forms.Form):
    search_query = forms.CharField(label="Search", max_length=100)

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields =  ['name', 'description', 'price', 'category', 'quantity', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            
        } 