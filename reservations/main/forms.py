from datetime import datetime

from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            choices = [
                (table, 'Table ' + str(table))
                for table in range(1, kwargs['instance'].number_of_tables + 1)
            ]
            self.fields['table'] = forms.ChoiceField(choices=choices)
            choices_time = [
                ('{}:00'.format(hour), '{}:00'.format(hour))
                for hour in range(
                    int(str(kwargs['instance'].open_time)[:2]),
                    int(str(kwargs['instance'].close_time)[:2])
                )
            ]
            self.fields['time'] = forms.ChoiceField(choices=choices_time)

    def clean(self):
        cleaned_data = super().clean()
        visitors = cleaned_data.get('visitors')
        table = cleaned_data.get('table')
        if visitors > int(table):
            raise forms.ValidationError(
                'Visitors more than places on table',
                code='invalid'
            )
        return cleaned_data

    class Meta:
        model = Reservation
        fields = (
            'date',
            'time',
            'visitors',
            'table',
            'contact_telephone'
        )
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': str(datetime.date(datetime.today()))
                })
        }
