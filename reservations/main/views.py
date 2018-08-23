from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse

from .models import Restaurant, Reservation
from .forms import ReservationForm


class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'main/index.html'


class ReservationsView(DetailView):
    model = Restaurant
    template_name = 'main/detail.html'

    def get(self, request, *args, **kwargs):
        if 'date' in request.GET:
            reserves_time = Reservation.objects.filter(
                restaurant=self.get_object(),
                date=request.GET['date']
            ).values('time')
            #print(list(reserves_time))
            data = {
                'reserve': list(reserves_time)
            }
            return JsonResponse(data)
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(
            restaurant=self.get_object(),
            date=datetime.date(datetime.now()))
        context['form'] = ReservationForm(
            instance=Restaurant.objects.get(id=self.kwargs['pk']))
        print(context['form'].fields['time'].choices)
        return context


class MakeReserve(CreateView):
    form_class = ReservationForm
    template_name = 'main/detail.html'

    def form_valid(self, form):
        form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('reservations', kwargs={'pk': self.kwargs['pk']})
