from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet

from main.models import Table, Restaurant, User


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = (
            'numb',
            'count_sits',
        )


class RestaurauntForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = (
            'title',
            'number_tables',
            'open_time',
            'close_time',
        )


TableFormset = inlineformset_factory(
    Restaurant,
    Table,
    form=TableForm,
    can_delete=False
)
RestaurantFormset = inlineformset_factory(
    User,
    Restaurant,
    fields=('user',),
    can_delete=False,
)
# TableFormSet = formset_factory(
#     form=TableForm,
#     can_delete=False,
# )


# class BaseRestaurantFormset(BaseInlineFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#
#         form.nested = TableFormSet(
#             instance=form.instance,
#             data=form.data if form.is_bound() else None,
#             files=form.files if form.is_bound else None,
#             prefix='table-%s-%s' % (
#                 form.prefix,
#                 TableFormSet.get_default_prefix()),
#             extra=1)
#
#     def save(self, commit=True):
#         result = super().save(commit=commit)
#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     form.nested.save(commit=commit)
#         return result
#
#
# RestaurantFormset = inlineformset_factory(
#     User,
#     Restaurant,
#     formset=BaseRestaurantFormset,
#     fields=(),
#     extra=1
# )
