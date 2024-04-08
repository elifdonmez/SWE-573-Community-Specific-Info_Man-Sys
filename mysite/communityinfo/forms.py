from django import forms
from django.forms import CheckboxInput
from .models import User, Community


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    kvkk_rules_accepted = forms.BooleanField(widget=CheckboxInput)

    class Meta:
        model = User
        fields = ['email', 'password']


class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']


class CommunityCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.TextInput)
    privacy = forms.BooleanField(widget=forms.CheckboxInput)

    class Meta:
        model = Community
        fields = ['name', 'description', 'privacy']

