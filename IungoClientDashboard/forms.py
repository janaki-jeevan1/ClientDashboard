import allauth.app_settings
from allauth import app_settings
from allauth.utils import get_username_max_length, set_form_field_order
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import pgettext

from .models import *
from allauth.account.forms import LoginForm, PasswordField

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.name)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=40)
    mobile_phone = forms.RegexField(max_length=10, required=True, regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(
        attrs={'class': 'input-sm form-control width-30', 'type': 'tel', 'pattern': '^\+?1?\d{9,15}$'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'mobile_phone', 'password1']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['mobile_phone'].widget.attrs['class'] = \
            "form-control"
        self.fields['mobile_phone'].widget.attrs['placeholder'] = 'Mobile Number'
        self.fields['email'].widget.attrs['class'] = \
            "form-control"
        self.fields['email'].widget.attrs['placeholder'] = 'Email ID'
        self.fields['password1'].widget.attrs['class'] = \
            "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = 'Please make sure your password is more than 8 letters'
        self.fields.pop('password2')


class PortfolioForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 30}))
    category = MyModelChoiceField(
        queryset=Category.objects.all(),
        required=False, )
    sub_category = MyModelChoiceField(queryset=sub_category.objects.all())

    class Meta:
        model = Portfolio
        fields = ['prefix', 'secondary_phone', 'tel_phone',
                  'experience', 'qualification', 'profile_pic', 'about_me', 'budget', 'category',
                  'sub_category',
                  ]

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        self.fields['prefix'].widget.attrs['class'] = \
            "form-control"
        self.fields['experience'].widget.attrs['class'] = \
            "form-control"
        self.fields['budget'].widget.attrs['class'] = \
            "form-control"
