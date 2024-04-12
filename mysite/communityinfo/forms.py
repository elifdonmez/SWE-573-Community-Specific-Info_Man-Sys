from django import forms
from django.forms import CheckboxInput
from .models import RegisteredUser, Community, Posts


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    kvkk_rules_accepted = forms.BooleanField(widget=CheckboxInput)

    class Meta:
        model = RegisteredUser
        fields = ['email', 'password']


class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = RegisteredUser
        fields = ['email', 'password']


class CommunityCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.TextInput)
    privacy = forms.NullBooleanField(widget=forms.CheckboxInput)
    rules = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Community
        fields = ['name', 'description', 'privacy', 'rules']


class EditRulesForm(forms.ModelForm):
    rules = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Community
        fields = ['rules']


class TextBasedPostForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Posts
        fields = ['header', 'description']
