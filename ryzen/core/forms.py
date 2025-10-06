# core/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="User Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your User name"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )
