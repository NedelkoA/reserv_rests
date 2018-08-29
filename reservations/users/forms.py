from django import forms

from main.forms import ReservationForm


class UserReservationsForm(ReservationForm):
    pre_order = forms.BooleanField(
        required=False
    )

    class Meta(ReservationForm.Meta):
        exclude = (
            'contact_telephone',
        )
