from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import NotFound

from ..models import UserProfile
from . import serializers
from . import permissions as custom_perms


class UserView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (
        custom_perms.IsOwner,
    )

    def list(self, request, *args, **kwargs):
        raise NotFound

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUserProfileSerializer
        return self.serializer_class
