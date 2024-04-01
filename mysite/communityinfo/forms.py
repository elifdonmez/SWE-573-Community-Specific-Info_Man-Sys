from django import forms
from django.forms import CheckboxInput

from .models import User

class RegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    kvkk_rules_accepted = forms.BooleanField(widget=CheckboxInput)

    class Meta:
        model = User
        fields = ['email', 'password']
