from django import forms
from .models import Party, Invitation
from .choices import *

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['invite_code']
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'invite_code',
                'required': True,
                'placeholder': "Say something..."
            }),
        }
    def __init__(self, *args, **kwargs):
        super(PartyForm, self).__init__(*args, **kwargs)
        self.fields['invite_code'].widget.attrs.update({'class' : 'form-control form-control-lg', 'placeholder' : 'Enter your invite code here...'})
        self.fields['invite_code'].label = ''

class RsvpForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect())