from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<pk>[0-9])/make_reserve$', views.UserReservationView.as_view(), name='user_reserve'),
]
