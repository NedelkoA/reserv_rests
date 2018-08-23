from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Restaurant, User, Table
from user_profile.models import UserProfile
from .forms import TableFormset, TableForm


class AddRestaurantView(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = (
        'title',
        'number_tables',
        'open_time',
        'close_time',
    )
    login_url = 'login'
    template_name = 'restaur_admin/restaurant_create.html'

    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        if profile.status_user == 'rst_adm':
            return super().get(request, args, kwargs)
        return redirect('/restaurants_list/')

    def form_valid(self, form):
        form.instance.user = User.objects.get(id=self.request.user.id)
        restaurant = form.save()
        Table.objects.bulk_create([
            Table(
                numb=number_table,
                count_sits=2,
                restaurant=restaurant
            )
            for number_table in range(1, restaurant.number_tables + 1)
        ])
        return redirect(reverse('table', kwargs={'pk': restaurant.id}))

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.object.id})


class EditTableView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    fields = (
        'title',
        'number_tables',
        'open_time',
        'close_time',
    )
    template_name = 'restaur_admin/tables_edit.html'

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
        context['add_form'] = TableForm()
        return context

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return redirect('/restaurants_list/')
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.kwargs['pk']})


class AddTableView(LoginRequiredMixin, CreateView):
    model = Table
    fields = (
        'numb',
        'count_sits',
    )
    login_url = 'login'

    def form_valid(self, form):
        restaurant_object = Restaurant.objects.get(id=self.kwargs['pk'])
        form.instance.restaurant = restaurant_object
        restaurant_object.number_tables = restaurant_object.number_tables + 1
        restaurant_object.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        obj = Restaurant.objects.get(id=kwargs['pk'])
        if obj.user != self.request.user:
            return redirect('/restaurants_list/')
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.kwargs['pk']})


class RemoveTableView(LoginRequiredMixin, DeleteView):
    model = Table

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.restaurant.user != self.request.user:
            return redirect('/restaurants_list/')
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.get_object().restaurant.id})
