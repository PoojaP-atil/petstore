from django import forms
from .models import register

class form(forms.ModelForm):
    class Meta:
        model = register
        fields = '__all__'
