from django import forms 
from .models import Pet, CustomUser, Product
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user

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