from datetime import datetime

from django import forms

from .models import Reservation, Restaurant


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            choices = [
                (table, 'Table ' + str(table))
                for table in range(1, kwargs['instance'].number_tables + 1)
            ]
            self.fields['table'] = forms.ChoiceField(choices=choices)
            choices_time = [
                ('{}:00'.format(hour), '{}:00'.format(hour))
                for hour in range(
                    int(str(kwargs['instance'].open_time[:2])),
                    int(str(kwargs['instance'].close_time[:2]))
                )
            ]
            self.fields['time'] = forms.ChoiceField(choices=choices_time)

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'visitors', 'table', 'contact_telephone']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': str(datetime.date(datetime.today()))
                }),
            'visitors': forms.NumberInput(
                attrs={
                    'min': 1,
                    'max': 6
                })
        }
