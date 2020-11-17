from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    trust_score = forms.FloatField(
        widget=forms.HiddenInput(), initial=0, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1',
                  'password2', 'first_name', 'last_name', 'trust_score']
