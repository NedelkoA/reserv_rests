from rest_framework import permissions


class IsRestaurantAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile.status_user == 'rst_adm'
