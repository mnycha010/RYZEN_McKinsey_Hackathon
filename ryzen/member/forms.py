from django import forms
from .models import Member, Stokvel

class OnboardForm(forms.ModelForm):
    stokvel = forms.ModelChoiceField(
        queryset=Stokvel.objects.filter(active=True),
        required=True,
        label="Select a Stokvel to join"
    )

    class Meta:
        model = Member
        fields = ["phone_number", "address", "date_of_birth", "stokvel"]
