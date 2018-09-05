from datetime import timedelta

from django.views.generic import CreateView
from django.shortcuts import reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserReserve
from .forms import UserReservationsForm
from .tasks import send_notification
from main.models import Restaurant, Reservation
from .utils.date_converter import DateConversion


class UserReservationView(LoginRequiredMixin, CreateView):
    form_class = UserReservationsForm
    template_name = 'users/user_reserve.html'
    login_url = 'login'

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        if Reservation.objects.filter(
            restaurant=restaurant,
            table=form.cleaned_data['table'],
            date=form.cleaned_data['date'],
            time=form.cleaned_data['time']
        ):
            return redirect(reverse('user_reserve', kwargs={'pk': self.kwargs['pk']}))
        form.instance.restaurant = restaurant
        form.instance.contact_telephone = self.request.user.profile.telephone
        reservation = form.save()
        UserReserve.objects.create(
            reservations=reservation,
            user=self.request.user,
            pre_order=form.cleaned_data['pre_order']
        )
        reserve_time = DateConversion(reservation.date, reservation.time)
        send_notification.apply_async([
            self.request.user.profile.telegram_id,
            reservation.restaurant.title],
            eta=reserve_time.utc_time() - timedelta(hours=1)
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = UserReserve.objects.filter(user=self.request.user)
        return context

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['restaurant'] = Restaurant.objects.get(id=self.kwargs['pk'])
        return kw

    def get_success_url(self, **kwargs):
        return reverse('user_reserve', kwargs={'pk': self.kwargs['pk']})


