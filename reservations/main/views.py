from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Restaurant, Reservation
from .forms import ReservationForm


class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'main/index.html'


class ReservationsView(DetailView):
    model = Restaurant
    template_name = 'main/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(
            restaurant=self.get_object(),
            date=datetime.date(datetime.now()))
        context['form'] = ReservationForm(
            instance=Restaurant.objects.get(id=self.kwargs['pk']))
        return context


class MakeReserve(CreateView):
    form_class = ReservationForm
    template_name = 'main/detail.html'

    def form_valid(self, form):
        form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('reservations', kwargs={'pk': self.kwargs['pk']})
