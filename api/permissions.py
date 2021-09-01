from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import CustomUser


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role in [CustomUser.ADMIN,
                                         CustomUser.MODERATOR])


class CanDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method == 'DELETE'
                and obj.author == request.user)


class ReadPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == 'GET'


class IsPostOrGetRequest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in ['POST', 'GET']


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_superuser


class NotAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.auth


class IsSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
