from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAdminOrReadSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if view.action in ("create", "destroy"):
            if not (request.user.is_staff or request.user.is_superuser):
                raise PermissionDenied("Anda tidak punya akses untuk melakukan aksi ini.")

        return True
    

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff or user.is_superuser:
            return True

        if obj.pk == user.pk:
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method in ("PUT", "PATCH"):
                return True
            
        raise PermissionDenied("Anda tidak punya akses untuk melakukan aksi ini.")