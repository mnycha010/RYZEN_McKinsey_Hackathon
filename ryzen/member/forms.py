from django import forms
from django.contrib.auth.models import User
from .models import Member


class OnboardForm(forms.ModelForm):
    # Additional fields for registration
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    stokvel_id = forms.CharField(max_length=20, required=True, label="Stokvel ID")

    class Meta:
        model = Member
        fields = ["phone_number", "address", "date_of_birth"]
