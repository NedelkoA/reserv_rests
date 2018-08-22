from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'create$', views.AddRestaurantView.as_view(), name='create'),
    url(r'(?P<pk>[0-9]+)/tables$', views.AddTableView.as_view(), name='table'),
]
