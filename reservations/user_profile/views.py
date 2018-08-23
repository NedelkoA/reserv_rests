from django.urls import reverse
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, UserProfileFormSet
from .models import UserProfile, User


class MyLoginView(LoginView):
    template_name = 'user_profile/login.html'

    # def get_success_url(self):
    #     return '/restaurants_list/'
    def get_redirect_url(self):
        return '/restaurants_list/'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user_profile/registration.html'
    success_url = '/restaurants_list/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        profile = UserProfile.objects.create(user=user)
        profile.telephone = form.cleaned_data.get('telephone')
        profile.save()
        return valid


class SaveSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        'first_name',
        'last_name',
        'email',
    )
    template_name = 'user_profile/settings.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            return redirect('/restaurants_list/')
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_profile'] = UserProfileFormSet(self.request.POST, instance=self.get_object())
        else:
            context['user_profile'] = UserProfileFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile = context['user_profile']
        with transaction.atomic():
            self.object = form.save()
            if profile.is_valid():
                profile.instance = self.object
                profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('save_changes', kwargs={'pk': self.kwargs['pk']})
