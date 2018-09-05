from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from main.models import Restaurant, User, Table
from user_profile.models import UserProfile
from .forms import TableFormset, AddTableForm


class AddRestaurantView(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = (
        'title',
        'number_of_tables',
        'open_time',
        'close_time',
    )
    login_url = 'login'
    template_name = 'restaur_admin/restaurant_create.html'

    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        if profile.status_user == 'rst_adm':
            return super().get(request, args, kwargs)
        return redirect(reverse('restaurants_list'))

    def form_valid(self, form):
        if Restaurant.objects.filter(title=form.cleaned_data['title']):
            messages.add_message(self.request, messages.INFO,
                                 'This restaurant already is create.')
            return redirect(reverse('create_restaurant'))
        form.instance.user = User.objects.get(id=self.request.user.id)
        restaurant = form.save()
        Table.objects.bulk_create([
            Table(
                table_number=number_table,
                number_of_seats=2,
                restaurant=restaurant
            )
            for number_table in range(1, restaurant.number_of_tables + 1)
        ])
        return redirect(reverse('table', kwargs={'pk': restaurant.id}))

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.object.id})


class EditTableView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    fields = (
        'title',
        'number_of_tables',
        'open_time',
        'close_time',
    )
    template_name = 'restaur_admin/tables_edit.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return redirect(reverse('restaurants_list'))
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['enum_tables'] = TableFormset(
                self.request.POST,
                instance=obj
            )
            if context['enum_tables'].is_valid():
                context['enum_tables'].save()
        else:
            context['enum_tables'] = TableFormset(
                instance=obj
            )
        context['objects_list'] = Table.objects.filter(restaurant=obj)
        context['add_form'] = AddTableForm()
        return context

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.kwargs['pk']})


class AddTableView(LoginRequiredMixin, CreateView):
    model = Table
    fields = (
        'table_number',
        'number_of_seats',
    )
    login_url = 'login'

    def form_valid(self, form):
        restaurant_object = Restaurant.objects.get(id=self.kwargs['pk'])
        form.instance.restaurant = restaurant_object
        restaurant_object.number_of_tables = restaurant_object.number_of_tables + 1
        restaurant_object.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        obj = Restaurant.objects.get(id=kwargs['pk'])
        if obj.user != self.request.user:
            return redirect(reverse('restaurants_list'))
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.kwargs['pk']})


class RemoveTableView(LoginRequiredMixin, DeleteView):
    model = Table

    def post(self, request, *args, **kwargs):
        restaurant = self.get_object().restaurant
        if restaurant.user != self.request.user:
            return redirect(reverse('restaurants_list'))
        restaurant.number_of_tables = restaurant.number_of_tables - 1
        restaurant.save()
        return super().post(request, args, kwargs)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.get_object().restaurant.id})
