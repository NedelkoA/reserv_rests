from django import forms
from django.forms import inlineformset_factory

from main.models import Table, Restaurant, User


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = (
            'numb',
            'count_sits',
        )


TableFormset = inlineformset_factory(
    Restaurant,
    Table,
    form=TableForm,
    can_delete=False,
    extra=0
)

