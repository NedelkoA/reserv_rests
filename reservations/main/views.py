from datetime import datetime

from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.http import JsonResponse, Http404

from .models import Restaurant, Reservation
from .forms import ReservationForm


class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'main/index.html'


class MakeReserve(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'main/detail.html'

    def form_valid(self, form):
        print(self.kwargs['pk'])
        form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        print(form.instance.restaurant)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('make_reserve', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['instance'] = Restaurant.objects.get(id=self.kwargs['pk'])
        return kw

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        context['reservations'] = Reservation.objects.filter(
            restaurant=restaurant,
            date=datetime.date(datetime.now()))
        return context


def get_dates(request, pk):
    if not request.is_ajax():
        raise Http404
    else:
        if request.method == 'GET':
            if 'date' in request.GET and 'time' in request.GET:
                reserves_tables = Reservation.objects.filter(
                    restaurant_id=pk,
                    date=request.GET['date'],
                    time=request.GET['time']
                ).values('table')
                data = {
                    'reserve_tables': list(reserves_tables)
                }
                return JsonResponse(data)
