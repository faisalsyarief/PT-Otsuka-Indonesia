from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AttendancePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True

        if view.action in ("destroy", "list"):
            return True 
        if view.action == "create":
            return True

        return True


    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff or user.is_superuser:
            return True

        if obj.karyawan == user:
            return True

        raise PermissionDenied("Anda tidak punya akses untuk melakukan aksi ini.")
