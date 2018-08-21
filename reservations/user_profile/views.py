from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, SettingsForm, UserProfileFormSet
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
    form_class = SettingsForm
    template_name = 'user_profile/settings.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profile = UserProfile.objects.get(user=self.get_object())
        # context['form'] = SettingsForm(
        #     instance=self.get_object(),
        #     initial={
        #         'telephone': profile.telephone,
        #         'status_user': profile.status_user
        #     }
        # )
        context['form'] = UserProfileFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        profile = UserProfile.objects.get(user=self.get_object())
        profile.telephone = form.cleaned_data['telephone']
        profile.status_user = form.cleaned_data['status_user']
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('save_changes', kwargs={'pk': self.kwargs['pk']})
