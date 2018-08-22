from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from main.models import Restaurant, User, Table
from .forms import TableFormset


class AddRestaurantView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Restaurant
    fields = (
        'title',
        'number_tables',
        'open_time',
        'close_time',
    )
    login_url = 'login'
    permission_required = 'main.add_restaurant'
    template_name = 'restaur_admin/restaurant_create.html'

    def form_valid(self, form):
        form.instance.user = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.object.id})


class AddTableView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Restaurant
    fields = (
        'title',
        'number_tables',
        'open_time',
        'close_time',
    )
    login_url = 'login'
    permission_required = 'main.add_table'
    template_name = 'restaur_admin/table_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        TableFormset.max_num = restaurant.number_tables
        TableFormset.extra = restaurant.number_tables
        if self.request.POST:
            context['enum_tables'] = TableFormset(self.request.POST, instance=self.get_object())
        else:
            context['enum_tables'] = TableFormset(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        tables = context['enum_tables']
        print(tables)
        restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        with transaction.atomic():
            self.object = form.save()
            if tables.is_valid():
                tables.instance = self.object
                tables.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('table', kwargs={'pk': self.kwargs['pk']})
