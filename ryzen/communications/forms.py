from django import forms
from .models import CoordinatorMessage, Notification

class CoordinatorMessageForm(forms.ModelForm):
    CATEGORY_CHOICES = Notification.CATEGORY_CHOICES

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, initial='general')

    class Meta:
        model = CoordinatorMessage
        fields = ['message', 'target_members', 'category']
