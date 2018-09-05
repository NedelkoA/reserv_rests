from rest_framework import viewsets
from rest_framework import permissions

from ..models import Restaurant
from . import serializers
from . import permissions as custom_perms


class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_perms.IsRestaurantAdminOrReadOnly,
    )

