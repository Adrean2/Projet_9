from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import TextInput,PasswordInput
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63,
        widget=TextInput(attrs={
            "placeholder":"Nom d'utilisateur",
            "class":"form-text"}),
            label="")
    password = forms.CharField(max_length=63,
        widget=PasswordInput(attrs={
            "placeholder": "Mot de passe",
            "class":"form-text"}),
            label="")

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.User
        fields = ['username']

