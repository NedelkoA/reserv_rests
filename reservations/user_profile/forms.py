from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class SignUpForm(UserCreationForm):
    telephone = forms.CharField(max_length=13)
    status_user = forms.ChoiceField(
        choices=[
            ('usr', 'Client'),
            ('rst_adm', 'Restaurant admin')
        ]
    )


class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'telephone',
            'status_user',
        )


UserProfileFormSet = inlineformset_factory(
    User,
    UserProfile,
    form=SettingsForm,
    can_delete=False,
    extra=1
)

