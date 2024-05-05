from django import forms
from django.forms import CheckboxInput
from .models import RegisteredUser, Community, Posts, UserProfile, PostTemplate


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    kvkk_rules_accepted = forms.BooleanField(widget=CheckboxInput)

    class Meta:
        model = RegisteredUser
        fields = ['email', 'password']


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea())
    photo = forms.ImageField(widget=forms.FileInput)
    title = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = UserProfile
        fields = ['bio', 'photo', 'title']


class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = RegisteredUser
        fields = ['email', 'password']


class CommunityCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    privacy = forms.BooleanField(required=False, widget=forms.CheckboxInput, initial=False)
    rules = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Community
        fields = ['name', 'description', 'privacy', 'rules']


class EditRulesForm(forms.ModelForm):
    rules = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Community
        fields = ['rules']


class TextBasedPostForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Posts
        fields = ['header', 'description']


class PostTemplateForm(forms.Form):
    name = forms.CharField(label='Template Name', max_length=100)
    fields = forms.MultipleChoiceField(
        label='Select Fields',
        choices=[
            ('description', 'Description'),
            ('image_url', 'Image URL'),
            ('video_url', 'Video URL'),
            ('geolocation', 'Geolocation'),
            ('date_time_fields', 'Date-Time Field'),
            ('audio_url', 'Audio URL')
        ],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    is_mandatory = forms.BooleanField(required=False, widget=forms.CheckboxInput, initial=False)

    class Meta:
        model = PostTemplate
        fields = ['name']