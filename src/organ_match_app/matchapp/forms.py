
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from matchapp.choices import * 

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrganRequestForm(forms.Form):
    need_by = forms.DateField(input_formats=['%Y-%m-%d'], 
    widget = forms.TextInput(attrs={'placeholder': 'YYYY-mm-dd (please provide a date in the future)'}))
    organ = forms.ChoiceField(choices=ORGAN_CHOICES, required=True)

class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    birth_date = forms.DateField(input_formats=['%Y-%m-%d'], 
    widget=forms.TextInput(attrs={'placeholder': 'YYYY-mm-dd (must be 18 years of age or older)'}))
    blood_type = forms.ChoiceField(choices=BLOOD_TYPE_CHOICES, required=True)