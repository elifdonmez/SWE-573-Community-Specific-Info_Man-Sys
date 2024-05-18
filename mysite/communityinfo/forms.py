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


class AdvancedSearchForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    geolocation = forms.CharField(widget=forms.TextInput)
    date_time_field = forms.DateTimeField(widget=forms.DateTimeInput)

    def __init__(self, *args, **kwargs):
        template = kwargs.pop('template', None)
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        if template is not None:
            self.generate_form_fields(template)

    def generate_form_fields(self, template):
        self.fields.clear()
        field_definitions = template.fields.split(',')
        for field_info in field_definitions:
            field_name, order, requirement, field_label = field_info.split(':')

            if field_name == 'header':
                self.fields['header'] = forms.CharField(widget=forms.TextInput, label=field_label, required=False)
            elif field_name == 'description':
                self.fields['description'] = forms.CharField(widget=forms.Textarea, label=field_label, required=False)
            elif field_name == 'geolocation':
                self.fields['geolocation'] = forms.CharField(widget=forms.TextInput, label=field_label, required=False)
            elif field_name == 'date_time_field':
                self.fields['date_time_field'] = forms.DateTimeField(widget=forms.DateTimeInput, label=field_label, required=False)

    class Meta:
        model = Posts
        fields = ['header', 'description', 'geolocation', 'date_time_field']


class CustomTemplatePostForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    image_url = forms.CharField(widget=forms.TextInput)
    video_url = forms.CharField(widget=forms.TextInput)
    geolocation = forms.CharField(widget=forms.TextInput)
    date_time_field = forms.DateTimeField(widget=forms.DateTimeInput)
    audio_url = forms.CharField(widget=forms.TextInput)
    template_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        template = kwargs.pop('template', None)
        super(CustomTemplatePostForm, self).__init__(*args, **kwargs)
        if template is not None:
            self.generate_form_fields(template)
            self.initial['template_id'] = template.id

    def generate_form_fields(self, template):
        self.fields.clear()
        field_definitions = template.fields.split(',')
        for field_info in field_definitions:
            field_name, order, requirement, field_label = field_info.split(':')
            required = requirement == 'mandatory'
            field_type = forms.CharField if field_name == 'description' else forms.CharField
            self.fields[field_name] = field_type(widget=forms.TextInput, label=field_label, required=required)
        self.fields['template_id'] = field_type(widget=forms.HiddenInput(attrs={'value':template.id}), required=True)

    class Meta:
        model = Posts
        fields = ['header', 'description', 'image_url', 'video_url', 'geolocation', 'date_time_field', 'audio_url',
                  'template_id']



class PostTemplateForm(forms.Form):
    name = forms.CharField(label='Template Name', max_length=100)
    fields = forms.MultipleChoiceField(
        label='Select Fields',
        choices=[
            ('description', 'Description'),
            ('image_url', 'Image URL'),
            ('video_url', 'Video URL'),
            ('geolocation', 'Geolocation'),
            ('date_time_field', 'Date-Time'),
            ('audio_url', 'Audio URL')
        ],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    is_mandatory = forms.BooleanField(required=False, widget=forms.CheckboxInput, initial=False)
    custom_labels = forms.CharField(widget=forms.TextInput, max_length=50)

    class Meta:
        model = PostTemplate
        fields = ['name']
