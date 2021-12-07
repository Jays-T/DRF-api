from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Use rest framework built in permissions to set access
    to get/put read/write on profile objects
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
