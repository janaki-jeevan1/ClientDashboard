from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    mobile_phone = forms.RegexField(max_length=10, required=True, regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(
        attrs={'class': 'input-sm form-control width-30', 'type': 'tel', 'pattern': '^\+?1?\d{9,15}$'}))

    class Meta:
        model = User
        fields = ['username', 'mobile_phone']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')

class PortfolioForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = ['user', 'prefix', 'gender', 'date_of_birth', 'mobile_phone', 'secondary_phone', 'tel_phone',
                  'experience', 'qualification', 'profile_pic', 'location', 'about_me']
