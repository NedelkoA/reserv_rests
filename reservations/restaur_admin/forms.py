from django import forms
from django.forms import inlineformset_factory

from main.models import Table, Restaurant


class AddTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = (
            'table_number',
            'number_of_seats',
        )


class EditTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = (
            'table_number',
            'number_of_seats',
        )
        widgets = {
            'table_number': forms.TextInput(
                attrs={
                    'type': 'text',
                    'readonly': True
                })
        }


TableFormset = inlineformset_factory(
    Restaurant,
    Table,
    form=EditTableForm,
    can_delete=False,
    extra=0
)

