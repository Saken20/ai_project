from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    number = forms.CharField(
        max_length=18, 
    )
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
