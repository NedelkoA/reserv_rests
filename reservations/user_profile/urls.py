from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    url(r'login$', views.MyLoginView.as_view(), name='login'),
    url(r'logout$', LogoutView.as_view(next_page='restaurants_list'), name='logout'),
    url(r'sign_up$', views.SignUpView.as_view(), name='sign_up'),
    url(r'(?P<pk>[0-9])/settings/$', views.SaveSettingsView.as_view(), name='save_changes'),
]
