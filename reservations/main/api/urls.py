from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'restaurant', views.RestaurantView)

urlpatterns = [
    url(r'', include(router.urls))
]
