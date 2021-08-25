from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['sale_employee', 'sale_quantity']
        widgets = {
            'sale_employee': forms.Select(attrs = {'class': 'form-control', 'required': True}),
            'sale_quantity': forms.NumberInput(attrs = {'class': 'form-control', 'required': True, 'min': 1})
        }
