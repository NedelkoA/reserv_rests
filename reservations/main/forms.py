from datetime import datetime

from django import forms

from .models import Reservation, Table


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop('restaurant', None)
        super(ReservationForm, self).__init__(*args, **kwargs)
        if restaurant:
            self.fields['table'].queryset = Table.objects.filter(restaurant=restaurant)
            choices_time = [
                ('{}:00'.format(hour), '{}:00'.format(hour))
                for hour in range(
                    int(str(restaurant.open_time)[:2]),
                    int(str(restaurant.close_time)[:2])
                )
            ]
            self.fields['time'] = forms.ChoiceField(choices=choices_time)

    def clean(self):
        cleaned_data = super().clean()
        visitors = cleaned_data.get('visitors')
        table = cleaned_data.get('table')
        if visitors > int(table.number_of_seats):
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
