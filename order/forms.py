# form tag의 label 표시용
from django import forms
from order.models import Stock

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        widgets = {
            'st_name': forms.TextInput(attrs={'class': 'form-control'}),
            'st_quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'st_price': forms.TextInput(attrs={'class': 'form-control'})
        }