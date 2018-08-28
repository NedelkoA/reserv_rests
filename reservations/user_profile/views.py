from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, UserProfileFormSet
from .models import UserProfile, User


class SignInView(LoginView):
    template_name = 'user_profile/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('restaurants_list'))
        return super().get(request, args, kwargs)

    def get_redirect_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return reverse('restaurants_list')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user_profile/registration.html'
    success_url = reverse_lazy('restaurants_list')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('restaurants_list'))
        return super().get(request, args, kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
        UserProfile.objects.create(
            user=user,
            telephone=form.cleaned_data.get('telephone'),
            status_user=form.cleaned_data.get('status_user')
        )
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
    success_url = reverse_lazy('save_changes')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_profile'] = UserProfileFormSet(self.request.POST, instance=self.request.user)
        else:
            context['user_profile'] = UserProfileFormSet(instance=self.request.user)
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
