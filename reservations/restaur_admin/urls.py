from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'create_restaurant$', views.AddRestaurantView.as_view(), name='create_restaurant'),
    url(r'(?P<pk>[0-9]+)/tables$', views.EditTableView.as_view(), name='table'),
    url(r'(?P<pk>[0-9]+)/tables/create$', views.AddTableView.as_view(), name='create_table'),
    url(r'tables/(?P<pk>[0-9]+)/delete$', views.RemoveTableView.as_view(), name='delete_table'),
]
