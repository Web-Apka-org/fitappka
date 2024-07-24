from django import forms
from .models import Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'energy', 'fat', 'saturated_fat', 'carbo', 'sugar', 'salt', 'protein', 'fibre', 'alcohol']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'energy': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control'}),
            'saturated_fat': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbo': forms.NumberInput(attrs={'class': 'form-control'}),
            'sugar': forms.NumberInput(attrs={'class': 'form-control'}),
            'salt': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'fibre': forms.NumberInput(attrs={'class': 'form-control'}),
            'alcohol': forms.NumberInput(attrs={'class': 'form-control'}),
        }