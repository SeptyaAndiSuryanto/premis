from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class PremisAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Name'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))