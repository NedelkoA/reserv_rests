from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'restaurants_list/$', views.RestaurantsView.as_view(), name='restaurants_list'),
    url(r'restaurant/(?P<pk>[0-9])$', views.ReservationsView.as_view(), name='reservations'),
    url(r'restaurant/(?P<pk>[0-9])/create$', views.MakeReserve.as_view(), name='make_reserve'),
]
