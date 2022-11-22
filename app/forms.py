from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import N_user

class LoginForm(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput
    )
    
class SignupForm(forms.ModelForm):
    class Meta:
        model=N_user
        fields = ('first_name','last_name','username','password1','password2','email','role'
        )